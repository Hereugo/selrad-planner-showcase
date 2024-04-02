import hull from "hull.js";
import { usePlans } from "../Plans/index.hooks";
import _, { random } from "lodash";
import { useManagers } from "@/components/molecules/plan-dialog-new/index.hooks";
import { useState } from "react";
import { managerFullName } from "@/lib/utils";
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

    const [selectedPlanId, setSelectedPlanId] = useState<
        Plan["id"] | undefined
    >();
    const selectedPlan = plans.filter((p) => p.id === selectedPlanId)[0];
    const mapCenter = [43.238949, 76.889709];

    const plansByDay = _.groupBy(plans, "assigned_date");

    const polygons = [];
    const placeMarks = [];

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

        for (let [idx, manager] of Object.entries(managers)) {
            polygons.push(
                ...managerPlansToPolygon(
                    plans,
                    manager,
                    edgeColors[Number(idx) % edgeColors.length],
                    (Number(idx) / managers.length) * 2e-3,
                ),
            );
        }
    }

    return {
        mapCenter,
        placeMarks,
        polygons,
        selectedPlan,
        setSelectedPlanId,
    };
};

const planToPlaceMark = (plan: Plan, color: string, callback: Function) => {
    return {
        geometry: [
            Number(plan.client.address.lat) + random(-1e-3, 1e-3),
            Number(plan.client.address.lon) + random(-1e-3, 1e-3),
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
            <p>Адрес: ${plan.client.address.street}</p>
        </div>
    `;
};

const managerPlansToPolygon = (
    dayPlans: Plan[],
    manager: Manager,
    color: string,
    displace = 0,
) => {
    const managerPlans = _.filter(dayPlans, (plan, _) =>
        plan.managers.map((m) => m.id).includes(manager.id),
    );
    const managerCoordinates = managerPlans.map((plan) => [
        Number(plan.client.address.lat) + displace,
        Number(plan.client.address.lon) + displace,
    ]);

    if (managerCoordinates.length <= 1) return [];

    const polygonCoords = hull(managerCoordinates, 50);
    return [
        {
            geometry: [polygonCoords],
            options: {
                fillColor: color + "10",
                strokeColor: color,
                strokeWidth: 1.5,
            },
            properties: {
                hintContent: managerFullName(manager),
            },
        },
    ];
};
