import axios from "axios";
import { useToast } from "@/components/ui/use-toast";
import { useClientsQuery } from "@/lib/backend/clients";
import { usePlanCreateMutation } from "@/lib/backend/plans";
import { useWorkItemsQuery } from "@/lib/backend/work_items";
import { formatClientName } from "@/lib/utils";
import { use, useEffect, useState } from "react";
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

  const { data: workItems } = useWorkItemsQuery();

  const [assignedDate, setAssignedDate] = useState<string | undefined>(
    defaultAssignedDate,
  );
  const [client, setClient] = useState<string | undefined>(defaultClientId);
  const [selectedManagers, setSelectedManagers] = useState<string[]>([]);
  const [selectedWorkItems, setSelectedWorkItems] = useState<WorkItem["id"][]>(
    [],
  );
  const [shipmentCostFormula, setShipmentCostFormula] = useState<string>();
  const [boxCount, setBoxCount] = useState<number>();
  const [comment, setComment] = useState<string>();

  const [invoiceDate, setInvoiceDate] = useState<string | undefined>(
    defaultAssignedDate,
  );
  const [accountantComment, setAccountantComment] = useState<string>();

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
      work_items: selectedWorkItems || [],
      shipment_cost_formula: shipmentCostFormula ?? "0",
      box_count: boxCount ?? 0,
      comment: comment ?? "",
      invoice_date: isAccountant ? invoiceDate : undefined,
      accountant_comment: isAccountant ? accountantComment : undefined,
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
    setSelectedWorkItems((prev) => {
      if (prev.includes(id)) {
        return prev.filter((w) => w !== id);
      } else {
        return [...prev, id];
      }
    });
  };

  const isAccountant = selectedWorkItems.some((id) => {
    return workItems?.data.some(
      (workItem) =>
        workItem.id === id &&
        (workItem.content_type === "Return" ||
          workItem.content_type === "Shipment"),
    );
  });

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
      setSelectedWorkItems([]);
      setShipmentCostFormula(undefined);
      setBoxCount(undefined);
      setComment(undefined);
      setInvoiceDate(undefined);
      setAccountantComment(undefined);
    }
  }, [planCreateMutation.isSuccess, toast, setIsOpen]);

  useEffect(() => {
    if (!invoiceDate && assignedDate && isAccountant) {
      setInvoiceDate(assignedDate);
    }
    if (!isAccountant) {
      setInvoiceDate(undefined);
    }
  }, [invoiceDate, assignedDate, isAccountant]);

  useEffect(() => {
    if (!isAccountant) {
      setAccountantComment("");
    }
  }, [isAccountant]);

  return {
    isOpen,
    selectedManagers,
    selectedWorkItems,
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
    invoiceDate,
    setInvoiceDate,
    accountantComment,
    setAccountantComment,
    handleCreatePlan,
    isAccountant: isAccountant,
    isSuccess: planCreateMutation.isSuccess,
    isLoading: planCreateMutation.isLoading,
  };
};
