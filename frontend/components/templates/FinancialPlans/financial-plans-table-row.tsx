import { TableCell, TableRow } from "@/components/ui/table";
import { FC } from "react";
import { cn, formatDate, formatPrice, isPlanAReturn } from "@/lib/utils";
import FinancialPlansEditDialog from "./financial-plans-dialog";

interface FinancialPlansTableRowProps {
  plan: Plan;
  className?: string;
}

const FinancialPlansTableRow: FC<FinancialPlansTableRowProps> = ({
  plan,
  className,
}) => {
  return (
    <TableRow
      id={`plan-row-${plan.id}`}
      className={cn("duration-500 hover:bg-blue-50", className)}
    >
      <TableCell>{formatDate(plan.assigned_date)}</TableCell>
      <TableCell className="text-ellipsis" title={plan.client.name}>
        {plan.client.name}
      </TableCell>
      <TableCell className="text-center">
        {formatPrice(plan.shipment_cost)}
      </TableCell>
      <TableCell>
        {plan.invoice_date ? formatDate(plan.invoice_date) : "Не указано"}
      </TableCell>
      <TableCell>{isPlanAReturn(plan) && "Есть"}</TableCell>
      <TableCell className="max-w-[60px] text-ellipsis line-clamp-1">
        {plan.accountant_comment}
      </TableCell>
      <TableCell className="text-blue-500 hover:cursor-pointer">
        <FinancialPlansEditDialog plan={plan}>
          <span>Изменить</span>
        </FinancialPlansEditDialog>
      </TableCell>
    </TableRow>
  );
};

export default FinancialPlansTableRow;
