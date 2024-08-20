import { useQuery } from "@tanstack/react-query";
import urls from "../urls";
import { fetchWithAuth } from "../httpCalls";

export const useWorkItemsQuery = () => {
  const url = urls.base_backend.work_items;

  return useQuery(["useWorkItemsQuery"], async () =>
    fetchWithAuth<WorkItem[]>(url),
  );
};
