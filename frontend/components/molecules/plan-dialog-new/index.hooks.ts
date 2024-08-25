import axios from "axios";
import { useToast } from "@/components/ui/use-toast";
import { useClientsQuery } from "@/lib/backend/clients";
import { usePlanCreateMutation } from "@/lib/backend/plans";
import { useWorkItemsQuery } from "@/lib/backend/work_items";
import { formatClientName } from "@/lib/utils";
import { useEffect, useState } from "react";
import { highlightPlanRow } from "../plan-dialog-edit/index.hooks";
import { useManagersQuery } from "@/lib/backend/users/managers";

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

  const managers = (data?.data ?? []).sort((a, b) =>
    a.name.localeCompare(b.name),
  );

  return {
    managers,
    error,
    isLoading,
  };
};

export const useWorks = () => {
  const { data, error, isLoading } = useWorkItemsQuery();

  const workItems = data?.data ?? [];

  return {
    workItems,
    error,
    isLoading,
  };
};

interface createPlanProps {
  defaultClientId?: string;
  defaultAssignedDate?: string;
  defaultIsOpen?: boolean;
}

export const useCreatePlan = ({
  defaultClientId,
  defaultAssignedDate,
  defaultIsOpen,
}: createPlanProps) => {
  const { toast } = useToast();

  const [assignedDate, setAssignedDate] = useState<string | undefined>(
    defaultAssignedDate,
  );
  const [client, setClient] = useState<string | undefined>(defaultClientId);
  const [selectedManagers, setSelectedManagers] = useState<string[]>([]);
  const [selectedWorkItem, setSelectedWorkItem] = useState<string[]>([]);
  const [shipmentCostFormula, setShipmentCostFormula] = useState<string>();
  const [boxCount, setBoxCount] = useState<number>();
  const [comment, setComment] = useState<string>();

  const planCreateMutation = usePlanCreateMutation();
  const [isOpen, setIsOpen] = useState(defaultIsOpen || false);

  const handleCreatePlan = () => {
    if (!assignedDate || !client) {
      toast({
        title: "Ошибка при создании плана",
        description: "Заполните хотя бы дату и клиента",
      });
      return;
    }

    return planCreateMutation.mutate({
      assigned_date: assignedDate,
      client: client,
      managers: selectedManagers || [],
      work_items: selectedWorkItem || [],
      shipment_cost_formula: shipmentCostFormula ?? "0",
      box_count: boxCount ?? 0,
      comment: comment ?? "",
    });
  };

  const switchManager = (manager: string) => {
    setSelectedManagers((prev) => {
      if (prev.includes(manager)) {
        return prev.filter((m) => m !== manager);
      } else {
        return [...prev, manager];
      }
    });
  };

  const switchWork = (id: WorkItem["id"]) => {
    setSelectedWorkItem((prev) => {
      if (prev.includes(id)) {
        return prev.filter((w) => w !== id);
      } else {
        return [...prev, id];
      }
    });
  };

  useEffect(() => {
    if (planCreateMutation.isError) {
      toast({
        title: "Ошибка",
        description: axios.isAxiosError(planCreateMutation.error)
          ? planCreateMutation.error.response?.data.error ||
            "Ошибка при создании плана"
          : "Ошибка при создании плана",
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
      setSelectedWorkItem([]);
      setShipmentCostFormula(undefined);
      setBoxCount(undefined);
      setComment(undefined);
    }
  }, [planCreateMutation.isSuccess, toast, setIsOpen]);

  return {
    isOpen,
    selectedManagers,
    selectedWorkItem,
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
    isSuccess: planCreateMutation.isSuccess,
    isLoading: planCreateMutation.isLoading,
  };
};
