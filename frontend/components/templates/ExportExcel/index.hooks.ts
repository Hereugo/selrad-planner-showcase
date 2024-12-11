import { compareReportExportQuery } from "@/lib/backend/clients";
import {
  planExportQuery,
  managerReportExportQuery,
  dispatchExportQuery,
  dispatchListExportQuery,
} from "@/lib/backend/plans";
import { decodeContentDisposition, formatDateBackend } from "@/lib/utils";
import { DateRange } from "react-day-picker";

interface handlePlanDownloadProps {
  setIsLoading: Function;
  toast: Function;
  calendarRange?: DateRange;
  searchQuery?: string;
  managerId?: Manager["id"];
  workId?: WorkItem["id"];
}

interface handleCompareReportDownloadProps {
  setIsLoading: Function;
  toast: Function;
  calendarRange?: DateRange;
  yearDifference?: number;
  managerId?: Manager["id"];
  workId?: WorkItem["id"];
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
    start_date: formatDateBackend(calendarRange?.from),
    end_date: formatDateBackend(calendarRange?.to),
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
    start_date: formatDateBackend(calendarRange?.from),
    end_date: formatDateBackend(calendarRange?.to),
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
    start_date: formatDateBackend(calendarRange?.from),
    end_date: formatDateBackend(calendarRange?.to),
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

export const handleCompareReportDownload = ({
  setIsLoading,
  toast,
  calendarRange,
  yearDifference,
  managerId,
  workId,
}: handleCompareReportDownloadProps) => {
  setIsLoading(true);

  const data = compareReportExportQuery({
    start_date: formatDateBackend(calendarRange?.from),
    end_date: formatDateBackend(calendarRange?.to),
    diff_year: yearDifference || 1,
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
        a.download = filename || "compare_report.xlsx";
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

export const handleDispatchListDownload = ({
  setIsLoading,
  toast,
  calendarRange,
  searchQuery,
  managerId,
  workId,
}: handlePlanDownloadProps) => {
  setIsLoading(true);

  if (!managerId) return;

  const data = dispatchListExportQuery(managerId, {
    start_date: formatDateBackend(calendarRange?.from),
    end_date: formatDateBackend(calendarRange?.to),
    search: searchQuery,
    work_items: workId ? [workId] : undefined,
    set_time_dispatch: false,
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
        a.download = filename ?? "dispatch_list.xlsx";
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
