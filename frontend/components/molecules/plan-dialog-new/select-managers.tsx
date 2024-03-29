"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { useManagers } from "./index.hooks";
import { Label } from "@/components/ui/label";
import { FC } from "react";
import { managerFullName, managerShortName } from "@/lib/utils";

interface SelectManagersProps {
  id?: string;
  switchManager: (id: number) => void;
}

const SelectManagers: FC<SelectManagersProps> = ({ id, switchManager }) => {
  const { managers } = useManagers();

  return (
    <div className="grid gap-4 grid-cols-3" id={id}>
      {managers.map((manager) => (
        <div className="flex items-center gap-2" key={manager.id}>
          <Checkbox
            id={`manager-${manager.id}`}
            onClick={() => switchManager(manager.id)}
          />
          <Label
            className="font-normal hover:cursor-pointer"
            htmlFor={`manager-${manager.id}`}
            title={managerFullName(manager)}
          >
            {managerShortName(manager)}
          </Label>
        </div>
      ))}
    </div>
  );
};

export default SelectManagers;
