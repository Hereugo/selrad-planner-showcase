import useFiltersContext from "@/components/molecules/side-bar/index.providers";
import { usePlansQuery } from "@/lib/backend/plans";
import { formatDateBackend } from "@/lib/utils";

export const useFinancialPlans = () => {
  const { calendarRange, searchQuery, managerId, workId } = useFiltersContext();
  const startDate = formatDateBackend(calendarRange?.from);
  const endDate = formatDateBackend(calendarRange?.to);

  const { data, error, isLoading } = usePlansQuery({
    start_date: startDate,
    end_date: endDate,
    search: searchQuery,
    managers: managerId ? [managerId] : undefined,
    work_items: workId ? [workId] : undefined, // todo: mn only отгрузка и возврат
  });

  const financialPlans = (data?.data || []).sort((a, b) => {
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
    financialPlans,
    error,
    isLoading,
  };
};
