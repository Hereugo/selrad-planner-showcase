import { Table, TableBody, TableCaption } from "@/components/ui/table";
import PaymentTableHeader from "./payment-table-header";
import PaymentTableRow from "./payment-table-row";
import { usePaymentRegistries } from "./index.hooks";
import { Loader2 } from "lucide-react";

const PaymentTable = () => {
  const { isLoading, isError, paymentRegistries } = usePaymentRegistries();

  return (
    <>
      <Table className="mt-2">
        <PaymentTableHeader />
        <TableBody>
          {
            paymentRegistries.reduce(
              (acc, paymentRegistry) => {
                if (acc.prevDate !== paymentRegistry.date) {
                  acc.prevDate = paymentRegistry.date;
                  acc.parity = 1 - acc.parity;
                }
                acc.rows.push(
                  <PaymentTableRow
                    paymentRegistry={paymentRegistry}
                    key={paymentRegistry.id}
                    className={acc.parity ? "bg-yellow-50" : ""}
                  />,
                );

                return acc;
              },
              {
                prevDate: "",
                parity: 1,
                rows: [] as JSX.Element[],
              },
            ).rows
          }
        </TableBody>
        {!paymentRegistries.length && !isLoading && (
          <TableCaption>Нет выплат</TableCaption>
        )}
      </Table>
      {isLoading && (
        <div className="flex justify-center items-center h-40 w-full">
          <Loader2 className="animate-spin" />
        </div>
      )}
    </>
  );
};

export default PaymentTable;
