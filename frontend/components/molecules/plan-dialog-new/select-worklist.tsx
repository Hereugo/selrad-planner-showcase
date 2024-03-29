"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { FC } from "react";
import { useWorks } from "./index.hooks";

interface SelectWorklistProps {
  id?: string;
  switchWork: (id: string) => void;
}

const SelectWorkList: FC<SelectWorklistProps> = ({ id, switchWork }) => {
  const { worklist } = useWorks();

  return (
    <div className="grid gap-4 grid-cols-3" id={id}>
      {worklist.map((work) => (
        <div className="flex items-center gap-2" key={work.pk}>
          <Checkbox
            id={`work-${work.pk}`}
            onClick={() => switchWork(work.pk)}
          />
          <Label
            className="font-normal hover:cursor-pointer"
            htmlFor={`work-${work.pk}`}
            title={work.description}
          >
            {work.name}
          </Label>
        </div>
      ))}
    </div>
  );
};

export default SelectWorkList;
