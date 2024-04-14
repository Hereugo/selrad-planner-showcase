import hull from "hull.js";
import { usePlans } from "../Plans/index.hooks";
import _, { map, set } from "lodash";
import { useManagers } from "@/components/molecules/plan-dialog-new/index.hooks";
import React, { useEffect, useRef, useState } from "react";
import { useYMaps } from "@pbe/react-yandex-maps";
import { formatClientName, managerFullName } from "@/lib/utils";
import Color from "color";
import { formatDate } from "date-fns";

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
  const [selectedManager, setSelectedManager] = useState<Manager | undefined>();
  const [selectedPlanId, setSelectedPlanId] = useState<
    Plan["id"] | undefined
  >();

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

    setSelectedPlanId(undefined);
    if (selectedManager) {
      clearMap(mapInstance);
      selectedManagerDisplay(
        mapInstance,
        plans,
        ymaps,
        selectedManager,
        selectedPlanId,
        setSelectedPlanId,
      );
    } else {
      clearMap(mapInstance);
      initailStateDisplay(mapInstance, plans, ymaps, setSelectedManager);
    }
  }, [plans, mapInstance, selectedManager]);

  return {
    plans,
    managers,
    mapElementRef,
    ymaps,
    selectedManager,
    setSelectedManager,
    selectedPlanId,
    setSelectedPlanId,
  };
};

const clearMap = (mapInstance: ymaps.Map) => {
  mapInstance.geoObjects.removeAll();
  mapInstance.balloon.close();
};

const initailStateDisplay = (
  mapInstance: ymaps.Map,
  plans: Plan[],
  ymaps: any,
  setSelectedManager: (manager: Manager) => void,
) => {
  // get unique clients in plans
  const clients = _.uniqBy(
    plans.map((plan) => plan.client),
    "addresses[0].id",
  );

  clients.forEach((client) => {
    const { lon, lat } = client.addresses[0];
    const clientPlacemark = new ymaps.Placemark(
      [lat, lon],
      {
        // hintContent: client.name
      },
      {
        preset: "islands#circleDotIcon",
        iconColor: "#ff0000",
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

      const managerPlacemark = new ymaps.Placemark(
        [managerLat, managerLon],
        {
          hintContent: managerFullName(manager),
        },
        {
          // preset: "islands#circleDotIcon",
          iconLayout: "default#image",
          iconImageHref: `/human.svg`,
          iconImageSize: [20, 20],
          iconImageOffset: [-10, -10],
        },
      );

      managerPlacemark.events.add("click", (e: any) => {
        e.preventDefault();
        setSelectedManager(manager);
      });

      mapInstance.geoObjects.add(managerPlacemark);
    });

    clientPlacemark.events.add("click", (e: any) => {
      e.preventDefault();
      mapInstance.balloon.open([lat, lon], {
        contentHeader: formatClientName(client.name),
        contentBody: `
                    Тут ${clientPlans.length} план, ${managers.length} менеджер
                    <ul class="list-disc">
                        ${clientPlans.map((plan) => `<li> • ${formatDate(plan.assigned_date, "dd/MM/yyyy")}</li>`).join("")}
                    </ul>`,
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
  selectedPlanId: Plan["id"] | undefined,
  setSelectedPlan: React.Dispatch<React.SetStateAction<Plan["id"] | undefined>>,
) => {
  // get unique clients in plans
  const clients = _.uniqBy(
    plans.map((plan) => plan.client),
    "addresses[0].id",
  );

  clients.forEach((client) => {
    // for every client get all managers that are working there
    const clientPlans = plans.filter((plan) => plan.client.id === client.id);
    const clientPlanManagers = _.flatMap(
      clientPlans.map((plan) => plan.managers),
    );
    const managers = _.uniqBy(clientPlanManagers, "id");

    const { lon, lat } = client.addresses[0];
    const clientPlacemark = new ymaps.Placemark(
      [lat + rand(), lon + rand()],
      {
        // hintContent: client.name
      },
      {
        preset: "islands#circleDotIcon",
        iconColor: managers.map((m) => m.id).includes(manager.id)
          ? "#ff0000"
          : "#00000010",
        zIndex: managers.map((m) => m.id).includes(manager.id) ? 1000 : 100,
      },
    );

    clientPlacemark.events.add("click", (e: any) => {
      e.preventDefault();
      setSelectedPlan(clientPlans[0].id);
    });

    mapInstance.geoObjects.add(clientPlacemark);
  });

  // only plans where manager is working
  const managerPlans = plans.filter((plan) =>
    plan.managers.some((m) => m.id === manager.id),
  );

  // group by day
  const groupedPlans = _.groupBy(managerPlans, (plan) => plan.assigned_date);

  Object.entries(groupedPlans).forEach(([date, plans]) => {
    // draw a convex hull around the plans
    const hullPoints = plans.map((plan) => [
      plan.client.addresses[0].lat,
      plan.client.addresses[0].lon,
    ]);

    const hullPolygon = new ymaps.Polygon(
      [hull(hullPoints)],
      {
        hintContent: "Менеджер",
      },
      {
        fillColor: "#00000000",
        strokeColor: "#ff0000",
        strokeWidth: 2,
        opacity: 0.5,
      },
    );

    mapInstance.geoObjects.add(hullPolygon);
  });
};

const rand = () => Math.random() * 0.0001 - 0.00005;
