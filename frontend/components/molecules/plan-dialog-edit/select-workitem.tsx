"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { FC } from "react";
import { useWorks } from "./index.hooks";
import { toTitle } from "@/lib/utils";

interface SelectWorkItemProps {
  id?: string;
  workItems: string[];
  switchWork: (id: WorkItem["id"]) => void;
}

const SelectWorkItem: FC<SelectWorkItemProps> = ({
  id,
  workItems,
  switchWork,
}) => {
  const { workItems: allWorkItems } = useWorks();

  return (
    <div className="grid gap-4 grid-cols-3" id={id}>
      {allWorkItems.map((workItem) => (
        <div className="flex items-center gap-2" key={workItem.id}>
          <Checkbox
            id={`workItem-${workItem.id}`}
            onClick={() => switchWork(workItem.id)}
            checked={workItems.includes(workItem.id)}
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
