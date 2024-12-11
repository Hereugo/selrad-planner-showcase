import { Table, TableBody } from "@/components/ui/table";
import PaymentTableHeader from "./payment-table-header";
import PaymentTableRow from "./payment-table-row";

const PaymentTable = () => {
  return (
    <Table className="mt-2">
      <PaymentTableHeader />
      <TableBody>
        <PaymentTableRow />
      </TableBody>
    </Table>
  );
};

export default PaymentTable;
