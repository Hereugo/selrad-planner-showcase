import { Label } from "@/components/ui/label";
import { FC } from "react";
import DayPicker from "./day-picker";
import CommentInput from "./input-comment";

interface AccountantFieldsProps {
  invoiceDate: string | undefined;
  setInvoiceDate: (date: string) => void;
  accountantComment?: string;
  setAccountantComment: (comment: string) => void;
}

const AccountantFields: FC<AccountantFieldsProps> = ({
  invoiceDate,
  setInvoiceDate,
  accountantComment,
  setAccountantComment,
}) => {
  return (
    <div className="w-full flex flex-col gap-2">
      <div className="w-full">
        <Label htmlFor="invoice_date">Дата накладной</Label>
        <DayPicker
          id="invoice_date"
          assignedDate={invoiceDate}
          setAssignedDate={setInvoiceDate}
        />
      </div>
      <div className="w-full">
        <Label htmlFor="accountant_comment">Комментарий для бухгалтера</Label>
        <CommentInput
          id="accountant_comment"
          comment={accountantComment}
          setComment={setAccountantComment}
        />
      </div>
    </div>
  );
};

export default AccountantFields;
