import hull from "hull.js";
import { usePlans } from "../plans/index.hooks";
import _ from "lodash";
import { Polygon } from "@pbe/react-yandex-maps";
import { useManagers } from "@/components/molecules/plan-dialog-new/index.hooks";

// HSV contrast colors
const colors = [
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

  const mapCenter = plans.reduce(
    (acc, plan) => [
      acc[0] + Number(plan.client.address.lat) / plans.length,
      acc[1] + Number(plan.client.address.lon) / plans.length,
    ],
    [0, 0],
  );
  if (plans.length === 0) {
    mapCenter[0] = 43.238949;
    mapCenter[1] = 76.889709;
  }

  const plansByDay = _.groupBy(plans, "assigned_date");

  const polygons = [];
  const placeMarks = [];

  for (let i = 0; i < Object.keys(plansByDay).length; i++) {
    let day = Object.keys(plansByDay)[i];
    let plans = plansByDay[day];

    // Make placeMarks
    for (let plan of plans) {
      placeMarks.push({
        geometry: [
          Number(plan.client.address.lat),
          Number(plan.client.address.lon),
        ],
        properties: {
          hintContent: plan.client.name,
          balloonContent: [
            `<b>${plan.assigned_date}</b>`,
            plan.client.name,
            plan.managers.map((m) => `<li>${m.first_name}</li>`).join("\n"),
            plan.worklist.map((w) => `<ul>${w.name}</ul>`).join("\n"),
            "<a href='#' class='text-blue-500'>Изменить</a>",
          ].join("<br/>"),
        },
        options: {
          iconColor: colors[i % colors.length],
        },
      });
    }

    // Make polygons
    for (let manager of managers) {
      const plansByManager = _.filter(plans, (plan, i) =>
        plan.managers.map((m) => m.id).includes(manager.id),
      );
      let managerCoordinates = plansByManager.map((plan) => [
        Number(plan.client.address.lat),
        Number(plan.client.address.lon),
      ]);

      if (managerCoordinates.length <= 1) continue;

      let polygonCoords = hull(managerCoordinates, 50);
      polygons.push({
        geometry: [polygonCoords],
        options: {
          fillColor: colors[i % colors.length] + "33",
          strokeColor: colors[i % colors.length],
          strokeWidth: 2,
        },
      });
    }
  }

  return {
    mapCenter,
    placeMarks,
    polygons,
  };
};
