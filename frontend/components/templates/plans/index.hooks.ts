import { usePlansQuery } from "@/lib/backend/plans";

export const usePlans = () => {
    const { data, error, isLoading } = usePlansQuery();

    const plans = (data?.data || [])
        .sort((a, b) => {
            let diff = new Date(b.assigned_date).getTime() - new Date(a.assigned_date).getTime();
            if (diff === 0) {
                return a.client.name.localeCompare(b.client.name);
            }
            return -diff;
        });

    return {
        plans,
        error,
        isLoading
    };
}