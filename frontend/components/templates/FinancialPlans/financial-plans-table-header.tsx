import { TableHeader, TableRow, TableHead } from "@/components/ui/table";

const FinancialPlansTableHeader = () => {
  return (
    <TableHeader>
      <TableRow>
        <TableHead className="w-[150px]">Дата</TableHead>
        <TableHead className="w-[200px]">Клиент</TableHead>
        <TableHead className="w-[160px]">Сумма отгрузки</TableHead>
        <TableHead>Менеджеры</TableHead>
        <TableHead>Возврат</TableHead>
        <TableHead>Комментарий</TableHead>
        <TableHead></TableHead>
      </TableRow>
    </TableHeader>
  );
};

export default FinancialPlansTableHeader;
