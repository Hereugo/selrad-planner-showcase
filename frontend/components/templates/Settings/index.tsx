"use client";

import { useManagers } from "@/components/molecules/plan-dialog-edit/index.hooks";
import { Input } from "@/components/ui/input";
import { cn, managerFullName } from "@/lib/utils";
import { useManagerPayment } from "./index.hooks";
import { Button } from "@/components/ui/button";
import { FC } from "react";
import { Save } from "lucide-react";

const SettingsTemplate = () => {
  const { managers } = useManagers();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Настройки выплат</h1>

      <div className="bg-white rounded-lg border max-w-md">
        {managers.map((manager) => (
          <div
            key={manager.id}
            className="flex items-center justify-between px-4 gap-4 py-2 border-b border-gray-200 last:border-none"
          >
            <div className="w-40">{managerFullName(manager)}</div>
            <UserPaymnetInput manager={manager} />
          </div>
        ))}
      </div>
    </div>
  );
};

interface UserPaymnetInputProps {
  manager: Manager;
}

const UserPaymnetInput: FC<UserPaymnetInputProps> = ({ manager }) => {
  const { payment, setPayment, isEditted, handleUpdateManagerPayment } =
    useManagerPayment(manager);

  return (
    <div className="flex items-center gap-4">
      <Input
        className="w-20"
        type="number"
        value={payment}
        onChange={(e) => setPayment(parseInt(e.target.value))}
      />
      <Button
        disabled={!isEditted}
        className="text-white bg-accent-foreground w-30 disabled:opacity-0"
        onClick={handleUpdateManagerPayment}
      >
        <Save className="w-5 h-5" />
      </Button>
    </div>
  );
};

export default SettingsTemplate;
