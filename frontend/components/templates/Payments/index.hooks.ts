import {
  usePaymentRegistriesQuery,
  usePaymentRegistryUpdateMutation,
} from "@/lib/backend/payment_registries";
import { useState } from "react";

export const usePaymentRegistries = () => {
  const { isLoading, isError, data } = usePaymentRegistriesQuery();

  return {
    isLoading,
    isError,
    paymentRegistries: data?.data || [],
  };
};

export const useUpdatePaymentRegistry = (
  initialPaymentRegistry: PaymentRegistry,
) => {
  const [payment, setPayment] = useState(initialPaymentRegistry.payment);
  const [bonus, setBonus] = useState(initialPaymentRegistry.bonus);
  const [comment, setComment] = useState(initialPaymentRegistry.comment);
  const [isConfirmed, setIsConfirmed] = useState(
    initialPaymentRegistry.is_confirmed,
  );

  const paymentRegistryUpdateMutation = usePaymentRegistryUpdateMutation(
    initialPaymentRegistry.id,
  );

  const handleUpdatePaymentRegistry = () => {
    return paymentRegistryUpdateMutation.mutate({
      payment,
      bonus,
      comment,
      is_confirmed: isConfirmed,
    });
  };

  return {
    payment,
    setPayment,
    bonus,
    setBonus,
    comment,
    setComment,
    isConfirmed,
    setIsConfirmed,
    handleUpdatePaymentRegistry,
  };
};
