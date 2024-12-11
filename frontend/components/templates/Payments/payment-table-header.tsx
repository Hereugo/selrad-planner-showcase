import { TableHead, TableHeader, TableRow } from "@/components/ui/table";

const PaymentTableHeader = () => {
  return (
    <TableHeader>
      <TableRow>
        <TableHead>Дата</TableHead>
        Менеджер
        <TableHead>Сумма</TableHead>
        <TableHead>Изменить</TableHead>
      </TableRow>
    </TableHeader>
  );
};

export default PaymentTableHeader;
