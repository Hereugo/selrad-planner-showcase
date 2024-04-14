import { Label } from "@/components/ui/label";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { useManagersQuery } from "@/lib/backend/managers";
import { managerFullName } from "@/lib/utils";
import { FC } from "react";

interface SelectManagerProps {
  selectedManager: Manager | undefined;
  onSelect: (manager: Manager | undefined) => void;
}

const SelectManager: FC<SelectManagerProps> = ({
  onSelect,
  selectedManager,
}) => {
  const { data } = useManagersQuery();

  const handleSelect = (managerId: string) => {
    if (managerId === "-1") {
      onSelect(undefined);
      return;
    }

    const manager = data?.data.find(
      (manager) => String(manager.id) === managerId,
    );
    if (manager) {
      onSelect(manager);
    }
  };

  return (
    <div>
      <Label>Менеджер</Label>
      <Select onValueChange={handleSelect} value={selectedManager?.id || "-1"}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="Не выбрано" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="-1">Не выбрано</SelectItem>
          {data?.data.map((manager) => (
            <SelectItem value={String(manager.id)} key={manager.id}>
              {managerFullName(manager)}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

export default SelectManager;
