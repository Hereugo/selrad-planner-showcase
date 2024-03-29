"use client";

import { FC, ReactNode, useEffect, useState } from "react";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { Separator } from "@/components/ui/separator";
import { ru } from "date-fns/locale";
import {
  addDays,
  startOfISOWeek,
  startOfMonth,
  endOfMonth,
  addMonths,
  startOfYear,
  endOfYear,
  startOfToday,
} from "date-fns";
import useFiltersContext from "./index.providers";

interface CalendarFilterPopoverProps {
  children: ReactNode;
}

const CalendarFilterPopover: FC<CalendarFilterPopoverProps> = ({
  children,
}) => {
  const defaultSelected = calendarOptions[3];
  const { calendarRange, setCalendarRange } = useFiltersContext();
  const [month, setMonth] = useState(
    calendarRange?.from || defaultSelected.from,
  );

  // default selected range
  useEffect(() => {
    if (!calendarRange) setCalendarRange(defaultSelected);
  }, []);
  useEffect(() => {
    setMonth(calendarRange?.from || defaultSelected.from);
  }, [calendarRange]);

  return (
    <Popover>
      <PopoverTrigger asChild>{children}</PopoverTrigger>
      <PopoverContent side="right" asChild>
        <div className="p-4 w-[500px] h-96 bg-white shadow-lg rounded-lg z-50 flex flex-row">
          <Calendar
            locale={ru}
            mode="range"
            defaultMonth={month}
            month={month}
            onMonthChange={setMonth}
            selected={calendarRange}
            onSelect={setCalendarRange}
          />
          <Separator orientation="vertical" />
          <div className="flex flex-col gap-2 w-[200px]">
            {calendarOptions.map((option) => (
              <div
                key={option.label}
                className="flex flex-row items-center px-4 cursor-pointer"
                onClick={() => setCalendarRange(option)}
              >
                {option.label}
              </div>
            ))}
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
};

export default CalendarFilterPopover;

const today = startOfToday();
const yesterday = addDays(today, -1);
const tomorrow = addDays(today, 1);
const lastWeekStart = startOfISOWeek(addDays(today, -7));
const lastWeekEnd = addDays(lastWeekStart, 6);
const weekStart = startOfISOWeek(today);
const weekEnd = addDays(weekStart, 6);
const nextWeekStart = addDays(weekStart, 7);
const nextWeekEnd = addDays(nextWeekStart, 6);
const monthStart = startOfMonth(today);
const monthEnd = endOfMonth(today);
const lastMonthStart = startOfMonth(addMonths(today, -1));
const lastMonthEnd = endOfMonth(addMonths(today, -1));
const nextMonthStart = startOfMonth(addMonths(today, 1));
const nextMonthEnd = endOfMonth(addMonths(today, 1));
const yearStart = startOfYear(today);
const yearEnd = endOfYear(today);

export const calendarOptions = [
  { label: "Сегодня", from: today, to: today },
  { label: "Вчера", from: yesterday, to: yesterday },
  { label: "Завтра", from: tomorrow, to: tomorrow },
  { label: "Эта неделя", from: weekStart, to: weekEnd },
  { label: "Прошлая неделя", from: lastWeekStart, to: lastWeekEnd },
  { label: "Следующая неделя", from: nextWeekStart, to: nextWeekEnd },
  { label: "Этот месяц", from: monthStart, to: monthEnd },
  { label: "Прошлый месяц", from: lastMonthStart, to: lastMonthEnd },
  { label: "Следующий месяц", from: nextMonthStart, to: nextMonthEnd },
  { label: "Этот год", from: yearStart, to: yearEnd },
];
