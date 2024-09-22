import useFiltersContext from "@/components/molecules/side-bar/index.providers";
import { planExportQuery, managerReportExportQuery, dispatchExportQuery } from "@/lib/backend/plans";
import { decodeContentDisposition } from "@/lib/utils";
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
    start_date: calendarRange?.from
      ?.toLocaleDateString("ru-RU")
      .split(".")
      .reverse()
      .join("-"),
    end_date: calendarRange?.to
      ?.toLocaleDateString("ru-RU")
      .split(".")
      .reverse()
      .join("-"),
    search: searchQuery,
    managers: managerId ? [managerId] : undefined,
    work_items: workId ? [workId] : undefined,
  });

  data
    .then((data) => {
      if (data?.data) {
        console.log(data);
        const filename = decodeContentDisposition(
          data.headers["content-disposition"],
        )
          ?.split("filename=")[1]
          .replace(/[^A-Za-zА-Яа-я\s0-9.-]/g, "");
        const url = window.URL.createObjectURL(new Blob([data.data]));
        const a = document.createElement("a");
        a.href = url;
        a.download = filename || "plans.xlsx";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      }
      setIsLoading(false);
    })
    .catch((e) => {
      console.error(e);
      setIsLoading(false);
      toast({
        title: "Ошибка, не удалось скачать план",
        description: e.message,
      });
    });
};

export const handleDispatchDownload = ({
  setIsLoading,
  toast,
  calendarRange,
  searchQuery,
  managerId,
  workId,
}: handlePlanDownloadProps) => {
  setIsLoading(true);

  const data = dispatchExportQuery({
    start_date: calendarRange?.from
      ?.toLocaleDateString("ru-RU")
      .split(".")
      .reverse()
      .join("-"),
    end_date: calendarRange?.to
      ?.toLocaleDateString("ru-RU")
      .split(".")
      .reverse()
      .join("-"),
    search: searchQuery,
    managers: managerId ? [managerId] : undefined,
    work_items: workId ? [workId] : undefined,
  });

  data
    .then((data) => {
      if (data?.data) {
        console.log(data);
        const filename = decodeContentDisposition(
          data.headers["content-disposition"],
        )
          ?.split("filename=")[1]
          .replace(/[^A-Za-zА-Яа-я\s0-9.-]/g, "");
        const url = window.URL.createObjectURL(new Blob([data.data]));
        const a = document.createElement("a");
        a.href = url;
        a.download = filename || "dispatch.xlsx";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      }
      setIsLoading(false);
    })
    .catch((e) => {
      console.error(e);
      setIsLoading(false);
      toast({
        title: "Ошибка, не удалось скачать план",
        description: e.message,
      });
    });
};

export const handleReportDownload = ({
  setIsLoading,
  toast,
  calendarRange,
  searchQuery,
  managerId,
  workId,
}: handlePlanDownloadProps) => {
  if (!managerId || managerId === "-1") {
    toast({
      title: "Выберите менеджера",
      description: "Для скачивания отчета необходимо выбрать одного менеджера",
    });
    return;
  }

  setIsLoading(true);

  const data = managerReportExportQuery({
    start_date: calendarRange?.from
      ?.toLocaleDateString("ru-RU")
      .split(".")
      .reverse()
      .join("-"),
    end_date: calendarRange?.to
      ?.toLocaleDateString("ru-RU")
      .split(".")
      .reverse()
      .join("-"),
    search: searchQuery,
    managers: managerId ? [managerId] : undefined,
    work_items: workId ? [workId] : undefined,
  });

  data
    .then((data) => {
      if (data?.data) {
        const filename = decodeContentDisposition(
          data.headers["content-disposition"],
        )
          ?.split("filename=")[1]
          .replace(/[^A-Za-zА-Яа-я\s0-9.-]/g, "");
        const url = window.URL.createObjectURL(new Blob([data.data]));
        const a = document.createElement("a");
        a.href = url;
        a.download = filename || "report.xlsx";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      }
      setIsLoading(false);
    })
    .catch((e) => {
      console.error(e);
      setIsLoading(false);
      toast({
        title: "Ошибка, не удалось скачать отчет",
        description: e.message,
      });
    });
};
