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

export const useMetaClientsQuery = () => {
  const url = urls.base_backend.meta_clients;

  return useQuery(["useMetaClientsQuery"], async () =>
    fetchWithAuth<MetaClient[]>(url),
  );
};

export interface ClientCreateMutationProps {
  name: string;
  meta_client_id?: string;
  meta_client_name?: string;
  address: {
    street: string;
    twogis_link?: string;
    lat: number;
    lon: number;
  };
}

export const useClientCreateMutation = () => {
  const queryClient = useQueryClient();

  const url = urls.base_backend.clients + "/";

  const call = (client: ClientCreateMutationProps) => {
    return postWithAuth<Client>(url, client);
  };

  return useMutation(call, {
    onSuccess: () => {
      queryClient.invalidateQueries(["useClientsQuery"]);
      queryClient.invalidateQueries(["useMetaClientsQuery"]);
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
