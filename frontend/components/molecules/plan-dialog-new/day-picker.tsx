"use client";

import { format } from "date-fns";
import { ru } from "date-fns/locale";
import { FC } from "react";
import { Calendar as CalendarIcon } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

interface DayPickerProps {
  id?: string;
  assignedDate?: string;
  setAssignedDate: (date: string) => void;
}

const DayPicker: FC<DayPickerProps> = ({
  id,
  assignedDate,
  setAssignedDate,
}) => {
  const date = assignedDate ? new Date(assignedDate) : undefined;
  const setDate = (date: Date) => setAssignedDate(format(date, "yyyy-MM-dd"));

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          id={id}
          variant={"outline"}
          className={cn(
            "w-full justify-start text-left font-normal",
            !date && "text-muted-foreground",
          )}
        >
          <CalendarIcon className="mr-2 h-4 w-4" />
          {date ? (
            format(date, "PPP", { locale: ru })
          ) : (
            <span>Выбрать дату</span>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0">
        <Calendar
          mode="single"
          locale={ru}
          selected={date}
          onSelect={setDate}
          initialFocus
        />
      </PopoverContent>
    </Popover>
  );
};

export default DayPicker;
