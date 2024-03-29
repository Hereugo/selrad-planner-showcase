import { useToast } from "@/components/ui/use-toast";
import { useClientsQuery } from "@/lib/backend/clients";
import { useManagersQuery } from "@/lib/backend/managers";
import { usePlanUpdateMutation } from "@/lib/backend/plans";
import { useWorklistsQuery } from "@/lib/backend/worklist";
import { formatClientName } from "@/lib/utils";
import { useEffect, useState } from "react";

export const useClients = () => {
  const { data, error, isLoading } = useClientsQuery();

  const clients = (data?.data ?? [])
    .sort((a, b) => a.name.localeCompare(b.name))
    .map((client) => ({
      ...client,
      name: formatClientName(client.name),
    }));

  return {
    clients,
    error,
    isLoading,
  };
};

export const useManagers = () => {
  const { data, error, isLoading } = useManagersQuery();

  const managers = (data?.data ?? []).sort(
    (a, b) =>
      a.first_name.localeCompare(b.first_name) ||
      a.last_name.localeCompare(b.last_name),
  );

  return {
    managers,
    error,
    isLoading,
  };
};

export const useWorks = () => {
  const { data, error, isLoading } = useWorklistsQuery();

  const worklist = data?.data ?? [];

  return {
    worklist,
    error,
    isLoading,
  };
};

export const highlightPlanRow = (plan: Plan) => {
  try {
    const row = document.getElementById(`plan-row-${plan.pk}`);
    if (row) {
      setTimeout(() => {
        row.classList.add("bg-blue-100");
      }, 200);
      setTimeout(() => {
        row.classList.remove("bg-blue-100");
      }, 1500);
    }
  } catch (e) {
    console.error(e);
  }
};

export const useUpdatePlan = (initialPlan: Plan) => {
  const { toast } = useToast();

  const [isOpen, setIsOpen] = useState(false);
  const [assignedDate, setAssignedDate] = useState(initialPlan.assigned_date);
  const [client, setClient] = useState(initialPlan.client.pk);
  const [managers, setManagers] = useState(
    initialPlan.managers.map((manager) => manager.id),
  );
  const [worklist, setWorklist] = useState(
    initialPlan.worklist.map((work) => work.pk),
  );
  const [shipmentCost, setShipmentCost] = useState(initialPlan.shipment_cost);
  const [boxCount, setBoxCount] = useState(initialPlan.box_count);
  const [comment, setComment] = useState(initialPlan.comment);

  const planUpdateMutation = usePlanUpdateMutation(initialPlan.pk);

  const switchManager = (manager: number) => {
    setManagers((prev) => {
      if (prev.includes(manager)) {
        return prev.filter((m) => m !== manager);
      } else {
        return [...prev, manager];
      }
    });
  };

  const switchWork = (work: string) => {
    setWorklist((prev) => {
      if (prev.includes(work)) {
        return prev.filter((w) => w !== work);
      } else {
        return [...prev, work];
      }
    });
  };

  const handleUpdatePlan = () => {
    if (
      !assignedDate ||
      !client ||
      !managers.length ||
      !worklist.length ||
      !shipmentCost ||
      !boxCount
    ) {
      toast({
        title: "Ошибка при обновлении плана",
        description: "Заполните все поля",
      });
      return;
    }

    return planUpdateMutation.mutate({
      assigned_date: assignedDate,
      client: client,
      managers: managers,
      worklist: worklist,
      shipment_cost: shipmentCost,
      box_count: boxCount,
      comment: comment ?? "",
    });
  };

  useEffect(() => {
    if (planUpdateMutation.isError) {
      toast({
        title: "Ошибка",
        description: "Ошибка при изменении плана",
      });
    }
  }, [planUpdateMutation.isError, toast]);

  useEffect(() => {
    if (planUpdateMutation.isSuccess) {
      toast({
        title: "Успех",
        description: "Предложение успешно изменено",
      });

      setIsOpen(false);
      highlightPlanRow(planUpdateMutation.data.data);
    }
  }, [planUpdateMutation.isSuccess, toast, setIsOpen]);

  return {
    assignedDate,
    setAssignedDate,
    client,
    setClient,
    managers,
    worklist,
    shipmentCost,
    setShipmentCost,
    boxCount,
    setBoxCount,
    comment,
    setComment,
    switchManager,
    switchWork,
    handleUpdatePlan,
    isOpen,
    setIsOpen,
    isLoading: planUpdateMutation.isLoading,
  };
};
