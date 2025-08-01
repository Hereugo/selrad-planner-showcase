"use client";

import { FC, useState } from "react";
import {
  handleDispatchDownload,
  handlePlanDownload,
  handleReportDownload,
  handleCompareReportDownload,
  handleDispatchListDownload,
  handlePaymentReportDownload,
  handleDistributionCostReportDownload,
} from "./index.hooks";
import useFiltersContext from "@/components/molecules/side-bar/index.providers";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { useToast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import { Loader2, Terminal } from "lucide-react";
import { cn } from "@/lib/utils";
import { useDriversQuery } from "@/lib/backend/users/managers";
import { useViewFeature } from "@/lib/hooks/useViewFeature";

interface ExportExcelTemplateProps {}

const ExportExcelTemplate: FC<ExportExcelTemplateProps> = () => {
  const viewFeature = useViewFeature();
  const { data: allDrivers } = useDriversQuery();

  const { calendarRange, searchQuery, managerId, workId } = useFiltersContext();
  const { toast } = useToast();

  const [isPlanLoading, setIsPlanLoading] = useState(false);
  const [isDispatchLoading, setIsDispatchLoading] = useState(false);
  const [isDispatchListLoading, setIsDispatchListLoading] = useState(false);
  const [isReportLoading, setIsReportLoading] = useState(false);
  const [isCompareLoading, setIsCompareLoading] = useState(false);
  const [isPaymentLoading, setIsPaymentLoading] = useState(false);
  const [isDistributionCostLoading, setIsDistributionCostLoading] =
    useState(false);

  return (
    <>
      <div className="flex gap-4 mb-4">
        <Button
          onClick={() =>
            handlePlanDownload({
              setIsLoading: setIsPlanLoading,
              calendarRange,
              searchQuery,
              managerId,
              workId,
              toast,
            })
          }
          className={cn(viewFeature.canExportPlans ? "" : "hidden")}
          disabled={isPlanLoading}
        >
          Скачать план
          {isPlanLoading && <Loader2 className="w-6 h-6 ml-2 animate-spin" />}
        </Button>

        <Button
          onClick={() =>
            handleDispatchDownload({
              setIsLoading: setIsDispatchLoading,
              calendarRange,
              searchQuery,
              managerId,
              workId,
              toast,
            })
          }
          className={cn(viewFeature.canExportDispatchReport ? "" : "hidden")}
          disabled={isDispatchLoading}
        >
          Скачать отчет по диспечерскому
          {isDispatchLoading && (
            <Loader2 className="w-6 h-6 ml-2 animate-spin" />
          )}
        </Button>

        <Button
          onClick={() =>
            handleReportDownload({
              setIsLoading: setIsReportLoading,
              calendarRange,
              managerId,
              toast,
            })
          }
          className={cn(viewFeature.canExportReport ? "" : "hidden")}
          disabled={isReportLoading}
        >
          Скачать отчет
          {isReportLoading && <Loader2 className="w-6 h-6 ml-2 animate-spin" />}
        </Button>
        <Button
          onClick={() =>
            handleDispatchListDownload({
              setIsLoading: setIsDispatchListLoading,
              calendarRange,
              toast,
              searchQuery,
              managerId,
              workId,
            })
          }
          className={cn(viewFeature.canExportDispatchList ? "" : "hidden")}
          disabled={
            isDispatchListLoading ||
            !allDrivers?.data.find((driver) => driver.id === managerId)
              ?.is_driver
          }
        >
          Скачать диспечерский лист
          {isDispatchListLoading && (
            <Loader2 className="w-6 h-6 ml-2 animate-spin" />
          )}
        </Button>
        <Button
          onClick={() =>
            handleCompareReportDownload({
              setIsLoading: setIsCompareLoading,
              calendarRange,
              toast,
              managerId,
              workId,
            })
          }
          className={cn(viewFeature.canExportCompareReport ? "" : "hidden")}
          disabled={isCompareLoading}
        >
          Сравнить с прошлым годом
          {isCompareLoading && (
            <Loader2 className="w-6 h-6 ml-2 animate-spin" />
          )}
        </Button>
        <Button
          onClick={() =>
            handlePaymentReportDownload({
              setIsLoading: setIsPaymentLoading,
              calendarRange,
              toast,
              managerId,
              workId,
            })
          }
          className={cn(viewFeature.canExportPaymentReport ? "" : "hidden")}
          disabled={isPaymentLoading}
        >
          Скачать отчет по оплатам
          {isPaymentLoading && (
            <Loader2 className="w-6 h-6 ml-2 animate-spin" />
          )}
        </Button>
        <Button
          onClick={() =>
            handleDistributionCostReportDownload({
              setIsLoading: setIsDistributionCostLoading,
              calendarRange,
              toast,
              managerId,
              workId,
            })
          }
          className={cn(
            viewFeature.canExportDistributionCostReport ? "" : "hidden",
          )}
          disabled={isDistributionCostLoading}
        >
          Скачать отчет по распределению затрат
          {isDistributionCostLoading && (
            <Loader2 className="w-6 h-6 ml-2 animate-spin" />
          )}
        </Button>
      </div>
      {(searchQuery || managerId || workId) && (
        <Alert variant="warning">
          <Terminal className="h-4 w-4" />
          <AlertTitle>Внимание!</AlertTitle>
          <AlertDescription>
            Включены фильтры, убедитесь что они правильно настроены перед
            экспортом
            <br />
            <ul className="list-disc list-inside">
              {searchQuery && <li>Поиск: {searchQuery}</li>}
              {managerId && <li>Менеджер</li>}
              {workId && <li>Работа</li>}
            </ul>
          </AlertDescription>
        </Alert>
      )}
    </>
  );
};

export default ExportExcelTemplate;
