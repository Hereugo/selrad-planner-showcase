import { useQuery } from "@tanstack/react-query";
import { fetchWithAuth } from "../httpCalls";
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
