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
import { useManagerScoresQuery } from "@/lib/backend/manager_scores";

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
  const [plan, setPlan] = useState({
    assignedDate: initialPlan.assigned_date,
    client: initialPlan.client.id,
    managers: initialPlan.managers.map((manager) => manager.id),
    workItems: initialPlan.work_items.map((workItem) => workItem.id),
    shipmentCostFormula: initialPlan.shipment_cost_formula,
    boxCount: initialPlan.box_count,
    comment: initialPlan.comment,
    invoiceDate: initialPlan.invoice_date,
    accountantComment: initialPlan.accountant_comment,
  });

  const planUpdateMutation = usePlanUpdateMutation(initialPlan.id);

  const { data: scoresData, isLoading: scoresLoading } = useManagerScoresQuery(
    plan.assignedDate,
    plan.client,
    String(initialPlan.id),
  );
  const scores: ManagerScore[] = scoresData?.data ?? [];

  const isReturn = plan.workItems.some((id) => {
    return allWorkItems?.data.some(
      (workItem) => workItem.id === id && workItem.content_type === "Return",
    );
  });
  const isShipment = plan.workItems.some((id) => {
    return allWorkItems?.data.some(
      (workItem) => workItem.id === id && workItem.content_type === "Shipment",
    );
  });
  const isAccountant = isReturn || isShipment;

  const switchManager = (manager: string) => {
    setPlan((prev) => {
      let newPlan = {
        ...prev,
        managers: prev.managers.includes(manager)
          ? prev.managers.filter((m) => m !== manager)
          : [...prev.managers, manager],
      };

      newPlan = {
        ...newPlan,
        accountantComment: getGeneratedAccountantComment(newPlan),
      };

      return newPlan;
    });
  };

  const switchWork = (id: WorkItem["id"]) => {
    setPlan((prev) => {
      let newPlan = {
        ...prev,
        workItems: prev.workItems.includes(id)
          ? prev.workItems.filter((w) => w !== id)
          : [...prev.workItems, id],
      };

      newPlan = {
        ...newPlan,
        accountantComment: getGeneratedAccountantComment(newPlan),
      };

      return newPlan;
    });
  };

  const handleUpdatePlan = () => {
    if (!plan.assignedDate || !plan.client) {
      toast({
        title: "Ошибка при создании плана",
        description: "Заполните хотя бы дату и клиента",
      });
      return;
    }

    return planUpdateMutation.mutate({
      assigned_date: plan.assignedDate,
      client: plan.client,
      managers: plan.managers || [],
      work_items: plan.workItems || [],
      shipment_cost_formula: plan.shipmentCostFormula,
      box_count: plan.boxCount ?? 0,
      comment: plan.comment ?? "",
      invoice_date: plan.invoiceDate,
      accountant_comment: plan.accountantComment,
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
    if (!plan.invoiceDate && plan.assignedDate && isAccountant) {
      setPlan((prev) => ({ ...prev, invoiceDate: plan.assignedDate }));
    }
    if (!isAccountant) {
      setPlan((prev) => ({ ...prev, invoiceDate: undefined }));
    }
  }, [plan.invoiceDate, plan.assignedDate, isAccountant, plan.workItems]);

  useEffect(() => {
    if (!isAccountant) {
      setPlan((prev) => ({ ...prev, accountantComment: "" }));
    }
  }, [isAccountant]);

  const getGeneratedAccountantComment = (newPlan: typeof plan) => {
    const invoiceSum = newPlan.shipmentCostFormula
      .split("+")
      .reduce((acc, cur) => {
        const num = Number(cur);
        if (isNaN(num)) {
          return acc;
        }
        return acc + num;
      }, 0);
    const invoiceCount = newPlan.shipmentCostFormula.split("+").length ?? 0;
    const isReturn = newPlan.workItems.some((id) => {
      return allWorkItems?.data.some(
        (workItem) => workItem.id === id && workItem.content_type === "Return",
      );
    });
    const isShipment = newPlan.workItems.some((id) => {
      return allWorkItems?.data.some(
        (workItem) =>
          workItem.id === id && workItem.content_type === "Shipment",
      );
    });

    const newComment = generateAccountantComment({
      isReturn,
      isShipment,
      invoiceSum,
      invoiceCount,
      client: allClients?.data.find((c) => c.id === newPlan.client),
      hasManager: newPlan.managers.length > 0,
    });

    return newComment;
  };

  const handleClientChange = (client: string) => {
    setPlan((prev) => {
      let newPlan = { ...prev, client };
      newPlan = {
        ...newPlan,
        accountantComment: getGeneratedAccountantComment(newPlan),
      };
      return newPlan;
    });
  };

  const handleShipmentCostFormulaChange = (shipmentCostFormula: string) => {
    setPlan((prev) => {
      let newPlan = { ...prev, shipmentCostFormula };
      newPlan = {
        ...newPlan,
        accountantComment: getGeneratedAccountantComment(newPlan),
      };
      return newPlan;
    });
  };

  return {
    assignedDate: plan.assignedDate,
    setAssignedDate: (assignedDate: string) => {
      setPlan((prev) => ({ ...prev, assignedDate }));
    },
    client: plan.client,
    setClient: handleClientChange,
    managers: plan.managers,
    workItems: plan.workItems,
    shipmentCostFormula: plan.shipmentCostFormula,
    setShipmentCostFormula: handleShipmentCostFormulaChange,
    boxCount: plan.boxCount,
    setBoxCount: (boxCount: number) => {
      setPlan((prev) => ({ ...prev, boxCount }));
    },
    comment: plan.comment,
    setComment: (comment: string) => {
      setPlan((prev) => ({ ...prev, comment }));
    },
    invoiceDate: plan.invoiceDate,
    setInvoiceDate: (invoiceDate: string) => {
      setPlan((prev) => ({ ...prev, invoiceDate }));
    },
    accountantComment: plan.accountantComment,
    setAccountantComment: (accountantComment: string) => {
      setPlan((prev) => ({ ...prev, accountantComment }));
    },
    isAccountant,
    switchManager,
    switchWork,
    handleUpdatePlan,
    isOpen,
    setIsOpen,
    isLoading: planUpdateMutation.isLoading,
    scores,
    scoresLoading,
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
