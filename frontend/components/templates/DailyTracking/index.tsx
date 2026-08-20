"use client";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Label } from "@/components/ui/label";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  fetchDailyTracking,
  useDailyTrackingQuery,
} from "@/lib/backend/daily_tracking";
import {
  useDriversQuery,
  useManagersQuery,
} from "@/lib/backend/users/managers";
import {
  cn,
  formatDateBackend,
  isPlanAShipment,
  managerFullName,
} from "@/lib/utils";
import { useYMaps } from "@pbe/react-yandex-maps";
import Color from "color";
import { CalendarIcon, Loader2, RefreshCw } from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { CITIES, CityKey, DEFAULT_CITY } from "../maps/constants";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";

const APP_TIME_ZONE = "Asia/Almaty";

const DailyTrackingTemplate = () => {
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [selectedPersonId, setSelectedPersonId] = useState<string>();
  const selectedDateString = formatDateBackend(selectedDate);

  const people = useTrackingPeople();
  const [snapshot, setSnapshot] = useState<DailyTrackingResponse>();
  const [trackingManager, setTrackingManager] = useState<DailyTrackingManager>();
  const [plans, setPlans] = useState<Plan[]>([]);
  const [geopoints, setGeopoints] = useState<ManagerGeoPoint[]>([]);
  const [cursor, setCursor] = useState<DailyTrackingCursor | null>(null);
  const [timeline, setTimeline] = useState<DailyTrackingTimelineRow[]>([]);
  const [currentGeopoint, setCurrentGeopoint] =
    useState<ManagerGeoPoint | null>(null);
  const cursorCreatedAt = cursor?.created_at;
  const cursorId = cursor?.id;
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [activeRowId, setActiveRowId] = useState<string>();
  const [activePlanId, setActivePlanId] = useState<string>();

  const fullQuery = useDailyTrackingQuery(
    { managerId: selectedPersonId, date: selectedDateString },
    Boolean(selectedPersonId && selectedDateString),
  );

  useEffect(() => {
    setSnapshot(undefined);
    setTrackingManager(undefined);
    setPlans([]);
    setGeopoints([]);
    setCursor(null);
    setTimeline([]);
    setCurrentGeopoint(null);
    setActiveRowId(undefined);
    setActivePlanId(undefined);
  }, [selectedPersonId, selectedDateString]);

  useEffect(() => {
    if (!fullQuery.data) return;
    setSnapshot(fullQuery.data);
    setTrackingManager(fullQuery.data.manager);
    setPlans(fullQuery.data.plans ?? []);
    setGeopoints(fullQuery.data.geopoints);
    setCursor(fullQuery.data.cursor);
    setTimeline(fullQuery.data.timeline);
    setCurrentGeopoint(fullQuery.data.current_geopoint);
  }, [fullQuery.data]);

  const refreshDelta = useCallback(async () => {
    if (!selectedPersonId || !selectedDateString || isRefreshing) return;

    setIsRefreshing(true);
    try {
      const data = await fetchDailyTracking({
        managerId: selectedPersonId,
        date: selectedDateString,
        sinceCreatedAt: cursorCreatedAt,
        sinceId: cursorId,
      });

      setSnapshot(data);
      setTrackingManager(data.manager);
      setPlans(data.plans);
      setGeopoints((current) => mergeGeopoints(current, data.geopoints));
      setCursor(data.cursor);
      setTimeline(data.timeline);
      setCurrentGeopoint(data.current_geopoint);
    } finally {
      setIsRefreshing(false);
    }
  }, [
    selectedPersonId,
    selectedDateString,
    isRefreshing,
    cursorCreatedAt,
    cursorId,
  ]);

  useEffect(() => {
    if (!selectedPersonId || !selectedDateString || !isToday(selectedDate)) return;

    const intervalId = window.setInterval(() => {
      refreshDelta();
    }, 1000 * 60 * 2);

    return () => window.clearInterval(intervalId);
  }, [selectedPersonId, selectedDate, selectedDateString, refreshDelta]);

  const matchingRows = useMemo(() => {
    if (!activePlanId) return [];
    return timeline.filter((row) => rowTouchesPlan(row, activePlanId));
  }, [activePlanId, timeline]);

  useEffect(() => {
    if (!matchingRows[0]) return;
    document
      .getElementById(`daily-tracking-row-${matchingRows[0].id}`)
      ?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [matchingRows]);

  const isLoading = fullQuery.isLoading || people.isLoading;

  return (
    <div className="flex min-w-[980px] flex-col gap-4">
      <div className="flex items-end justify-between gap-4">
        <div className="flex items-end gap-3">
          <PersonSelect
            people={people.people}
            selectedPersonId={selectedPersonId}
            setSelectedPersonId={setSelectedPersonId}
          />
          <DateSelect date={selectedDate} setDate={setSelectedDate} />
          <Button
            variant="outline"
            onClick={refreshDelta}
            disabled={!selectedPersonId || !selectedDateString || isRefreshing}
          >
            {isRefreshing ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <RefreshCw className="mr-2 h-4 w-4" />
            )}
            Обновить
          </Button>
        </div>
        {isLoading && <Loader2 className="h-5 w-5 animate-spin text-gray-400" />}
      </div>

      {!selectedPersonId ? (
        <div className="rounded-lg border border-dashed p-8 text-center text-muted-foreground">
          Выберите менеджера или водителя для Daily Tracking.
        </div>
      ) : (
        <>
          <DailyTrackingMap
            plans={plans}
            geopoints={geopoints}
            currentGeopoint={currentGeopoint}
            trackingManager={trackingManager}
            timeline={timeline}
            activeRowId={activeRowId}
            activePlanId={activePlanId}
            setActivePlanId={setActivePlanId}
          />
          <TimelineTable
            rows={timeline}
            activeRowId={activeRowId}
            activePlanId={activePlanId}
            setActiveRowId={setActiveRowId}
          />
          {snapshot && plans.length > 0 && geopoints.length === 0 && (
            <div className="text-sm text-muted-foreground">
              Геоточки за выбранный день не записаны. На карте отображены только
              планы.
            </div>
          )}
          {snapshot && plans.length === 0 && geopoints.length > 0 && (
            <div className="text-sm text-muted-foreground">
              На выбранный день нет назначенных планов. На карте отображен
              маршрут по геоточкам.
            </div>
          )}
        </>
      )}
    </div>
  );
};

const PersonSelect = ({
  people,
  selectedPersonId,
  setSelectedPersonId,
}: {
  people: Manager[];
  selectedPersonId?: string;
  setSelectedPersonId: (id: string | undefined) => void;
}) => {
  return (
    <div className="flex w-72 flex-col gap-1">
      <Label>Менеджер / водитель</Label>
      <Select
        value={selectedPersonId ?? ""}
        onValueChange={(value) => setSelectedPersonId(value || undefined)}
      >
        <SelectTrigger>
          <SelectValue placeholder="Выберите" />
        </SelectTrigger>
        <SelectContent>
          {people.map((person) => (
            <SelectItem key={person.id} value={person.id}>
              {managerFullName(person)} {person.is_driver ? "(водитель)" : ""}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

const DateSelect = ({
  date,
  setDate,
}: {
  date: Date;
  setDate: (date: Date) => void;
}) => {
  return (
    <div className="flex flex-col gap-1">
      <Label>Дата</Label>
      <Popover>
        <PopoverTrigger asChild>
          <Button variant="outline" className="w-44 justify-start font-normal">
            <CalendarIcon className="mr-2 h-4 w-4" />
            {date.toLocaleDateString("ru-RU")}
          </Button>
        </PopoverTrigger>
        <PopoverContent align="start" className="w-auto p-0">
          <Calendar
            mode="single"
            selected={date}
            onSelect={(newDate) => newDate && setDate(newDate)}
          />
        </PopoverContent>
      </Popover>
    </div>
  );
};

const DailyTrackingMap = ({
  plans,
  geopoints,
  currentGeopoint,
  trackingManager,
  timeline,
  activeRowId,
  activePlanId,
  setActivePlanId,
}: {
  plans: Plan[];
  geopoints: ManagerGeoPoint[];
  currentGeopoint: ManagerGeoPoint | null;
  trackingManager?: DailyTrackingManager;
  timeline: DailyTrackingTimelineRow[];
  activeRowId?: string;
  activePlanId?: string;
  setActivePlanId: (planId: string | undefined) => void;
}) => {
  const [selectedCity, setSelectedCity] = useState<CityKey>(DEFAULT_CITY);
  const cityConfig = CITIES[selectedCity];
  const mapElementRef = useRef<HTMLDivElement | null>(null);
  const ymaps = useYMaps([
    "Map",
    "Placemark",
    "Polyline",
    "Circle",
    "control.ZoomControl",
    "geoObject.addon.hint",
  ]);
  const [mapInstance, setMapInstance] = useState<ymaps.Map>();
  const activeRow = timeline.find((row) => row.id === activeRowId);
  const activeInsidePlanId =
    activeRow?.type === "inside_plan" ? activeRow.plan_id : undefined;
  const highlightedPlanId = activeInsidePlanId ?? activePlanId;

  useEffect(() => {
    if (!ymaps || !mapElementRef.current || mapInstance) return;

    const map = new ymaps.Map(mapElementRef.current, {
      center: cityConfig.center,
      zoom: cityConfig.zoom,
      controls: ["zoomControl"],
    });
    setMapInstance(map);
  }, [ymaps, mapInstance, cityConfig.center, cityConfig.zoom]);

  useEffect(() => {
    if (!mapInstance) return;
    mapInstance.setCenter(cityConfig.center);
    mapInstance.setZoom(cityConfig.zoom);
  }, [selectedCity, mapInstance, cityConfig.center, cityConfig.zoom]);

  useEffect(() => {
    if (!ymaps || !mapInstance) return;

    mapInstance.geoObjects.removeAll();
    const geopointsById = new Map(geopoints.map((point) => [point.id, point]));

    drawFullRoute(ymaps, mapInstance, geopoints);
    drawTimelineSegments(ymaps, mapInstance, timeline, geopointsById, activeRowId);
    drawActivePlanCircle(ymaps, mapInstance, plans, activeInsidePlanId);
    drawDepotMarker(ymaps, mapInstance, trackingManager);

    plans.forEach((plan) => {
      if (plan.client.is_hidden_on_map) return;
      const isHighlighted = highlightedPlanId === plan.id;
      const placemark = new ymaps.Placemark(
        [Number(plan.client.address.lat), Number(plan.client.address.lon)],
        { hintContent: plan.client.name },
        {
          iconLayout: "default#image",
          iconImageHref: getIconColored(
            isPlanAShipment(plan) ? "truck" : "woman",
            isHighlighted ? "#2563eb" : "#ef4444",
          ),
          iconImageSize: isHighlighted ? [48, 48] : [40, 40],
          iconImageOffset: isHighlighted ? [-24, -24] : [-20, -20],
          zIndex: isHighlighted ? 20 : 10,
        },
      );
      // @ts-ignore
      placemark.events.add("click", () => setActivePlanId(plan.id));
      mapInstance.geoObjects.add(placemark);
    });

    if (currentGeopoint) {
      if (currentGeopoint.accuracy && currentGeopoint.accuracy > 0) {
        const accuracyCircle = new ymaps.Circle(
          [
            [currentGeopoint.latitude, currentGeopoint.longitude],
            currentGeopoint.accuracy,
          ],
          {},
          {
            fillColor: "#dc26261f",
            strokeColor: "#dc2626",
            strokeOpacity: 0.45,
            strokeWidth: 2,
          },
        );
        mapInstance.geoObjects.add(accuracyCircle);
      }

      const placemark = new ymaps.Placemark(
        [currentGeopoint.latitude, currentGeopoint.longitude],
        { hintContent: geopointHint(currentGeopoint) },
        {
          preset: "islands#redCircleDotIcon",
          iconColor: "#dc2626",
          zIndex: 30,
        },
      );
      mapInstance.geoObjects.add(placemark);
    }
  }, [
    ymaps,
    mapInstance,
    plans,
    geopoints,
    currentGeopoint,
    trackingManager,
    timeline,
    activeRowId,
    activePlanId,
    activeInsidePlanId,
    highlightedPlanId,
    setActivePlanId,
  ]);

  return (
    <div className="relative h-[560px] overflow-hidden rounded-lg border">
      <div className="absolute left-2 top-2 z-10">
        <Tabs
          value={selectedCity}
          onValueChange={(value: string) => setSelectedCity(value as CityKey)}
        >
          <TabsList>
            <TabsTrigger value="almaty">Алматы</TabsTrigger>
            <TabsTrigger value="astana">Астана</TabsTrigger>
          </TabsList>
        </Tabs>
      </div>
      <div ref={mapElementRef} className="h-full w-full" />
    </div>
  );
};

const TimelineTable = ({
  rows,
  activeRowId,
  activePlanId,
  setActiveRowId,
}: {
  rows: DailyTrackingTimelineRow[];
  activeRowId?: string;
  activePlanId?: string;
  setActiveRowId: (id: string | undefined) => void;
}) => {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-40">Тип</TableHead>
          <TableHead>Маршрут</TableHead>
          <TableHead className="w-56">Время</TableHead>
          <TableHead className="w-40">Длительность</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {rows.map((row) => (
          <TableRow
            key={row.id}
            id={`daily-tracking-row-${row.id}`}
            className={cn(
              "cursor-pointer",
              activeRowId === row.id && "bg-blue-50",
              activePlanId && rowTouchesPlan(row, activePlanId) && "bg-blue-100",
            )}
            onMouseEnter={() => setActiveRowId(row.id)}
            onMouseLeave={() => setActiveRowId(undefined)}
            onClick={() => setActiveRowId(row.id)}
          >
            <TableCell>{row.type_label}</TableCell>
            <TableCell>{row.route}</TableCell>
            <TableCell>
              {formatTime(row.start_at)} - {formatTime(row.end_at)}
            </TableCell>
            <TableCell>{formatDuration(row.duration_seconds)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
      {rows.length === 0 && <TableCaption>Нет сегментов</TableCaption>}
    </Table>
  );
};

const useTrackingPeople = () => {
  const managersQuery = useManagersQuery();
  const driversQuery = useDriversQuery();

  const people = useMemo(() => {
    const byId = new Map<string, Manager>();
    [...(managersQuery.data?.data ?? []), ...(driversQuery.data?.data ?? [])].forEach(
      (person) => byId.set(person.id, person),
    );
    return Array.from(byId.values()).sort((a, b) => a.name.localeCompare(b.name));
  }, [managersQuery.data, driversQuery.data]);

  return {
    people,
    isLoading: managersQuery.isLoading || driversQuery.isLoading,
  };
};

const mergeGeopoints = (
  current: ManagerGeoPoint[],
  incoming: ManagerGeoPoint[],
) => {
  const byId = new Map(current.map((point) => [point.id, point]));
  incoming.forEach((point) => byId.set(point.id, point));
  return Array.from(byId.values()).sort(
    (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime(),
  );
};

const isToday = (date: Date) => {
  return date.toDateString() === new Date().toDateString();
};

const rowTouchesPlan = (row: DailyTrackingTimelineRow, planId: string) => {
  return (
    row.plan_id === planId || row.from_plan_id === planId || row.to_plan_id === planId
  );
};

const drawFullRoute = (
  ymaps: typeof globalThis.ymaps,
  mapInstance: ymaps.Map,
  geopoints: ManagerGeoPoint[],
) => {
  if (geopoints.length < 2) return;

  const polyline = new ymaps.Polyline(
    geopoints.map((point) => [point.latitude, point.longitude]),
    {},
    {
      strokeColor: "#94a3b8",
      strokeOpacity: 0.7,
      strokeWidth: 3,
    },
  );
  mapInstance.geoObjects.add(polyline);
};

const drawTimelineSegments = (
  ymaps: typeof globalThis.ymaps,
  mapInstance: ymaps.Map,
  timeline: DailyTrackingTimelineRow[],
  geopointsById: Map<string, ManagerGeoPoint>,
  activeRowId?: string,
) => {
  timeline
    .filter((row) => row.type === "travel")
    .forEach((row, index, rows) => {
      const coordinates = row.geopoint_ids
        .map((id) => geopointsById.get(id))
        .filter(Boolean)
        .map((point) => [point!.latitude, point!.longitude]);

      if (coordinates.length < 2) return;

      const color = getSegmentColor(index, rows.length);
      const hasActiveRow = Boolean(activeRowId);
      const isActiveRow = activeRowId === row.id;
      const polyline = new ymaps.Polyline(
        coordinates,
        {},
        {
          strokeColor: hasActiveRow && !isActiveRow ? "#94a3b8" : color,
          strokeOpacity: hasActiveRow && !isActiveRow ? 0.45 : 0.95,
          strokeWidth: isActiveRow ? 7 : 5,
        },
      );
      mapInstance.geoObjects.add(polyline);
    });
};

const drawActivePlanCircle = (
  ymaps: typeof globalThis.ymaps,
  mapInstance: ymaps.Map,
  plans: Plan[],
  planId?: string | null,
) => {
  if (!planId) return;

  const plan = plans.find((item) => item.id === planId);
  if (!plan) return;

  const circle = new ymaps.Circle(
    [[Number(plan.client.address.lat), Number(plan.client.address.lon)], 100],
    {},
    {
      fillColor: "#2563eb22",
      strokeColor: "#2563eb",
      strokeOpacity: 0.9,
      strokeWidth: 2,
    },
  );
  mapInstance.geoObjects.add(circle);
};

const drawDepotMarker = (
  ymaps: typeof globalThis.ymaps,
  mapInstance: ymaps.Map,
  manager?: DailyTrackingManager,
) => {
  if (!manager?.depot_lat || !manager?.depot_lon) return;

  const placemark = new ymaps.Placemark(
    [manager.depot_lat, manager.depot_lon],
    { hintContent: "Дом" },
    {
      iconLayout: "default#image",
      iconImageHref: getHouseIcon("#16a34a"),
      iconImageSize: [38, 38],
      iconImageOffset: [-19, -19],
      zIndex: 25,
    },
  );
  mapInstance.geoObjects.add(placemark);
};

const getHouseIcon = (color: string) => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24" fill="#000000"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" stroke="#ffffff" stroke-width="1"/></svg>`;
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg.replace("#000000", color))}`;
};

const geopointHint = (geopoint: ManagerGeoPoint) => {
  return `
    <div>
      <div>Время: ${formatTime(geopoint.created_at)}</div>
      <div>Точность: ${formatMeters(geopoint.accuracy)}</div>
      <div>Скорость: ${formatSpeed(geopoint.speed)}</div>
      <div>Направление: ${formatDegrees(geopoint.heading)}</div>
    </div>
  `;
};

const formatMeters = (value: number | null) => {
  return value === null ? "-" : `${Math.round(value)} м`;
};

const formatSpeed = (value: number | null) => {
  return value === null ? "-" : `${value.toFixed(1)} м/с`;
};

const formatDegrees = (value: number | null) => {
  return value === null ? "-" : `${Math.round(value)}°`;
};

const parseBackendUtcDate = (date: string) => {
  const hasTimezone = /(?:Z|[+-]\d{2}:?\d{2})$/.test(date);
  return new Date(hasTimezone ? date : `${date}Z`);
};

const formatTime = (date: string) => {
  return new Intl.DateTimeFormat("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    timeZone: APP_TIME_ZONE,
  }).format(parseBackendUtcDate(date));
};

const formatDuration = (seconds: number) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const restSeconds = seconds % 60;

  if (hours > 0) return `${hours}ч ${minutes}м`;
  if (minutes > 0) return `${minutes}м ${restSeconds}с`;
  return `${restSeconds}с`;
};

const getSegmentColor = (index: number, length: number) => {
  return Color.hsl((index / Math.max(length, 1)) * 359, 75, 48).hex();
};

const getIconColored = (iconType: "truck" | "woman", color: string) => {
  let svg;

  switch (iconType) {
    case "truck":
      svg = `<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M19.5 8H17V6c0-1.1-.9-2-2-2H3c-1.1 0-2 .9-2 2v9c0 1.1.9 2 2 2 0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h1c.55 0 1-.45 1-1v-3.33c0-.43-.14-.85-.4-1.2L20.3 8.4c-.19-.25-.49-.4-.8-.4zM6 18c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm13.5-8.5l1.96 2.5H17V9.5h2.5zM18 18c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z" stroke="#555" stroke-width=".5"/></svg>`;
      break;
    case "woman":
    default:
      svg = `<svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><g><rect fill="none" height="24" width="24"/><rect fill="none" height="24" width="24"/></g><g><circle cx="12" cy="4" r="2" stroke="#555"/><path d="M16.45,14.63l-2.52-6.32c-0.32-0.79-1.08-1.3-1.94-1.31c-0.85,0-1.62,0.51-1.94,1.31l-2.52,6.32 C7.28,15.29,7.77,16,8.47,16H10v5c0,0.55,0.45,1,1,1h1h1c0.55,0,1-0.45,1-1v-5h1.53C16.23,16,16.72,15.29,16.45,14.63z" stroke="#555" stroke-width=".5"/></g></svg>`;
      break;
  }

  return `data:image/svg+xml;utf8,${encodeURIComponent(svg.replace("#000000", color))}`;
};

export default DailyTrackingTemplate;
