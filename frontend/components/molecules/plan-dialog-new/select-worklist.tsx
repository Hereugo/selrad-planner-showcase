"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { FC } from "react";
import { useWorks } from "./index.hooks";
import { toTitle } from "@/lib/utils";

interface SelectWorklistProps {
  id?: string;
  switchWork: (id: string) => void;
  selectedWorklist: string[];
}

const SelectWorkList: FC<SelectWorklistProps> = ({
  id,
  switchWork,
  selectedWorklist,
}) => {
  const { worklist } = useWorks();

  return (
    <div className="grid gap-4 grid-cols-3" id={id}>
      {worklist.map((work) => (
        <div className="flex items-center gap-2" key={work.id}>
          <Checkbox
            id={`work-${work.id}`}
            onClick={() => switchWork(work.id)}
            checked={selectedWorklist.includes(work.id)}
          />
          <Label
            className="font-normal hover:cursor-pointer"
            htmlFor={`work-${work.id}`}
            title={work.description}
          >
            {toTitle(work.name)}
          </Label>
        </div>
      ))}
    </div>
  );
};

export default SelectWorkList;
