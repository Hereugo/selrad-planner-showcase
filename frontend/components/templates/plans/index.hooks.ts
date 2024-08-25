import useFiltersContext from "@/components/molecules/side-bar/index.providers";
import { usePlansQuery } from "@/lib/backend/plans";

export const usePlans = () => {
  const { calendarRange, searchQuery, managerId, workId } = useFiltersContext();
  const start_date = calendarRange?.from
    ?.toLocaleDateString("ru-RU")
    .split(".")
    .reverse()
    .join("-");
  const end_date = calendarRange?.to
    ?.toLocaleDateString("ru-RU")
    .split(".")
    .reverse()
    .join("-");

  const { data, error, isLoading } = usePlansQuery({
    start_date: start_date,
    end_date: end_date,
    search: searchQuery,
    managers: managerId ? [managerId] : undefined,
    work_items: workId ? [workId] : undefined,
  });

  const plans = (data?.data || []).sort((a, b) => {
    let diff =
      new Date(a.assigned_date).getTime() - new Date(b.assigned_date).getTime();
    if (diff === 0) {
      return (
        new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
      );
    }
    return diff;
  });

  return {
    plans,
    error,
    isLoading,
  };
};
