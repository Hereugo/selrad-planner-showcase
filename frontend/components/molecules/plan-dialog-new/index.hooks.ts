import axios from "axios";
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
  const [selectedWorklist, setSelectedWorklist] = useState<string[]>([]);
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
      worklist: selectedWorklist || [],
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
      setSelectedWorklist([]);
      setShipmentCostFormula(undefined);
      setBoxCount(undefined);
      setComment(undefined);
    }
  }, [planCreateMutation.isSuccess, toast, setIsOpen]);

  return {
    isOpen,
    selectedManagers,
    selectedWorklist,
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
