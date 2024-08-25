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

interface PlanTableRowProps {
  plan: Plan;
  className?: string;
}

const PlanTableRow: FC<PlanTableRowProps> = ({ plan, className }) => {
  return (
    <TableRow
      id={`plan-row-${plan.id}`}
      className={cn("duration-500 hover:bg-blue-50", className)}
    >
      <TableCell>{formatDate(plan.assigned_date)}</TableCell>
      <TableCell className="text-ellipsis" title={plan.client.name}>
        {plan.client.name}
      </TableCell>
      <TableCell>
        <div className="flex gap-1 flex-wrap">
          {plan.work_items.map((workItem) => (
            <Badge key={workItem.id} title={workItem.description}>
              {workItem.name}
            </Badge>
          ))}
        </div>
      </TableCell>
      <TableCell>
        <div className="flex gap-1 flex-wrap">
          {plan.managers.map((manager) => (
            <Badge key={manager.id} title={managerFullName(manager)}>
              {managerShortName(manager)}
            </Badge>
          ))}
        </div>
      </TableCell>
      <TableCell className="text-center">
        {formatPrice(plan.shipment_cost)}
      </TableCell>
      <TableCell className="text-center">{plan.box_count}</TableCell>
      <TableCell className="text-blue-500 hover:cursor-pointer">
        <PlanDialogEdit plan={plan}>
          <span>Изменить</span>
        </PlanDialogEdit>
      </TableCell>
    </TableRow>
  );
};

export default PlanTableRow;
