import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchWithAuth, postWithAuth } from "../httpCalls";
import urls from "../urls";

export const useClientsQuery = () => {
  const url = urls.base_backend.clients;

  return useQuery(["useClientsQuery"], async () =>
    fetchWithAuth<Client[]>(url),
  );
};

export const useClientQuery = (id: string) => {
  const url = urls.base_backend.clients;
  const urlParamed = `${url}/${id}/`;

  return useQuery(["useClientQuery", id], async () =>
    fetchWithAuth<Client>(urlParamed),
  );
};

interface clientCreateMutationProps extends Omit<Client, "id"> {}

export const useClientCreateMutation = () => {
  const queryClient = useQueryClient();

  const url = urls.base_backend.clients + "/";

  const call = (client: clientCreateMutationProps) => {
    return postWithAuth(url, client);
  };

  return useMutation(call, {
    onSuccess: () => {
      queryClient.invalidateQueries(["useClientsQuery"]);
    },
  });
};

export const useFindNearbyClientsQuery = (props: any, enabled: boolean) => {
  const url = `${urls.base_backend.clients}/${props.id}/find_nearby/`;
  const queryParams = [];

  if (props.radius) queryParams.push(`radius=${props.radius}`);
  if (props.from_date) queryParams.push(`from_date=${props.from_date}`);
  if (props.min_days_since_plan)
    queryParams.push(`min_days_since_plan=${props.min_days_since_plan}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return useQuery(
    ["useFindNearbyClientsQuery", urlWithParams],
    async () => fetchWithAuth<NearbyClient[]>(urlWithParams),
    { enabled },
  );
};

interface compareExportQueryProps {
  start_date?: string;
  end_date?: string;
  diff_year?: number;
  managers?: string[];
  work_items?: string[];
}

export const compareReportExportQuery = (props: compareExportQueryProps) => {
  const baseUrl = urls.base_backend.compare;
  const url = `${baseUrl}`;
  const queryParams = [];

  if (props.start_date) queryParams.push(`start_date=${props.start_date}`);
  if (props.end_date) queryParams.push(`end_date=${props.end_date}`);
  if (props.diff_year) queryParams.push(`diff_year=${props.diff_year}`);
  if (props.managers) queryParams.push(`managers=${props.managers.join(",")}`);
  if (props.work_items)
    queryParams.push(`work_items=${props.work_items.join(",")}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return fetchWithAuth<Blob>(urlWithParams, {
    responseType: "blob",
  });
};
