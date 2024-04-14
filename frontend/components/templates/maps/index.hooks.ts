import { usePlans } from "../Plans/index.hooks";
import _, { random } from "lodash";
import { useEffect, useRef, useState } from "react";
import { useYMaps } from "@pbe/react-yandex-maps";
import Color from "color";

export const useMaps = () => {
  const { plans, isLoading: isPlansLoading } = usePlans();
  const mapElementRef = useRef(null);
  const ymaps = useYMaps([
    "Map",
    "Placemark",
    "Polygon",
    "control.ZoomControl",
  ]);
  const [mapInstance, setMapInstance] = useState<ymaps.Map>();

  const [selectedPlanId, setSelectedPlanId] = useState<
    Plan["id"] | undefined
  >();
  const mapCenter = [43.238949, 76.889709];

  const plansByDay = _.groupBy(plans, "assigned_date");

  const placeMarks: {
    geometry: number[];
    properties: {};
    onClick: Function;
    options: { iconColor: string };
  }[] = [];

  const dayKeys = Object.keys(plansByDay);
  for (let i = 0; i < dayKeys.length; i++) {
    let day = dayKeys[i];
    let plans = plansByDay[day];

    for (let plan of plans) {
      placeMarks.push(
        planToPlaceMark(plan, getColor(i, dayKeys.length), () => {
          setSelectedPlanId((p) => (p !== plan.id ? plan.id : undefined));
        }),
      );
    }
  }

  // setup
  useEffect(() => {
    if (!ymaps || !mapElementRef.current) return;

    const map = new ymaps.Map(mapElementRef.current, {
      center: mapCenter,
      zoom: 12,
      controls: ["zoomControl"],
    });

    if (!mapInstance) setMapInstance(map);
  }, [ymaps, mapInstance, mapElementRef.current]);

  // drawing with data
  useEffect(() => {
    if (!ymaps || !mapElementRef.current) return;
    if (!mapInstance) return;
    clearMap(mapInstance);

    placeMarks.forEach((mark) => {
      const placemark = new ymaps.Placemark(
        mark.geometry,
        mark.properties,
        mark.options,
      );
      // @ts-ignore
      placemark.events.add("click", mark.onClick);
      mapInstance.geoObjects.add(placemark);
    });
  }, [plans, mapInstance, ymaps, placeMarks]);

  return {
    mapElementRef,
    selectedPlan: plans.filter((p) => p.id === selectedPlanId)[0] || undefined,
    setSelectedPlanId,
    isPlansLoading,
  };
};

const clearMap = (map: ymaps.Map) => {
  map.geoObjects.removeAll();
  map.balloon.close();
};

const planToPlaceMark = (plan: Plan, color: string, callback: Function) => {
  return {
    geometry: [
      Number(plan.client.addresses[0].lat) + random(-1e-5, 1e-5),
      Number(plan.client.addresses[0].lon) + random(-1e-5, 1e-5),
    ],
    properties: {
      // hintContent: plan.client.name,
      // balloonContent: planToBalloonHTML(plan),
    },
    onClick: callback,
    options: {
      iconColor: color,
    },
  };
};

const planToBalloonHTML = (plan: Plan) => {
  return `
        <div>
            <h3 class="text-lg font-semibold">${plan.client.name}</h3>
            <p>Адрес: ${plan.client.addresses[0].street}</p>
        </div>
    `;
};

const getColor = (index: number, length: number) => {
  return Color.hsl((index / length) * 100, 75, 50).hex();
};
