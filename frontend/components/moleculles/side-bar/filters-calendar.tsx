import { Input } from "@/components/ui/input";
import { CalendarIcon } from "lucide-react";

const CalendarFilters = () => {
    return (
        <div className="flex flex-col gap-2">
            <div className="flex flex-row items-center ">
                <CalendarIcon className="-mr-4 z-10 translate-x-1/2 text-muted-foreground w-4 h-4" />
                <Input placeholder="Начальная дата" className="pl-8" />
            </div>
            <span className="text-center text-sm">
                по
            </span>
            <div className="flex flex-row items-center ">
                <CalendarIcon className="-mr-4 z-10 translate-x-1/2 text-muted-foreground w-4 h-4" />
                <Input placeholder="Конечная дата" className="pl-8" />
            </div>
        </div>
    )
}

export default CalendarFilters;