"use client";

import { CalendarIcon } from "lucide-react";
import CalendarFilterPopover, { calendarOptions } from "./filters-calendar-popover";
import { Button } from "@/components/ui/button";
import useFiltersContext from "./index.providers";
import { DateRange } from "react-day-picker";
import { isSameDay } from "date-fns";

const CalendarFilters = () => {
    const { calendarRange } = useFiltersContext();

    return (
        <CalendarFilterPopover>
            <div className="flex flex-col gap-2 w-full">
                <div className="flex flex-row items-center ">
                    <CalendarIcon className="-mr-4 z-10 translate-x-1/2 text-muted-foreground w-4 h-4" />
                    <Button
                        variant="outline"
                        className="pl-8 font-normal w-full justify-start"
                    >
                        <span>{formatRange(calendarRange)}</span>
                    </Button>
                </div>
            </div>
        </CalendarFilterPopover>
    )
}

export default CalendarFilters;


const formatRange = (calendarRange: DateRange | undefined) => {
    if (!calendarRange) return 'Выберите дату';
    const { from, to } = calendarRange;

    if (!from) return 'Выберите дату';
    const fromStr = from.toLocaleDateString("ru-RU");

    if (!to) return `${fromStr} – ...`;
    const toStr = to.toLocaleDateString("ru-RU");

    const matchedLabel = calendarOptions.find((option) => {
        return isSameDay(option.from, from) && isSameDay(option.to, to);
    })?.label;

    if (matchedLabel) return matchedLabel;

    if (fromStr === toStr) return fromStr;

    return `${fromStr} – ${toStr}`;
}