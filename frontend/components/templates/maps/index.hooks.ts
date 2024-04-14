import hull from "hull.js";
import { usePlans } from "../Plans/index.hooks";
import _ from "lodash";
import { useManagers } from "@/components/molecules/plan-dialog-new/index.hooks";
import { useEffect, useRef, useState } from "react";
import { useYMaps } from "@pbe/react-yandex-maps";
import { formatClientName, managerFullName } from "@/lib/utils";
import Color from "color";
import { formatDate } from "date-fns";

// HSV contrast colors
const pinColors = [
  "#1f77b4",
  "#ff7f0e",
  "#2ca02c",
  "#d62728",
  "#9467bd",
  "#8c564b",
  "#e377c2",
  "#7f7f7f",
  "#bcbd22",
  "#17becf",
];

export const useMaps = () => {
  const { plans } = usePlans();
  const { managers } = useManagers();
  const mapElementRef = useRef(null);
  const ymaps = useYMaps([
    "Map",
    "Placemark",
    "Polygon",
    "geoObject.addon.balloon",
    "geoObject.addon.hint",
    "control.ZoomControl",
  ]);
  const [mapInstance, setMapInstance] = useState<ymaps.Map>();

  const [selectedManager, setSelectedManager] = useState<Manager | null>(null);

  // initial creation of the map
  useEffect(() => {
    if (!ymaps || !mapElementRef.current) return;
    const mapCenter = [43.25, 76.95];

    const map = new ymaps.Map(mapElementRef.current, {
      center: mapCenter,
      zoom: 12.5,
      controls: ["zoomControl"],
    });

    if (map && !mapInstance) {
      setMapInstance(map);
    }
  }, [ymaps, mapElementRef.current]);

  // further manipulation of the map with controls
  useEffect(() => {
    if (!ymaps || !mapElementRef.current || !mapInstance) return;

    if (selectedManager) {
      clearMap(mapInstance);
      selectedManagerDisplay(mapInstance, plans, ymaps, selectedManager);
    } else {
      clearMap(mapInstance);
      initailStateDisplay(mapInstance, plans, ymaps);
    }
  }, [plans, mapInstance, selectedManager]);

  return {
    plans,
    managers,
    mapElementRef,
    ymaps,
    setSelectedManager,
  };
};

const clearMap = (mapInstance: ymaps.Map) => {
  mapInstance.geoObjects.removeAll();
};

const initailStateDisplay = (
  mapInstance: ymaps.Map,
  plans: Plan[],
  ymaps: any,
) => {
  // get unique clients in plans
  const clients = _.uniqBy(
    plans.map((plan) => plan.client),
    "addresses[0].id",
  );

  clients.map((client) => {
    const { lon, lat } = client.addresses[0];
    const clientPlacemark = new ymaps.Placemark(
      [lat, lon],
      {
        // hintContent: client.name
      },
      {
        preset: "islands#circleDotIcon",
        iconColor: "red",
        zIndex: 1000,
      },
    );

    // for every client get all managers that are working there
    const clientPlans = plans.filter((plan) => plan.client.id === client.id);
    const clientPlanManagers = _.flatMap(
      clientPlans.map((plan) => plan.managers),
    );

    const managers = _.uniqBy(clientPlanManagers, "id");
    const n = managers.length;
    const r = 0.0001;

    // position in the circle around the client
    managers.map((manager, index) => {
      const managerLon = lon + r * Math.cos((2 * Math.PI * index) / n);
      const managerLat = lat + r * Math.sin((2 * Math.PI * index) / n);

      console.log(
        managerFullName(manager),
        [managerLat, managerLon],
        [lon, lat],
      );

      const managerPlacemark = new ymaps.Placemark(
        [managerLat, managerLon],
        {
          hintContent: managerFullName(manager),
        },
        {
          preset: "islands#circleDotIcon",
          iconColor: "blue",
        },
      );

      mapInstance.geoObjects.add(managerPlacemark);
    });

    clientPlacemark.events.add("click", (e: any) => {
      e.preventDefault();
      mapInstance.balloon.open([lat, lon], {
        contentHeader: formatClientName(client.name),
        contentBody: `Тут ${clientPlans.length} план, ${managers.length} менеджер`,
        contentFooter: client.addresses[0].street,
      });
    });

    mapInstance.geoObjects.add(clientPlacemark);
  });
};

const selectedManagerDisplay = (
  mapInstance: ymaps.Map,
  plans: Plan[],
  ymaps: any,
  manager: Manager,
) => {
  const managerPlans = plans.filter((plan) =>
    plan.managers.find((m) => m.id === manager.id),
  );
  const uniqueDates = _.uniq(managerPlans.map((plan) => plan.assigned_date));
  const n = uniqueDates.length;

  managerPlans.map((plan, i) => {
    const { lon, lat } = plan.client.addresses[0];
    const dateInd = uniqueDates.findIndex(
      (date) => date === plan.assigned_date,
    );
    const placemark = new ymaps.Placemark(
      [lat, lon],
      {
        hintContent: `${formatDate(plan.assigned_date, "dd.MM.yyyy")}`,
      },
      {
        preset: "islands#circleDotIcon",
        iconColor: Color.hsl((dateInd / n) * 100, 75, 50).hex(),
      },
    );
    mapInstance.geoObjects.add(placemark);
  });
};
