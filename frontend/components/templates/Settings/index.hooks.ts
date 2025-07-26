import { useUserUpdateMutation } from "@/lib/backend/users/managers";
import { useState } from "react";

export const useManagerPayment = (manager: Manager) => {
  const [payment, setPayment] = useState(manager["payment"]);
  const userUpdateMutation = useUserUpdateMutation(manager["id"]);

  const handleUpdateManagerPayment = () => {
    userUpdateMutation.mutate({
      payment,
    });
  };

  return {
    payment,
    setPayment,
    handleUpdateManagerPayment,
    isEditted: payment !== manager["payment"],
  };
};
