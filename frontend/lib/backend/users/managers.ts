import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchWithAuth, patchWithAuth } from "../httpCalls";
import urls from "../urls";

export const useManagersQuery = () => {
  const url = urls.base_backend.managers;

  return useQuery({
    queryKey: ["useManagersQuery"],
    queryFn: async () => fetchWithAuth<Manager[]>(url),
  });
};

export const useWarehousersQuery = () => {
  const url = urls.base_backend.warehousers;

  return useQuery({
    queryKey: ["useWarehousersQuery"],
    queryFn: async () => fetchWithAuth<Manager[]>(url),
  });
};

export const useDriversQuery = () => {
  const url = urls.base_backend.drivers;

  return useQuery({
    queryKey: ["useDriversQuery"],
    queryFn: async () => fetchWithAuth<Manager[]>(url),
  });
};

export const useUserUpdateMutation = (id: string) => {
  const queryClient = useQueryClient();

  const url = urls.base_backend.users;
  const urlParamed = `${url}/${id}/`;

  const call = (user: Partial<User>) => {
    return patchWithAuth(urlParamed, user);
  };

  return useMutation(call, {
    onSuccess: () => {
      queryClient.invalidateQueries(["useManagersQuery"]);
    },
  });
};
