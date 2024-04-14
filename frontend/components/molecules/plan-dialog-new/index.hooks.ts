import { useToast } from "@/components/ui/use-toast";
import { useClientsQuery } from "@/lib/backend/clients";
import { useManagersQuery } from "@/lib/backend/managers";
import { usePlanCreateMutation } from "@/lib/backend/plans";
import { useWorklistsQuery } from "@/lib/backend/worklist";
import { formatClientName } from "@/lib/utils";
import { useEffect, useState } from "react";
import { highlightPlanRow } from "../plan-dialog-edit/index.hooks";

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

export const useCreatePlan = () => {
  const { toast } = useToast();

  const [assigned_date, setAssignedDate] = useState<string>();
  const [client, setClient] = useState<string>();
  const [selectedManagers, setSelectedManagers] = useState<number[]>([]);
  const [selectedWorklist, setSelectedWorklist] = useState<string[]>([]);
  const [shipmentCost, setShipmentCost] = useState<number>(0);
  const [comment, setComment] = useState<string>();

  const planCreateMutation = usePlanCreateMutation();
  const [isOpen, setIsOpen] = useState(false);

  const handleCreatePlan = () => {
    if (!assigned_date || !client) {
      toast({
        title: "Ошибка при создании плана",
        description: "Заполните хотя бы дату и клиента",
      });
      return;
    }

    return planCreateMutation.mutate({
      assigned_date: assigned_date,
      client: client,
      managers: selectedManagers || [],
      worklist: selectedWorklist || [],
      shipment_cost: shipmentCost ?? 0,
      comment: comment ?? "",
    });
  };

  const switchManager = (manager: number) => {
    setSelectedManagers((prev) => {
      if (prev.includes(manager)) {
        return prev.filter((m) => m !== manager);
      } else {
        return [...prev, manager];
      }
    });
  };

  const switchWork = (work: string) => {
    setSelectedWorklist((prev) => {
      if (prev.includes(work)) {
        return prev.filter((w) => w !== work);
      } else {
        return [...prev, work];
      }
    });
  };

  useEffect(() => {
    if (planCreateMutation.isError) {
      toast({
        title: "Ошибка",
        description: "Ошибка при создании плана",
      });
    }
  }, [planCreateMutation.isError, toast]);

  useEffect(() => {
    if (planCreateMutation.isSuccess) {
      toast({
        title: "Успех",
        description: "Предложение успешно создано",
      });

      setIsOpen(false);
      highlightPlanRow(planCreateMutation.data?.data as Plan);

      // reset all fields
      setAssignedDate(undefined);
      setClient(undefined);
      setSelectedManagers([]);
      setSelectedWorklist([]);
      setShipmentCost(0);
      setComment(undefined);
    }
  }, [planCreateMutation.isSuccess, toast, setIsOpen]);

  return {
    isOpen,
    selectedManagers,
    selectedWorklist,
    setIsOpen,
    setAssignedDate,
    setClient,
    switchManager,
    switchWork,
    shipmentCost,
    setShipmentCost,
    setComment,
    handleCreatePlan,
    isSuccess: planCreateMutation.isSuccess,
    isLoading: planCreateMutation.isLoading,
  };
};
