import useFiltersContext from "@/components/molecules/side-bar/index.providers";
import { usePlanExportQuery } from "@/lib/backend/plans";

export const useDownloadExcel = () => {
  const { calendarRange, searchQuery, managerId, workId } = useFiltersContext();

  const { data, error, isLoading } = usePlanExportQuery({
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

  const handleDownload = () => {
    if (data) {
      console.log(data.data);
      // window.open(data.data, "_blank");
    }
  };

  return {
    error,
    isLoading,
    handleDownload,
  };
};
