import { TableCell, TableRow } from "@/components/ui/table";
import { cn, formatDate, formatPrice, managerFullName } from "@/lib/utils";
import { FC } from "react";
import PaymentDialog from "./payment-dialog";
import { Circle } from "lucide-react";

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
      <TableCell>
        {formatPrice(paymentRegistry.payment + paymentRegistry.bonus)}
      </TableCell>
      <TableCell className="text-blue-500 hover:cursor-pointer">
        <PaymentDialog paymentRegistry={paymentRegistry}>
          <div className="relative max-w-[100px]">
            <span>
              {paymentRegistry.is_confirmed ? "Изменить" : "Подтвердить"}
            </span>
            {!paymentRegistry.is_confirmed && (
              <Circle className="absolute fill-red-500 stroke-none top-0 right-0 w-2 h-2" />
            )}
          </div>
        </PaymentDialog>
      </TableCell>
    </TableRow>
  );
};

export default PaymentTableRow;
