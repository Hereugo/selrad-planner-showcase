import hull from "hull.js";
import { usePlans } from "../Plans/index.hooks";
import _ from "lodash";
import { Polygon } from "@pbe/react-yandex-maps";

// HSV contrast colors
const colors = ['#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#8c564b',
    '#e377c2',
    '#7f7f7f',
    '#bcbd22',
    '#17becf'];


export const useMaps = () => {
    const { plans } = usePlans();

    const mapCenter = plans.reduce((acc, plan) => [
        acc[0] + Number(plan.client.address.lat) / plans.length,
        acc[1] + Number(plan.client.address.lon) / plans.length,
    ], [0, 0]);
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

        // Make polygons
        let dayCoordinates = plans.map((plan) => [
            Number(plan.client.address.lat),
            Number(plan.client.address.lon),
        ]);
        let polygonCoords = hull(dayCoordinates, 50);
        polygons.push({
            geometry: [polygonCoords],
            options: {
                fillColor: colors[i % colors.length] + "33",
                strokeColor: colors[i % colors.length],
                strokeWidth: 2,
            }
        });

        // Make placeMarks
        for (let plan of plans) {
            placeMarks.push({
                geometry: [
                    Number(plan.client.address.lat),
                    Number(plan.client.address.lon),
                ],
                properties: {
                    hintContent: plan.client.name,
                    balloonContent: plan.client.name,
                },
                options: {
                    iconColor: colors[i % colors.length],
                }
            });
        }
    }

    return {
        mapCenter,
        placeMarks,
        polygons,
    };
}