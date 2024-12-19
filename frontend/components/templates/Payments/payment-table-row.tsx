import { TableCell, TableRow } from "@/components/ui/table";
import { cn } from "@/lib/utils";
import { FC } from "react";

interface PaymentTableRowProps {
  className: string;
}

const PaymentTableRow: FC<PaymentTableRowProps> = ({ className }) => {
  return (
    <TableRow className={cn("", className)}>
      <TableCell>Дата</TableCell>
      <TableCell>Менеджер</TableCell>
      <TableCell>Сумма</TableCell>
      <TableCell>Изменить</TableCell>
    </TableRow>
  );
};

export default PaymentTableRow;
