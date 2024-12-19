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
  } = useUpdatePaymentRegistry(paymentRegistry);

  setIsConfirmed;

  return (
    <Dialog>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="max-w-xl">
        <DialogHeader>
          <DialogTitle className="mb-4">Изменить выплату</DialogTitle>
        </DialogHeader>
        <div className="flex gap-4 flex-col justify-stretch w-full">
          <div className="flex gap-4 flex-row justify-stretch w-full">
            <div className="flex gap-4 flex-col justify-stretch w-full">
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
            <div>
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
            <div>
              <Label htmlFor="comment">Комментарий</Label>
              <Textarea
                id="comment"
                value={comment}
                onChange={(e) => setComment(e.target.value ?? "")}
              />
            </div>
          </div>
        </div>
        <DialogFooter>
          <div>
            <Checkbox
              id="isConfirmed"
              checked={isConfirmed}
              onChange={alert}
              // todo: <- check if this works
              // onChange={(e) => setIsConfirmed(e.target.value)}
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
