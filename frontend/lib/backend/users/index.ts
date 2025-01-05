import { useQuery } from "@tanstack/react-query";
import { fetchWithAuth } from "../httpCalls";
import urls from "../urls";

export const useMeQuery = () => {
  const url = urls.base_backend.users.me;

  return useQuery({
    queryKey: ["useMeQuery"],
    queryFn: async () => fetchWithAuth<Me>(url),
    refetchInterval: 1000 * 60 * 60 * 24, // 24 hours
  });
};
