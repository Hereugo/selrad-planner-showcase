import { TableHead, TableHeader, TableRow } from "@/components/ui/table";

const PaymentTableHeader = () => {
  return (
    <TableHeader>
      <TableRow>
        <TableHead className="w-40">Дата</TableHead>
        <TableHead>Менеджер</TableHead>
        <TableHead>Сумма</TableHead>
        <TableHead>Изменить</TableHead>
      </TableRow>
    </TableHeader>
  );
};

export default PaymentTableHeader;
