import { usePaymentRegistriesQuery } from "@/lib/backend/payment_registries";

export const usePaymentRegistries = () => {
  const { isLoading, isError, data } = usePaymentRegistriesQuery();

  return {
    isLoading,
    isError,
    paymentRegistries: data?.data || [],
  };
};
