import { TableCell, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { FC } from "react";
import {
  cn,
  formatDate,
  formatPrice,
  managerFullName,
  managerShortName,
} from "@/lib/utils";
import PlanDialogEdit from "@/components/molecules/plan-dialog-edit";

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
      <TableCell>{/* {formatDate(plan.invoice_date)}  todo: mn */}</TableCell>
      <TableCell>{/* {plan.is_return  todo: mn */}</TableCell>
      <TableCell className="text-blue-500 hover:cursor-pointer">
        <PlanDialogEdit plan={plan}>
          <span>Изменить</span>
        </PlanDialogEdit>
      </TableCell>
    </TableRow>
  );
};

export default FinancialPlansTableRow;
