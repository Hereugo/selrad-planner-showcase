"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { FC } from "react";
import { useWorks } from "./index.hooks";
import { toTitle } from "@/lib/utils";

interface SelectWorkItemProps {
  id?: string;
  switchWork: (id: WorkItem["id"]) => void;
  selectedWorkItem: string[]; // todo: rename to selectedWorkItems
}

const SelectWorkItem: FC<SelectWorkItemProps> = ({
  id,
  switchWork,
  selectedWorkItem,
}) => {
  const { workItems } = useWorks();

  return (
    <div className="grid gap-4 grid-cols-3" id={id}>
      {workItems.map((workItem) => (
        <div className="flex items-center gap-2" key={workItem.id}>
          <Checkbox
            id={`workItem-${workItem.id}`}
            onClick={() => switchWork(workItem.id)}
            checked={selectedWorkItem.includes(workItem.id)}
          />
          <Label
            className="font-normal hover:cursor-pointer"
            htmlFor={`workItem-${workItem.id}`}
            title={workItem.description}
          >
            {toTitle(workItem.name)}
          </Label>
        </div>
      ))}
    </div>
  );
};

export default SelectWorkItem;
