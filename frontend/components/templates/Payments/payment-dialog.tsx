import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { FC, ReactNode, useState } from "react";
import { useUpdatePaymentRegistry } from "./index.hooks";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { formatDate, managerFullName } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import PaymentDialogPlanTable from "./payment-dialog-plan-table";
import { Checkbox } from "@/components/ui/checkbox";

interface PaymentDialogProps {
  paymentRegistry: PaymentRegistry;
  children: ReactNode;
}

const PaymentDialog: FC<PaymentDialogProps> = ({
  paymentRegistry,
  children,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const {
    payment,
    setPayment,
    bonus,
    setBonus,
    comment,
    setComment,
    handleUpdatePaymentRegistry,
    isConfirmed,
    setIsConfirmed,
  } = useUpdatePaymentRegistry(paymentRegistry, () => setIsOpen(false));

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="max-w-xl min-w-[60vw]">
        <DialogHeader>
          <DialogTitle className="mb-4">Изменить выплату</DialogTitle>
        </DialogHeader>
        <div className="flex gap-4 flex-col justify-stretch w-full">
          <div className="flex gap-4 flex-row justify-stretch w-full">
            <div className="flex gap-4 flex-col justify-stretch w-full max-w-40">
              <div>
                <Label htmlFor="date">Дата</Label>
                <div id="date">{formatDate(paymentRegistry.date)}</div>
              </div>
              <div>
                <Label htmlFor="manager">Менеджер</Label>
                <div id="manager">
                  {managerFullName(paymentRegistry.manager)}
                </div>
              </div>
            </div>
            <div className="w-full max-h-[50vh] overflow-auto">
              <PaymentDialogPlanTable plans={paymentRegistry.plans} />
            </div>
          </div>
          <div className="flex gap-4 flex-row justify-stretch w-full">
            <div>
              <Label htmlFor="payment">Ставка</Label>
              <Input
                id="payment"
                value={payment}
                onChange={(e) => setPayment(Number(e.target.value))}
              />
            </div>
            <div>
              <Label htmlFor="bonus">Доплата</Label>
              <Input
                id="bonus"
                value={bonus}
                onChange={(e) => setBonus(Number(e.target.value))}
              />
            </div>
            <div className="w-full">
              <Label htmlFor="comment">Комментарий</Label>
              <Textarea
                id="comment"
                value={comment}
                onChange={(e) => setComment(e.target.value ?? "")}
              />
            </div>
          </div>
        </div>
        <DialogFooter className="flex justify-between gap-8">
          <div className="flex gap-2 items-center cursor-pointer">
            <Checkbox
              id="isConfirmed"
              checked={isConfirmed}
              onChange={alert}
              onClick={() => setIsConfirmed((v) => !v)}
            />
            <Label htmlFor="isConfirmed">Подтвердить</Label>
          </div>
          <Button onClick={handleUpdatePaymentRegistry}>Сохранить</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default PaymentDialog;
