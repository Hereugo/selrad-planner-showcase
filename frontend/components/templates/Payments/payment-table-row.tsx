import { TableCell, TableRow } from "@/components/ui/table";

const PaymentTableRow = () => {
  return (
    <TableRow>
      <TableCell>Дата</TableCell>
      Менеджер
      <TableCell>Сумма</TableCell>
      <TableCell>Изменить</TableCell>
    </TableRow>
  );
};

export default PaymentTableRow;
