"use client";

import { useManagers } from "@/components/molecules/plan-dialog-edit/index.hooks";
import { Input } from "@/components/ui/input";
import { managerFullName } from "@/lib/utils";

const SettingsTemplate = () => {
  const { managers } = useManagers();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Настройки выплат</h1>

      <div className="bg-white rounded-lg border max-w-md">
        {managers.map((manager) => (
          <div
            key={manager.id}
            className="flex items-center justify-between px-4 py-2 border-b border-gray-200 last:border-none"
          >
            <div>{managerFullName(manager)}</div>
            <Input className="w-30" value={100} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default SettingsTemplate;
