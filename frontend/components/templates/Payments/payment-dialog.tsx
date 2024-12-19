import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { FC, ReactNode } from "react";
import { useUpdatePaymentRegistry } from "./index.hooks";
import { Button } from "@/components/ui/button";

interface PaymentDialogProps {
  paymentRegistry: PaymentRegistry;
  children: ReactNode;
}

const PaymentDialog: FC<PaymentDialogProps> = ({
  paymentRegistry,
  children,
}) => {
  const {} = useUpdatePaymentRegistry(paymentRegistry);

  return (
    <Dialog>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="max-w-xl">
        <DialogHeader>
          <DialogTitle className="mb-4">Изменить выплату</DialogTitle>
        </DialogHeader>
        <div className="flex gap-4 flex-col justify-stretch w-full"></div>
        <DialogFooter>
          <Button>Подтвердить выплату</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default PaymentDialog;
