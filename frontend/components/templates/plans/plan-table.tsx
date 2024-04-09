"use client";

import {
  Table,
  TableBody,
  TableCaption,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { usePlans } from "./index.hooks";
import PlanTableRow from "./plan-table-row";
import { Loader2 } from "lucide-react";

const PlanTable = () => {
  const { plans, isLoading } = usePlans();

  return (
    <>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[150px]">Дата</TableHead>
            <TableHead className="w-[200px]">Клиент</TableHead>
            <TableHead>Работы</TableHead>
            <TableHead>Менеджеры</TableHead>
            <TableHead>Сумма отгрузки (₸)</TableHead>
            <TableHead>Кол. коробок</TableHead>
            <TableHead></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {
            plans.reduce(
              (acc, plan) => {
                if (acc.prevDate !== plan.assigned_date) {
                  acc.prevDate = plan.assigned_date;
                  acc.parity = 1 - acc.parity;
                }

                acc.rows.push(
                  <PlanTableRow
                    key={plan.id}
                    plan={plan}
                    className={acc.parity ? "bg-yellow-50" : ""}
                  />,
                );

                return acc;
              },
              {
                prevDate: "",
                parity: 1,
                rows: [] as JSX.Element[],
              },
            ).rows
          }
        </TableBody>
        {!plans.length && !isLoading && <TableCaption>Нет планов</TableCaption>}
      </Table>
      {isLoading && (
        <div className="flex justify-center items-center h-40 w-full">
          <Loader2 className="animate-spin" />
        </div>
      )}
    </>
  );
};

export default PlanTable;
