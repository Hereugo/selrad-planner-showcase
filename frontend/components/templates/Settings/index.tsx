"use client";

import { useViewFeature } from "@/lib/hooks/useViewFeature";
import PaymentSettings from "./payment-settings";

const SettingsTemplate = () => {
  const viewFeature = useViewFeature();

  return (
    <div>
      <h1 className="text-2xl font-bold">Настройки</h1>

      {viewFeature.canViewPaymentSettings && <PaymentSettings />}
    </div>
  );
};
export default SettingsTemplate;
