import { TableHeader, TableRow, TableHead } from "@/components/ui/table";

const FinancialPlansTableHeader = () => {
  return (
    <TableHeader>
      <TableRow>
        <TableHead className="w-[150px]">Дата</TableHead>
        <TableHead className="w-[200px]">Клиент</TableHead>
        <TableHead>Сумма отгрузки (₸)</TableHead>
        <TableHead className="w-[150px]">Дата накладной</TableHead>
        <TableHead>Возврат</TableHead>
        <TableHead></TableHead>
      </TableRow>
    </TableHeader>
  );
};

export default FinancialPlansTableHeader;
