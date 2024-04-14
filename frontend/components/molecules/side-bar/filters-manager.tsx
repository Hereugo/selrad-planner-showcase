"use client";

import useFiltersContext from "./index.providers";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn, managerFullName, toTitle } from "@/lib/utils";
import { useManagers } from "../plan-dialog-edit/index.hooks";

const ManagerFilter = () => {
  const { managerId, setManagerId } = useFiltersContext();
  const { managers } = useManagers();

  return (
    <div className="flex flex-col">
      <Label className="text-sm">Менеджер</Label>
      <Select value={managerId} onValueChange={setManagerId}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Не выбрано" />
        </SelectTrigger>
        <SelectContent side="right">
          <SelectItem key={-1} value={"-1"}>
            Не выбрано
          </SelectItem>
          {managers.map((manager) => (
            <SelectItem key={manager.id} value={manager.id}>
              {managerFullName(manager)}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

export default ManagerFilter;
