import useFiltersContext from "@/components/molecules/side-bar/index.providers";
import {
  usePaymentRegistriesQuery,
  usePaymentRegistryUpdateMutation,
} from "@/lib/backend/payment_registries";
import { formatDateBackend, getLastSundayDate, minDate } from "@/lib/utils";
import { useState } from "react";

export const usePaymentRegistries = () => {
  const { calendarRange, managerId } = useFiltersContext();
  //const lastSunday = getLastSundayDate();
  //const startDate = formatDateBackend(
  //  minDate([calendarRange?.from, lastSunday]),
  //);
  //const endDate = formatDateBackend(minDate([calendarRange?.to, lastSunday]));

  const startDate = formatDateBackend(calendarRange?.from);
  const endDate = formatDateBackend(calendarRange?.to);

  const { isLoading, isError, data } = usePaymentRegistriesQuery({
    managers: managerId ? [managerId] : undefined,
    start_date: startDate,
    end_date: endDate,
  });

  return {
    isLoading,
    isError,
    paymentRegistries: data?.data || [],
  };
};

export const useUpdatePaymentRegistry = (
  initialPaymentRegistry: PaymentRegistry,
  callback: () => void,
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
    paymentRegistryUpdateMutation.mutate({
      payment,
      bonus,
      comment,
      is_confirmed: isConfirmed,
    });

    callback();
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
