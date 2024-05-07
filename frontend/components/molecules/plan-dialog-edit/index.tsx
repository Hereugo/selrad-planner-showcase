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
import { useDeletePlan, useUpdatePlan } from "./index.hooks";
import { Loader2, Trash2 } from "lucide-react";
import { Separator } from "@/components/ui/separator";

interface PlanDialogEditProps {
  plan: Plan;
  children: ReactNode;
}

const PlanDialogEdit: FC<PlanDialogEditProps> = ({ children, plan }) => {
  const {
    assignedDate,
    setAssignedDate,
    client,
    setClient,
    managers,
    switchManager,
    worklist,
    switchWork,
    shipmentCost,
    setShipmentCost,
    boxCount,
    setBoxCount,
    comment,
    setComment,
    handleUpdatePlan,
    isOpen,
    setIsOpen,
    isLoading,
  } = useUpdatePlan(plan);

  const { handleDeletePlan } = useDeletePlan(plan);

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle className="mb-4">Изменить план</DialogTitle>
          <div className="flex flex-row gap-4">
            <div className="flex flex-col gap-4 flex-1  w-[calc((48rem-8rem)/2)]">
              <div>
                <Label htmlFor="assigned_date">Дата</Label>
                <DayPicker
                  id="assigned_date"
                  assignedDate={assignedDate}
                  setAssignedDate={setAssignedDate}
                />
              </div>

              <div>
                <Label htmlFor="client">Клиент</Label>
                <ClientPicker
                  id="client"
                  client={client}
                  setClient={setClient}
                />
              </div>

              <div className="flex gap-4 flex-row justify-stretch w-full">
                <ShipmentCostInput
                  id="shipment_cost"
                  className="flex-1"
                  shipmentCost={shipmentCost}
                  setShipmentCost={setShipmentCost}
                />
                <BoxCountInput
                  id="box_count"
                  className="flex-1"
                  boxCount={boxCount}
                  setBoxCount={setBoxCount}
                />
              </div>
            </div>
            <Separator orientation="vertical" />
            <div className="flex flex-col gap-4 flex-1  w-[calc((48rem-8rem)/2)]">
              <div className="flex flex-col gap-2">
                <Label htmlFor="managers">Менеджеры</Label>
                <SelectManagers
                  id="managers"
                  managers={managers}
                  switchManager={switchManager}
                />
              </div>

              <div className="flex flex-col gap-2">
                <Label htmlFor="worklist">Работы</Label>
                <SelectWorkList
                  id="worklist"
                  worklist={worklist}
                  switchWork={switchWork}
                />
              </div>
            </div>
          </div>
          <div>
            <Label htmlFor="comment">Комментарии</Label>
            <CommentInput
              id="comment"
              comment={comment}
              setComment={setComment}
            />
          </div>
        </DialogHeader>
        <DialogFooter>
          <Button
            disabled={isLoading}
            onClick={handleUpdatePlan}
            className="w-full"
          >
            {isLoading ? <Loader2 className="animate-spin" /> : "Сохранить"}
          </Button>
          <Button
            disabled={isLoading}
            onClick={handleDeletePlan}
            variant="destructive"
            className="w-10 h-10 p-3"
          >
            <Trash2 />
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default PlanDialogEdit;
