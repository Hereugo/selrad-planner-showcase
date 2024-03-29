import useFiltersContext from "@/components/molecules/side-bar/index.providers";
import { usePlansQuery } from "@/lib/backend/plans";

export const usePlans = () => {
    const { calendarRange, searchQuery } = useFiltersContext();

    const { data, error, isLoading } = usePlansQuery({
        date_after: calendarRange?.from
            ?.toLocaleDateString("ru-RU")
            .split(".")
            .reverse()
            .join("-"),
        date_before: calendarRange?.to
            ?.toLocaleDateString("ru-RU")
            .split(".")
            .reverse()
            .join("-"),
        search: searchQuery,
    });

    const plans = (data?.data || []).sort((a, b) => {
        let diff =
            new Date(b.assigned_date).getTime() - new Date(a.assigned_date).getTime();
        if (diff === 0) {
            return a.client.name.localeCompare(b.client.name);
        }
        return -diff;
    });

    return {
        plans,
        error,
        isLoading,
    };
};
