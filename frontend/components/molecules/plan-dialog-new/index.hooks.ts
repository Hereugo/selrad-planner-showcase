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
    const [managers, setManagers] = useState<number[]>([]);
    const [worklist, setWorklist] = useState<string[]>([]);
    const [shipment_cost, setShipmentCost] = useState<string>();
    const [box_count, setBoxCount] = useState<string>();
    const [comment, setComment] = useState<string>();

    const planCreateMutation = usePlanCreateMutation();
    const [isOpen, setIsOpen] = useState(false);

    const handleCreatePlan = () => {
        // do checking if all fields are filled
        if (
            !assigned_date ||
            !client ||
            !managers.length ||
            !worklist.length ||
            !shipment_cost ||
            !box_count
        ) {
            toast({
                title: "Ошибка при создании плана",
                description: "Заполните все поля",
            });
            return;
        }

        return planCreateMutation.mutate({
            assigned_date: assigned_date,
            client: client,
            managers: managers,
            worklist: worklist,
            shipment_cost: shipment_cost,
            box_count: box_count,
            comment: comment ?? "",
        });
    };

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
        }
    }, [planCreateMutation.isSuccess, toast, setIsOpen]);

    return {
        isOpen,
        setIsOpen,
        setAssignedDate,
        setClient,
        switchManager,
        switchWork,
        setShipmentCost,
        setBoxCount,
        setComment,
        handleCreatePlan,
        isSuccess: planCreateMutation.isSuccess,
        isLoading: planCreateMutation.isLoading,
    };
};
