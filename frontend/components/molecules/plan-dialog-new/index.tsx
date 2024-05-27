"use client";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { FC, ReactNode } from "react";
import DayPicker from "./day-picker";
import ClientPicker from "./client-picker";
import SelectManagers from "./select-managers";
import SelectWorkList from "./select-worklist";
import ShipmentCostInput from "./input-shipment-cost";
import BoxCountInput from "./input-box-count";
import CommentInput from "./input-comment";
import { useCreatePlan } from "./index.hooks";
import { Loader2 } from "lucide-react";
import { Separator } from "@/components/ui/separator";

interface PlanDialogNewProps {
  children?: ReactNode;
  defaultClientId?: string;
  defaultAssignedDate?: string;
  defaultIsOpen?: boolean;
  defaultHandleOpen?: (open: boolean) => void;
}

const PlanDialogNew: FC<PlanDialogNewProps> = ({
  children,
  defaultClientId,
  defaultAssignedDate,
  defaultIsOpen,
  defaultHandleOpen,
}) => {
  const {
    isOpen,
    setIsOpen,
    setAssignedDate,
    assignedDate,
    setClient,
    client,
    switchManager,
    switchWork,
    setShipmentCostFormula,
    setBoxCount,
    setComment,
    handleCreatePlan,
    isLoading,
    selectedManagers,
    selectedWorklist,
  } = useCreatePlan({ defaultClientId, defaultAssignedDate, defaultIsOpen });

  return (
    <Dialog
      open={isOpen}
      onOpenChange={(open) => {
        setIsOpen(open);
        if (defaultHandleOpen) defaultHandleOpen(open);
      }}
    >
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle className="mb-4">Новый план</DialogTitle>
          <div className="flex flex-row gap-4">
            <div className="flex flex-col gap-4 flex-1 w-[calc((48rem-8rem)/2)]">
              <div>
                <Label htmlFor="assigned_date">Дата</Label>
                <DayPicker
                  id="assigned_date"
                  setAssignedDate={setAssignedDate}
                  assignedDate={assignedDate}
                />
              </div>

              <div>
                <Label htmlFor="client">Клиент</Label>
                <ClientPicker
                  id="client"
                  setClient={setClient}
                  client={client}
                />
              </div>

              <div className="flex gap-4 flex-row justify-stretch w-full">
                <ShipmentCostInput
                  id="shipment_cost"
                  className="flex-1"
                  setShipmentCostFormula={setShipmentCostFormula}
                />
                <BoxCountInput
                  id="box_count"
                  className="flex-1"
                  setBoxCount={setBoxCount}
                />
              </div>
            </div>
            <Separator orientation="vertical" />
            <div className="flex flex-col gap-4 flex-1 w-[calc((48rem-8rem)/2)]">
              <div className="flex flex-col gap-2">
                <Label htmlFor="managers">Менеджеры</Label>
                <SelectManagers
                  id="managers"
                  switchManager={switchManager}
                  selectedManagers={selectedManagers}
                />
              </div>

              <div className="flex flex-col gap-2">
                <Label htmlFor="worklist">Работы</Label>
                <SelectWorkList
                  id="worklist"
                  switchWork={switchWork}
                  selectedWorklist={selectedWorklist}
                />
              </div>
            </div>
          </div>
          <div>
            <Label htmlFor="comment">Комментарии</Label>
            <CommentInput id="comment" setComment={setComment} />
          </div>
        </DialogHeader>
        <DialogFooter>
          <Button
            disabled={isLoading}
            onClick={handleCreatePlan}
            className="w-full"
          >
            {isLoading ? <Loader2 className="animate-spin" /> : "Создать"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default PlanDialogNew;
