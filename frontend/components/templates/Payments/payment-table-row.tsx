import { TableCell, TableRow } from "@/components/ui/table";
import { cn, formatDate, managerFullName } from "@/lib/utils";
import { FC } from "react";

interface PaymentTableRowProps {
  paymentRegistry: PaymentRegistry;
  className: string;
}

const PaymentTableRow: FC<PaymentTableRowProps> = ({
  paymentRegistry,
  className,
}) => {
  return (
    <TableRow className={cn("", className)}>
      <TableCell>{formatDate(paymentRegistry.date)}</TableCell>
      <TableCell>{managerFullName(paymentRegistry.manager)}</TableCell>
      <TableCell>{paymentRegistry.payment + paymentRegistry.bonus}</TableCell>
      <TableCell>Изменить</TableCell>
    </TableRow>
  );
};

export default PaymentTableRow;
