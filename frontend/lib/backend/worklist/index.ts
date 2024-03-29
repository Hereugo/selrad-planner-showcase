import { useQuery } from "@tanstack/react-query";
import urls from "../urls";
import { fetchWithAuth } from "../httpCalls";

export const useWorklistsQuery = () => {
    const url = urls.base_backend.worklist;

    return useQuery(['useWorklistQuery'], async () => fetchWithAuth<Work[]>(url));
};