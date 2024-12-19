import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import urls from "../urls";
import { fetchWithAuth, patchWithAuth } from "../httpCalls";

export const usePaymentRegistriesQuery = () => {
  const url = urls.base_backend.payment_registries;

  return useQuery(["usePaymentRegistriesQuery"], async () =>
    fetchWithAuth<PaymentRegistry[]>(url),
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
      queryClient.invalidateQueries(["usePaymentRegistryUpdateMutation"]);
    },
  });
};
