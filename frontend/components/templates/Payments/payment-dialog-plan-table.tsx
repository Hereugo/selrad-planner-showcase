import {
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { formatClientName, formatPrice } from "@/lib/utils";
import { FC } from "react";

interface PaymentDialogPlanTableProps {
  plans: Plan[];
}

const PaymentDialogPlanTable: FC<PaymentDialogPlanTableProps> = ({ plans }) => {
  const totalBoxCount = plans.reduce((acc, plan) => acc + plan.box_count, 0);
  const totalShipmentCost = plans.reduce(
    (acc, plan) => acc + plan.shipment_cost,
    0,
  );

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead></TableHead>
          <TableHead>Клиент</TableHead>
          <TableHead>Коробок</TableHead>
          <TableHead>Сумма</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {plans.map((plan, i) => (
          <PaymentDialogPlanTableRow key={plan.id} plan={plan} index={i + 1} />
        ))}
      </TableBody>
      <TableFooter>
        <TableRow>
          <TableHead></TableHead>
          <TableHead className="text-right">Итого</TableHead>
          <TableHead>{totalBoxCount}</TableHead>
          <TableHead>{formatPrice(totalShipmentCost)}</TableHead>
        </TableRow>
      </TableFooter>
    </Table>
  );
};

interface PaymentDialogPlanTableRowProps {
  plan: Plan;
  index: number;
}

const PaymentDialogPlanTableRow: FC<PaymentDialogPlanTableRowProps> = ({
  plan,
  index,
}) => {
  return (
    <TableRow>
      <TableCell>{index}.</TableCell>
      <TableCell>{formatClientName(plan.client.name)}</TableCell>
      <TableCell>{plan.box_count}</TableCell>
      <TableCell>{formatPrice(plan.shipment_cost)}</TableCell>
    </TableRow>
  );
};

export default PaymentDialogPlanTable;
