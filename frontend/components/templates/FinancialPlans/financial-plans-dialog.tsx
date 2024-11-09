import { useUpdatePlan } from "@/components/molecules/plan-dialog-edit/index.hooks";
import ShipmentCostInput from "@/components/molecules/plan-dialog-edit/input-shipment-cost";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Loader2 } from "lucide-react";
import { FC, ReactNode } from "react";

interface FinancialPlansEditDialogProps {
  plan: Plan;
  children: ReactNode;
}

const FinancialPlansEditDialog: FC<FinancialPlansEditDialogProps> = ({
  plan,
  children,
}) => {
  const {
    shipmentCostFormula,
    setShipmentCostFormula,
    isOpen,
    setIsOpen,
    isLoading,
    handleUpdatePlan,
  } = useUpdatePlan(plan);

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="mb-4">Изменить план</DialogTitle>
        </DialogHeader>
        <div className="flex gap-4 flex-row justify-stretch w-full">
          <ShipmentCostInput
            id="shipment_cost"
            className="flex-1"
            shipmentCostFormula={shipmentCostFormula}
            setShipmentCostFormula={setShipmentCostFormula}
          />
        </div>
        <DialogFooter>
          <Button
            disabled={isLoading}
            onClick={handleUpdatePlan}
            className="w-full"
          >
            {isLoading ? <Loader2 className="animate-spin" /> : "Сохранить"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default FinancialPlansEditDialog;
