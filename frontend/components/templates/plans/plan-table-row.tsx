import { TableCell, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { FC } from "react";
import { managerFullName, managerShortName } from "@/lib/utils";
import PlanDialogEdit from "@/components/molecules/plan-dialog-edit";

interface PlanTableRowProps {
    plan: Plan;
}

const PlanTableRow: FC<PlanTableRowProps> = ({ plan }) => {
    return (
        <TableRow id={`plan-row-${plan.id}`} className="duration-500">
            <TableCell>{formatDate(plan.assigned_date)}</TableCell>
            <TableCell className="text-ellipsis" title={plan.client.name}>
                {plan.client.name}
            </TableCell>
            <TableCell>
                <div className="flex gap-1 flex-wrap">
                    {plan.worklist.map((work) => (
                        <Badge key={work.id} title={work.description}>
                            {work.name}
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
            <TableCell className="text-center">{plan.shipment_cost}</TableCell>
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

const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString("ru-RU", {
        year: "numeric",
        month: "long",
        day: "numeric",
    });
};
