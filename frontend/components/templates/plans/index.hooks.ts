import useFiltersContext from "@/components/molecules/side-bar/index.providers";
import { usePlansQuery } from "@/lib/backend/plans";

export const usePlans = () => {
  const { calendarRange, searchQuery, managerId, workId } = useFiltersContext();

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
    manager_id: managerId,
    worklist_id: workId,
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
