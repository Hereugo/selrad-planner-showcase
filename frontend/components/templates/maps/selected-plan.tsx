import { TengeReciept } from "@/components/icons/tenge-reciept";
import PlanDialogEdit from "@/components/molecules/plan-dialog-edit";
import { Button } from "@/components/ui/button";
import { useNearbyPlansQuery, usePlanQuery } from "@/lib/backend/plans";
import { cn, formatPrice, managerFullName, toTitle } from "@/lib/utils";
import { CircleXIcon, Earth, PackageOpenIcon, PenBoxIcon } from "lucide-react";
import { FC } from "react";

interface SelectedPlanProps {
  planId?: Plan["id"];
  onClose?: () => void;
  className?: string;
}

const SelectedPlan: FC<SelectedPlanProps> = ({
  planId,
  onClose,
  className,
}) => {
  const { data } = useNearbyPlansQuery({ id: planId || "" });
  const { data: planData } = usePlanQuery(planId || "");
  const plan = planData?.data;

  if (!planId || !plan) return <></>;

  return (
    <div className={cn("flex flex-col gap-4 relative pt-8 px-4", className)}>
      <div className="text-lg font-bold">
        План{" "}
        {new Date(plan.assigned_date).toLocaleString("ru-RU", {
          day: "numeric",
          month: "long",
          year: "numeric",
        })}
      </div>
      <CircleXIcon
        className="fill-red-400 stroke-red-700 w-6 h-6 cursor-pointer absolute top-2 right-0"
        onClick={onClose}
      />
      <div className="w-full">
        <div
          className="text-lg font-bold line-clamp-1 text-ellipsis"
          title={plan.client.name}
        >
          {plan.client.name}
        </div>
        <div className="text-sm text-muted-foreground line-clamp-1 text-ellipsis">
          {plan.client.addresses[0].street}
        </div>
      </div>

      <div>
        <div className="font-semibold">Менеджеры:</div>
        <div className="grid grid-cols-3">
          {plan.managers
            .sort((a, b) => a.first_name.localeCompare(b.first_name))
            .map((manager) => (
              <div key={manager.id}>{managerFullName(manager)}</div>
            ))}
        </div>
      </div>

      <div>
        <div className="font-semibold">Работы:</div>
        <div className="grid grid-cols-3">
          {plan.worklist
            .sort((a, b) => a.name.localeCompare(b.name))
            .map((work) => (
              <div key={work.id}>{toTitle(work.name)}</div>
            ))}
        </div>
      </div>

      <div>
        <div className="font-semibold">Детали:</div>
        <div className="grid grid-cols-2 items-center">
          <span className="flex items-center">
            <TengeReciept className="w-5 h-5 mr-2" />
            Сумма отгрузки
          </span>
          <span>{formatPrice(plan.shipment_cost)}</span>
        </div>
        <div className="grid grid-cols-2">
          <span className="flex items-center">
            <PackageOpenIcon className="w-5 h-5 mr-2" />
            Кол. коробок
          </span>
          <span>{plan.box_count}</span>
        </div>
      </div>

      <div className="w-full gap-2 flex flex-row">
        <PlanDialogEdit plan={plan}>
          <Button className="flex-1">
            <PenBoxIcon className="w-5 h-5 mr-2" />
            Изменить
          </Button>
        </PlanDialogEdit>

        <Button className="flex-1" onClick={() => {}}>
          <Earth className="w-5 h-5 mr-2" />
          Клиенты рядом
        </Button>
      </div>
    </div>
  );
};

export default SelectedPlan;
