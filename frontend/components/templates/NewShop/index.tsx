"use client";

import axios from "axios";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { useYMaps } from "@pbe/react-yandex-maps";
import { Check, ChevronsUpDown, Loader2, MapPin, Plus } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { useToast } from "@/components/ui/use-toast";
import {
  useClientCreateMutation,
  useMetaClientsQuery,
} from "@/lib/backend/clients";
import { parse2gisLink, Parsed2gisPoint } from "@/lib/geo/parse2gisLink";
import { useViewFeature } from "@/lib/hooks/useViewFeature";
import { cn } from "@/lib/utils";

const ALMATY_CENTER: [number, number] = [43.238949, 76.889709];
const LINK_PARSE_WARNING =
  "Не удалось определить координаты из ссылки. Выберите точку на карте вручную.";

type MetaClientChoice =
  | { type: "existing"; id: string }
  | { type: "new"; name: string };

const NewShopTemplate = () => {
  const router = useRouter();
  const { toast } = useToast();
  const viewFeature = useViewFeature();
  const { data: metaClientsData } = useMetaClientsQuery();
  const createShopMutation = useClientCreateMutation();

  const [shopName, setShopName] = useState("");
  const [address, setAddress] = useState("");
  const [twogisLink, setTwogisLink] = useState("");
  const [linkWarning, setLinkWarning] = useState<string>();
  const [metaClientChoice, setMetaClientChoice] = useState<MetaClientChoice>();
  const [selectedPoint, setSelectedPoint] = useState<Parsed2gisPoint>();
  const [mapFocusVersion, setMapFocusVersion] = useState(0);

  const metaClients = (metaClientsData?.data ?? []).sort((a, b) =>
    a.name.localeCompare(b.name),
  );

  const isValid =
    shopName.trim() && address.trim() && metaClientChoice && selectedPoint;

  const handle2gisLinkChange = (value: string) => {
    setTwogisLink(value);

    if (!value.trim()) {
      setLinkWarning(undefined);
      return;
    }

    const parsedPoint = parse2gisLink(value);
    if (parsedPoint) {
      setSelectedPoint(parsedPoint);
      setMapFocusVersion((version) => version + 1);
      setLinkWarning(undefined);
      return;
    }

    if (value.trim().length > 10) {
      setLinkWarning(LINK_PARSE_WARNING);
    }
  };

  const handleSubmit = () => {
    if (!isValid || !selectedPoint || !metaClientChoice) {
      toast({
        title: "Ошибка",
        description: "Заполните название, клиента, адрес и точку на карте",
      });
      return;
    }

    createShopMutation.mutate({
      name: shopName.trim(),
      meta_client_id:
        metaClientChoice.type === "existing" ? metaClientChoice.id : undefined,
      meta_client_name:
        metaClientChoice.type === "new" ? metaClientChoice.name.trim() : undefined,
      address: {
        street: address.trim(),
        twogis_link: twogisLink.trim() || undefined,
        lat: selectedPoint.lat,
        lon: selectedPoint.lon,
      },
    });
  };

  useEffect(() => {
    if (!createShopMutation.isSuccess) return;

    toast({
      title: "Успех",
      description: "Магазин создан",
    });
    router.push("/");
  }, [createShopMutation.isSuccess, router, toast]);

  useEffect(() => {
    if (!createShopMutation.isError) return;

    toast({
      title: "Ошибка при создании магазина",
      description: axios.isAxiosError(createShopMutation.error)
        ? createShopMutation.error.response?.data?.error ||
          createShopMutation.error.response?.data?.non_field_errors?.[0] ||
          "Проверьте данные и попробуйте снова"
        : "Проверьте данные и попробуйте снова",
    });
  }, [createShopMutation.isError, createShopMutation.error, toast]);

  if (viewFeature.isLoading) {
    return <div>Загрузка...</div>;
  }

  if (!viewFeature.canCreateShop) {
    return <div>У вас нет прав на создание магазинов</div>;
  }

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold">Новый магазин</h1>
        <p className="text-sm text-muted-foreground">
          Создайте магазин, выберите клиента и отметьте точку на карте.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[22rem,1fr]">
        <div className="flex flex-col gap-4 rounded-lg border bg-background p-4">
          <div className="flex flex-col gap-2">
            <Label htmlFor="shop_name">Название магазина</Label>
            <Input
              id="shop_name"
              value={shopName}
              onChange={(event) => setShopName(event.target.value)}
              placeholder="Например: Magnum Абая"
            />
          </div>

          <div className="flex flex-col gap-2">
            <Label htmlFor="meta_client">Клиент</Label>
            <MetaClientPicker
              id="meta_client"
              metaClients={metaClients}
              choice={metaClientChoice}
              onChange={setMetaClientChoice}
            />
          </div>

          <div className="flex flex-col gap-2">
            <Label htmlFor="address">Адрес</Label>
            <Input
              id="address"
              value={address}
              onChange={(event) => setAddress(event.target.value)}
              placeholder="Город, улица, дом"
            />
          </div>

          <div className="flex flex-col gap-2">
            <Label htmlFor="twogis_link">Ссылка 2GIS</Label>
            <Input
              id="twogis_link"
              value={twogisLink}
              onChange={(event) => handle2gisLinkChange(event.target.value)}
              placeholder="https://2gis.kz/..."
            />
            {linkWarning && (
              <p className="text-sm text-amber-600">{linkWarning}</p>
            )}
          </div>

          <Button
            disabled={!isValid || createShopMutation.isLoading}
            onClick={handleSubmit}
            className="mt-2"
          >
            {createShopMutation.isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              "Создать магазин"
            )}
          </Button>
        </div>

        <div className="flex min-h-[34rem] flex-col gap-3 rounded-lg border bg-background p-4">
          <div>
            <Label>Местоположение</Label>
            <p className="text-sm text-muted-foreground">
              Нажмите на карту или вставьте ссылку 2GIS. Маркер можно
              перетащить.
            </p>
          </div>
          <ShopLocationMap
            point={selectedPoint}
            focusVersion={mapFocusVersion}
            onChange={setSelectedPoint}
          />
          {selectedPoint ? (
            <div className="grid gap-2 text-sm text-muted-foreground sm:grid-cols-2">
              <div>Широта: {selectedPoint.lat.toFixed(6)}</div>
              <div>Долгота: {selectedPoint.lon.toFixed(6)}</div>
            </div>
          ) : (
            <div className="text-sm text-muted-foreground">
              Точка на карте не выбрана
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

interface MetaClientPickerProps {
  id: string;
  metaClients: MetaClient[];
  choice?: MetaClientChoice;
  onChange: (choice: MetaClientChoice | undefined) => void;
}

const MetaClientPicker = ({
  id,
  metaClients,
  choice,
  onChange,
}: MetaClientPickerProps) => {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");

  const selectedLabel =
    choice?.type === "existing"
      ? metaClients.find((metaClient) => metaClient.id === choice.id)?.name
      : choice?.name;
  const canCreate = search.trim().length > 0;

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          id={id}
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className={cn(
            "w-full justify-between font-normal",
            !selectedLabel && "text-muted-foreground",
          )}
        >
          <span className="truncate">
            {selectedLabel || "Выбрать клиента..."}
          </span>
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[22rem] p-0 shadow-md">
        <Command>
          <CommandInput
            placeholder="Найти клиента..."
            value={search}
            onValueChange={setSearch}
          />
          <CommandList>
            <CommandEmpty>Клиент не найден</CommandEmpty>
            <CommandGroup>
              {metaClients.map((metaClient) => (
                <CommandItem
                  className="cursor-pointer"
                  key={metaClient.id}
                  value={metaClient.name}
                  onSelect={() => {
                    onChange({ type: "existing", id: metaClient.id });
                    setOpen(false);
                  }}
                >
                  <Check
                    className={cn(
                      "mr-2 h-4 w-4",
                      choice?.type === "existing" && choice.id === metaClient.id
                        ? "opacity-100"
                        : "opacity-0",
                    )}
                  />
                  {metaClient.name}
                </CommandItem>
              ))}
              {canCreate && (
                <CommandItem
                  className="cursor-pointer"
                  value={`Создать клиента ${search.trim()}`}
                  onSelect={() => {
                    onChange({ type: "new", name: search.trim() });
                    setOpen(false);
                  }}
                >
                  <Plus className="mr-2 h-4 w-4" />
                  Создать клиента &quot;{search.trim()}&quot;
                </CommandItem>
              )}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
};

interface ShopLocationMapProps {
  point?: Parsed2gisPoint;
  focusVersion: number;
  onChange: (point: Parsed2gisPoint) => void;
}

const ShopLocationMap = ({
  point,
  focusVersion,
  onChange,
}: ShopLocationMapProps) => {
  const mapElementRef = useRef<HTMLDivElement | null>(null);
  const mapInstanceRef = useRef<ymaps.Map | null>(null);
  const placemarkRef = useRef<ymaps.Placemark | null>(null);
  const appliedFocusVersionRef = useRef(focusVersion);
  const ymaps = useYMaps(["Map", "Placemark", "control.ZoomControl"]);

  useEffect(() => {
    if (!ymaps || !mapElementRef.current || mapInstanceRef.current) return;

    const map = new ymaps.Map(mapElementRef.current, {
      center: ALMATY_CENTER,
      zoom: 12,
      controls: ["zoomControl"],
    });

    map.events.add("click", (event: any) => {
      const coords = event.get("coords") as [number, number];
      onChange({ lat: coords[0], lon: coords[1] });
    });

    mapInstanceRef.current = map;

    return () => {
      map.destroy();
      mapInstanceRef.current = null;
    };
  }, [ymaps, onChange]);

  useEffect(() => {
    if (!ymaps || !mapInstanceRef.current) return;

    if (!point) {
      mapInstanceRef.current.geoObjects.removeAll();
      placemarkRef.current = null;
      return;
    }

    if (focusVersion !== appliedFocusVersionRef.current) {
      mapInstanceRef.current.setCenter([point.lat, point.lon], 16);
      appliedFocusVersionRef.current = focusVersion;
    } else {
      mapInstanceRef.current.setCenter([point.lat, point.lon]);
    }
    mapInstanceRef.current.geoObjects.removeAll();

    const placemark = new ymaps.Placemark(
      [point.lat, point.lon],
      {},
      { draggable: true },
    );

    placemark.events.add("dragend", () => {
      const coords = placemark.geometry?.getCoordinates() as [number, number];
      onChange({ lat: coords[0], lon: coords[1] });
    });

    mapInstanceRef.current.geoObjects.add(placemark);
    placemarkRef.current = placemark;
  }, [ymaps, point, focusVersion, onChange]);

  return (
    <div
      ref={mapElementRef}
      className="min-h-[28rem] flex-1 overflow-hidden rounded-md border"
    />
  );
};

export default NewShopTemplate;
