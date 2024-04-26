import { usePlans } from "../Plans/index.hooks";
import _ from "lodash";
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
    options: {
      iconLayout: string;
      iconImageHref: string;
      iconImageSize: number[];
      iconImageOffset: number[];
    };
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
  const iconType =
    plan.shipment_cost !== undefined
      ? plan.shipment_cost > 0
        ? "truck"
        : "woman"
      : "marker";

  return {
    geometry: [
      Number(plan.client.address.lat) +
      getDisplacement(plan.created_at, false),
      Number(plan.client.address.lon) +
      getDisplacement(plan.created_at, true),
    ],
    properties: {
      // hintContent: plan.client.name,
      // balloonContent: planToBalloonHTML(plan),
    },
    onClick: callback,
    options: {
      iconLayout: "default#image",
      iconImageHref: getIconColored(iconType, color),
      iconImageSize: [40, 40],
      iconImageOffset: [-10, -10],
    },
  };
};

const planToBalloonHTML = (plan: Plan) => {
  return `
        <div>
            <h3 class="text-lg font-semibold">${plan.client.name}</h3>
            <p>Адрес: ${plan.client.address.street}</p>
        </div>
    `;
};

const getColor = (index: number, length: number) => {
  return Color.hsl((index / length) * 359, 75, 50).hex();
};

const getIconColored = (iconType: string, color: string) => {
  let svg;

  switch (iconType) {
    case "truck":
      svg = `<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M19.5 8H17V6c0-1.1-.9-2-2-2H3c-1.1 0-2 .9-2 2v9c0 1.1.9 2 2 2 0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h1c.55 0 1-.45 1-1v-3.33c0-.43-.14-.85-.4-1.2L20.3 8.4c-.19-.25-.49-.4-.8-.4zM6 18c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm13.5-8.5l1.96 2.5H17V9.5h2.5zM18 18c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z" stroke="#fff" stroke-width=".5"/></svg>`;
      break;
    case "woman":
      svg = `<svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><g><rect fill="none" height="24" width="24"/><rect fill="none" height="24" width="24"/></g><g><circle cx="12" cy="4" r="2" stroke="#fff"/><path d="M16.45,14.63l-2.52-6.32c-0.32-0.79-1.08-1.3-1.94-1.31c-0.85,0-1.62,0.51-1.94,1.31l-2.52,6.32 C7.28,15.29,7.77,16,8.47,16H10v5c0,0.55,0.45,1,1,1h1h1c0.55,0,1-0.45,1-1v-5h1.53C16.23,16,16.72,15.29,16.45,14.63z" stroke="#fff" stroke-width=".5"/></g></svg>`;
      break;
    case "marker":
    default:
      svg = `<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13C19 5.13 15.87 2 12 2zm0 9c-1.38 0-2.5-1.12-2.5-2.5S10.62 6 12 6s2.5 1.12 2.5 2.5S13.38 11 12 11z" stroke="#fff" stroke-width=".5"/></svg>`;
      break;
  }
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg.replace("#000000", color))}`;
};

const getDisplacement = (created_date: string, useCos: boolean) => {
  // pseudo random displacement
  // based on the created_date
  // has to be the same for the same date
  // but different for different dates
  // range is [-1e-4, 1e-4]
  const func = useCos ? Math.cos : Math.sin;
  const time = new Date(created_date).getTime();
  const rand = func(time / 3) * 1e-4;
  return rand;
};
