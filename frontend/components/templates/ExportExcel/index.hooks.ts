import useFiltersContext from "@/components/molecules/side-bar/index.providers";
import { planExportQuery, managerReportExportQuery } from "@/lib/backend/plans";
import { DateRange } from "react-day-picker";

interface handlePlanDownloadProps {
  setIsLoading: Function;
  toast: Function;
  calendarRange?: DateRange;
  searchQuery?: string;
  managerId?: string;
  workId?: string;
}

export const handlePlanDownload = ({
  setIsLoading,
  toast,
  calendarRange,
  searchQuery,
  managerId,
  workId,
}: handlePlanDownloadProps) => {
  setIsLoading(true);

  const data = planExportQuery({
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

  data
    .then((data) => {
      if (data?.data) {
        const url = window.URL.createObjectURL(new Blob([data.data]));
        const a = document.createElement("a");
        a.href = url;
        a.download = "plans.xlsx";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      }
      setIsLoading(false);
    })
    .catch((e) => {
      console.log(e);
      setIsLoading(false);
      toast({
        title: "Ошибка, не удалось скачать план",
        description: e.message,
      });
    });
};

interface handleReportDownloadProps {
  setIsLoading: Function;
  toast: Function;
  managerId: Manager["id"] | undefined;
}

export const handleReportDownload = ({
  setIsLoading,
  toast,
  managerId,
}: handleReportDownloadProps) => {
  if (!managerId || managerId === "-1") {
    toast({
      title: "Выберите менеджера",
      description: "Для скачивания отчета необходимо выбрать одного менеджера",
    });
    return;
  }

  setIsLoading(true);

  const data = managerReportExportQuery({ manager_id: managerId });

  data
    .then((data) => {
      if (data?.data) {
        const url = window.URL.createObjectURL(new Blob([data.data]));
        const a = document.createElement("a");
        a.href = url;
        a.download = "report.xlsx";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      }
      setIsLoading(false);
    })
    .catch((e) => {
      console.log(e.request.text());
      setIsLoading(false);
      toast({
        title: "Ошибка, не удалось скачать отчет",
        description: e.message,
      });
    });
};
