import { usePlans } from "../Plans/index.hooks";

export const useMaps = () => {
    const { plans } = usePlans();

    const mapCenter = plans.reduce((acc, plan) => {
        return [
            acc[0] + Number(plan.client.address.lat) / plans.length,
            acc[1] + Number(plan.client.address.lon) / plans.length,
        ];
    }, [0, 0]);

    const placeMarks = plans.map((plan) => {
        return {
            geometry: [plan.client.address.lat, plan.client.address.lon],
            properties: {
                hintContent: plan.client.address.street,
                balloonContent: plan.client.address.street,
            },
        };
    })

    return {
        mapCenter,
        placeMarks,
    };
}