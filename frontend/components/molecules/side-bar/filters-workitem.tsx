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

const WorkFilter = () => {
  const { workId, setWorkId } = useFiltersContext();
  const { worklist } = useWorks();

  return (
    <div className="flex flex-col">
      <Label className="text-sm">Работа</Label>
      <Select value={workId} onValueChange={setWorkId}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Не выбрано" />
        </SelectTrigger>
        <SelectContent side="right">
          <SelectItem key={-1} value={"-1"}>
            Не выбрано
          </SelectItem>
          {worklist.map((work) => (
            <SelectItem key={work.id} value={work.id}>
              {toTitle(work.name)}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

export default WorkFilter;
