import hull from "hull.js";
import { usePlans } from "../Plans/index.hooks";
import _, { random } from "lodash";
import { useManagers } from "@/components/molecules/plan-dialog-new/index.hooks";
import { useEffect, useRef, useState } from "react";
import { managerFullName } from "@/lib/utils";
import { useYMaps } from "@pbe/react-yandex-maps";

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
const edgeColors = [
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
  const mapRef = useRef(null);
  const ymaps = useYMaps(["Map", "Placemark", "Polygon"]);

  const [selectedPlanId, setSelectedPlanId] = useState<
    Plan["id"] | undefined
  >();
  const selectedPlan = plans.filter((p) => p.id === selectedPlanId)[0];
  const mapCenter = [43.238949, 76.889709];

  const plansByDay = _.groupBy(plans, "assigned_date");

  const placeMarks: {
    geometry: number[];
    properties: {};
    onClick: Function;
    options: { iconColor: string };
  }[] = [];

  for (let i = 0; i < Object.keys(plansByDay).length; i++) {
    let day = Object.keys(plansByDay)[i];
    let plans = plansByDay[day];

    for (let plan of plans) {
      placeMarks.push(
        planToPlaceMark(plan, pinColors[i % pinColors.length], () => {
          setSelectedPlanId((p) => (p !== plan.id ? plan.id : undefined));
        }),
      );
    }
  }

  useEffect(() => {
    if (!ymaps || !mapRef.current) return;

    const map = new ymaps.Map(mapRef.current, {
      center: mapCenter,
      zoom: 12,
      controls: [],
    });

    placeMarks.forEach((mark) => {
      const placemark = new ymaps.Placemark(
        mark.geometry,
        mark.properties,
        mark.options,
      );
      // @ts-ignore
      placemark.events.add("click", mark.onClick);
      map.geoObjects.add(placemark);
    });
  }, [ymaps]);

  return {
    mapRef,
    mapCenter,
    placeMarks,
    selectedPlan,
    setSelectedPlanId,
  };
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
