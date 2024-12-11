import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { FC, ReactNode } from "react";

interface PaymentDialogProps {
  children: ReactNode;
}

const PaymentDialog: FC<PaymentDialogProps> = ({ children }) => {
  return (
    <Dialog>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="max-w-md">hi</DialogContent>
    </Dialog>
  );
};

export default PaymentDialog;
