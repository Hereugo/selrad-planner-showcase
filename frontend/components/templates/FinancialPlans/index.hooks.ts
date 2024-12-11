import useFiltersContext from "@/components/molecules/side-bar/index.providers";
import { usePlansQuery } from "@/lib/backend/plans";
import { useWorkItemsQuery } from "@/lib/backend/work_items";
import { formatDateBackend } from "@/lib/utils";

export const useFinancialPlans = () => {
  const { data: workItems } = useWorkItemsQuery();
  const { calendarRange, searchQuery } = useFiltersContext();
  const startDate = formatDateBackend(calendarRange?.from);
  const endDate = formatDateBackend(calendarRange?.to);

  const financialWorkItemIds =
    workItems?.data
      .filter((item) => {
        return (
          item.content_type === "Return" || item.content_type === "Shipment"
        );
      })
      .map((item) => item.id) || [];

  const { data, error, isLoading } = usePlansQuery({
    start_date: startDate,
    end_date: endDate,
    search: searchQuery,
    work_items: financialWorkItemIds,
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
