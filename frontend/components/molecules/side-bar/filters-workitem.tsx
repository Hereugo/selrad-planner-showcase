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
import { cn, toTitle } from "@/lib/utils";
import { useWorks } from "../plan-dialog-edit/index.hooks";
import { useViewFeature } from "@/lib/hooks/useViewFeature";

const WorkFilter = () => {
  const viewFeature = useViewFeature();
  const { workId, setWorkId } = useFiltersContext();
  const { workItems } = useWorks();

  const handleSelectWork = (newWorkId: string) => {
    setWorkId((oldWorkId) => {
      if (newWorkId == "undefined") {
        return undefined;
      }
      if (newWorkId == "-1") {
        return newWorkId;
      }
      return newWorkId;
    });
  };

  return (
    viewFeature.canUseWorkFilter && (
      <div className="flex flex-col">
        <Label className="text-sm">Работа</Label>
        <Select value={workId || "undefined"} onValueChange={handleSelectWork}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="---" />
          </SelectTrigger>
          <SelectContent side="right">
            <SelectItem value="undefined">Все</SelectItem>
            <SelectItem value="-1">Не выбрано</SelectItem>
            {workItems.map((workItem) => (
              <SelectItem key={workItem.id} value={workItem.id}>
                {toTitle(workItem.name)}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    )
  );
};

export default WorkFilter;
