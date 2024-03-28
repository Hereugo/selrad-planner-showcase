import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import urls from "../urls";
import { deleteWithAuth, fetchWithAuth, patchWithAuth, postWithAuth } from "../httpCalls";

export const usePlansQuery = () => {
    const url = urls.base_backend.plans;

    return useQuery(['usePlansQuery'], async () => fetchWithAuth<Plan[]>(url));
}

export const usePlanQuery = (id: string) => {
    const url = urls.base_backend.plans;
    const urlParamed = `${url}/${id}/`;

    return useQuery(['usePlanQuery', id], async () => fetchWithAuth<Plan>(urlParamed));
}


interface planCreateMutationProps {
    client: string;
    name: string;
    has_products: string[];
}

export const usePlanCreateMutation = () => {
    const queryClient = useQueryClient();

    const url = urls.base_backend.plans + '/';

    const call = (plan: planCreateMutationProps) => {
        return postWithAuth(url, plan);
    };

    return useMutation(call, {
        onSuccess: () => {
            queryClient.invalidateQueries(['usePlansQuery']);
        },
    });
};



interface planUpdateMutation extends Partial<Plan> { }

export const usePlanUpdateMutation = (id: string) => {
    const queryClient = useQueryClient();

    const url = urls.base_backend.plans;
    const urlParamed = `${url}/${id}/`;

    const call = (plan: planUpdateMutation) => {
        return patchWithAuth(urlParamed, plan);
    };

    return useMutation(call, {
        onSuccess: () => {
            queryClient.invalidateQueries({
                predicate: query => query.queryKey[0] === 'usePlansQuery',
            });
        },
    });
};



export const useDeletePlanMutation = (id: string) => {
    const queryClient = useQueryClient();

    const url = urls.base_backend.plans;
    const urlParamed = `${url}/${id}/`;

    const call = () => {
        return deleteWithAuth(urlParamed);
    };

    return useMutation(call, {
        onSuccess: () => {
            queryClient.invalidateQueries(['usePlansQuery']);
        },
    });
};