import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchWithAuth, postWithAuth } from "../httpCalls";
import urls from "../urls";

export const useManagersQuery = () => {
  const url = urls.base_backend.managers;

  return useQuery(["useManagersQuery"], async () =>
    fetchWithAuth<Manager[]>(url),
  );
};

export const useManagerQuery = (id: string) => {
  const url = urls.base_backend.managers;
  const urlParamed = `${url}/${id}/`;

  return useQuery(["useManagerQuery", id], async () =>
    fetchWithAuth<Manager>(urlParamed),
  );
};

interface managerCreateMutationProps extends Omit<Manager, "id"> {}

export const useManagerCreateMutation = () => {
  const queryClient = useQueryClient();

  const url = urls.base_backend.managers + "/";

  const call = (manager: managerCreateMutationProps) => {
    return postWithAuth(url, manager);
  };

  return useMutation(call, {
    onSuccess: () => {
      queryClient.invalidateQueries(["useManagersQuery"]);
    },
  });
};
