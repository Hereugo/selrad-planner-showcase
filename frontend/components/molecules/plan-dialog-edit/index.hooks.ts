import axios from "axios";
import { useToast } from "@/components/ui/use-toast";
import { useClientsQuery } from "@/lib/backend/clients";
import {
  usePlanDeleteMutation,
  usePlanUpdateMutation,
} from "@/lib/backend/plans";
import { useWorkItemsQuery } from "@/lib/backend/work_items";
import { formatClientName, generateAccountantComment } from "@/lib/utils";
import { useEffect, useState } from "react";
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

export const highlightPlanRow = (plan: Plan, attempts = 3) => {
  try {
    const row = document.getElementById(`plan-row-${plan.id}`);
    if (row) {
      setTimeout(() => {
        row.classList.add("bg-blue-100");
      }, 200);
      setTimeout(() => {
        row.classList.remove("bg-blue-100");
      }, 1500);
    } else {
      throw new Error("Row not found");
    }
  } catch (e) {
    console.error(e);
    if (attempts > 0) {
      setTimeout(() => {
        highlightPlanRow(plan, attempts - 1);
      }, 500);
    }
  }
};

export const useUpdatePlan = (initialPlan: Plan) => {
  const { toast } = useToast();
  const { data: allWorkItems } = useWorkItemsQuery();
  const { data: allClients } = useClientsQuery();

  const [isOpen, setIsOpen] = useState(false);
  const [assignedDate, setAssignedDate] = useState(initialPlan.assigned_date);
  const [client, setClient] = useState(initialPlan.client.id);
  const [managers, setManagers] = useState(
    initialPlan.managers.map((manager) => manager.id),
  );
  const [workItems, setWorkItems] = useState<WorkItem["id"][]>(
    initialPlan.work_items.map((workItem) => workItem.id),
  );
  const [shipmentCostFormula, setShipmentCostFormula] = useState(
    initialPlan.shipment_cost_formula,
  );
  const [boxCount, setBoxCount] = useState(initialPlan.box_count);
  const [comment, setComment] = useState(initialPlan.comment);
  const [invoiceDate, setInvoiceDate] = useState<Plan["invoice_date"]>(
    initialPlan.invoice_date,
  );
  const [accountantComment, setAccountantComment] = useState(
    initialPlan.accountant_comment,
  );

  const planUpdateMutation = usePlanUpdateMutation(initialPlan.id);

  const isReturn = workItems.some((id) => {
    return allWorkItems?.data.some(
      (workItem) => workItem.id === id && workItem.content_type === "Return",
    );
  });
  const isShipment = workItems.some((id) => {
    return allWorkItems?.data.some(
      (workItem) => workItem.id === id && workItem.content_type === "Shipment",
    );
  });
  const isAccountant = isReturn || isShipment;

  const switchManager = (manager: string) => {
    setManagers((prev) => {
      if (prev.includes(manager)) {
        return prev.filter((m) => m !== manager);
      } else {
        return [...prev, manager];
      }
    });
  };

  const switchWork = (id: WorkItem["id"]) => {
    setWorkItems((prev) => {
      if (prev.includes(id)) {
        return prev.filter((w) => w !== id);
      } else {
        return [...prev, id];
      }
    });
  };

  const handleUpdatePlan = () => {
    if (!assignedDate || !client) {
      toast({
        title: "Ошибка при создании плана",
        description: "Заполните хотя бы дату и клиента",
      });
      return;
    }

    return planUpdateMutation.mutate({
      assigned_date: assignedDate,
      client: client,
      managers: managers || [],
      work_items: workItems || [],
      shipment_cost_formula: shipmentCostFormula,
      box_count: boxCount ?? 0,
      comment: comment ?? "",
      invoice_date: invoiceDate,
      accountant_comment: accountantComment,
    });
  };

  useEffect(() => {
    if (planUpdateMutation.isError) {
      toast({
        title: "Ошибка",
        description: axios.isAxiosError(planUpdateMutation.error)
          ? planUpdateMutation.error.response?.data.error ||
            "Ошибка при изменении плана"
          : "Ошибка при изменении плана",
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

  useEffect(() => {
    if (!invoiceDate && assignedDate && isAccountant) {
      setInvoiceDate(assignedDate);
    }
    if (!isAccountant) {
      setInvoiceDate(undefined);
    }
  }, [invoiceDate, assignedDate, isAccountant, workItems]);

  useEffect(() => {
    if (!isAccountant) {
      setAccountantComment("");
    }
  }, [isAccountant]);

  useEffect(() => {
    const invoiceSum = shipmentCostFormula.split("+").reduce((acc, cur) => {
      const num = Number(cur);
      if (isNaN(num)) {
        return acc;
      }
      return acc + num;
    }, 0);
    const invoiceCount = shipmentCostFormula.split("+").length ?? 0;

    const newComment = generateAccountantComment({
      isReturn,
      isShipment,
      invoiceSum,
      invoiceCount,
      client: allClients?.data.find((c) => c.id === client),
      hasManager: managers.length > 0,
    });

    setAccountantComment(newComment);
  }, [shipmentCostFormula, client, allClients, managers, isReturn, isShipment]);

  return {
    assignedDate,
    setAssignedDate,
    client,
    setClient,
    managers,
    workItems,
    shipmentCostFormula,
    setShipmentCostFormula,
    boxCount,
    setBoxCount,
    comment,
    setComment,
    invoiceDate,
    setInvoiceDate,
    accountantComment,
    setAccountantComment,
    isAccountant,
    switchManager,
    switchWork,
    handleUpdatePlan,
    isOpen,
    setIsOpen,
    isLoading: planUpdateMutation.isLoading,
  };
};

export const useDeletePlan = (plan: Plan) => {
  const { toast } = useToast();

  const planDeleteMutation = usePlanDeleteMutation(plan.id);

  const handleDeletePlan = () => {
    return planDeleteMutation.mutate();
  };

  useEffect(() => {
    if (planDeleteMutation.isError) {
      toast({
        title: "Ошибка",
        description: axios.isAxiosError(planDeleteMutation.error)
          ? planDeleteMutation.error.response?.data.error ||
            "Ошибка при удалении плана"
          : "Ошибка при удалении плана",
      });
    }
  }, [planDeleteMutation.isError, toast]);

  useEffect(() => {
    if (planDeleteMutation.isSuccess) {
      toast({
        title: "Успех",
        description: "Предложение успешно удалено",
      });

      highlightPlanRow(plan);
    }
  }, [planDeleteMutation.isSuccess, toast]);

  return {
    handleDeletePlan,
  };
};
