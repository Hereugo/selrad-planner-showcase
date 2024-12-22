import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import urls from "../urls";
import { fetchWithAuth, patchWithAuth } from "../httpCalls";

interface PaymentRegistryQueryProps {
  start_date?: string;
  end_date?: string;
  managers?: string[];
}

export const usePaymentRegistriesQuery = (props: PaymentRegistryQueryProps) => {
  const url = urls.base_backend.payment_registries;
  const queryParams = [];

  if (props.start_date) queryParams.push(`start_date=${props.start_date}`);
  if (props.end_date) queryParams.push(`end_date=${props.end_date}`);
  if (props.managers) queryParams.push(`managers=${props.managers.join(",")}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return useQuery(["usePaymentRegistriesQuery", urlWithParams], async () =>
    fetchWithAuth<PaymentRegistry[]>(urlWithParams),
  );
};

export const usePaymentRegistryQuery = (id: PaymentRegistry["id"]) => {
  const url = urls.base_backend.payment_registries;
  const urlParamed = `${url}/${id}/`;

  return useQuery(["usePaymentRegistriesQuery"], async () =>
    fetchWithAuth<PaymentRegistry>(urlParamed),
  );
};

export const usePaymentRegistryUpdateMutation = (id: string) => {
  const queryClient = useQueryClient();

  const url = urls.base_backend.payment_registries;
  const urlParamed = `${url}/${id}/`;

  const call = (paymentRegister: Partial<PaymentRegistry>) => {
    return patchWithAuth(urlParamed, paymentRegister);
  };

  return useMutation(call, {
    onSuccess: () => {
      queryClient.invalidateQueries(["usePaymentRegistriesQuery"]);
    },
  });
};
