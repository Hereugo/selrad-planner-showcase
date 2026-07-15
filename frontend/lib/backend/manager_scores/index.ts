import { useQuery } from "@tanstack/react-query";
import urls from "../urls";
import { fetchWithAuth } from "../httpCalls";

export const useManagerScoresQuery = (
  date: string | undefined,
  clientId: string | undefined,
  planId?: string | undefined,
) => {
  const params = new URLSearchParams();
  if (date) params.append("date", date);
  if (clientId) params.append("client_id", clientId);
  if (planId) params.append("plan_id", planId);
  const url = `${urls.base_backend.manager_scores}/?${params.toString()}`;

  return useQuery({
    queryKey: ["useManagerScoresQuery", date, clientId, planId],
    queryFn: async () => fetchWithAuth<ManagerScore[]>(url),
    enabled: !!date && !!clientId,
    staleTime: 5 * 60 * 1000,
  });
};
