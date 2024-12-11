"use client";

import { Table, TableBody, TableCaption } from "@/components/ui/table";
import { useFinancialPlans } from "./index.hooks";
import FinancialPlansTableHeader from "./financial-plans-table-header";
import FinancialPlansTableRow from "./financial-plans-table-row";
import { Loader2 } from "lucide-react";

const FinancialPlansTable = () => {
  const { financialPlans, isLoading } = useFinancialPlans();

  return (
    <>
      <Table className="mt-2">
        <FinancialPlansTableHeader />
        <TableBody>
          {
            financialPlans.reduce(
              (acc, plan) => {
                if (acc.prevDate !== plan.assigned_date) {
                  acc.prevDate = plan.assigned_date;
                  acc.parity = 1 - acc.parity;
                }
                acc.rows.push(
                  <FinancialPlansTableRow
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
        {!financialPlans.length && !isLoading && (
          <TableCaption>Нет планов</TableCaption>
        )}
      </Table>
      {isLoading && (
        <div className="flex justify-center items-center h-40 w-full">
          <Loader2 className="animate-spin" />
        </div>
      )}
    </>
  );
};

export default FinancialPlansTable;
