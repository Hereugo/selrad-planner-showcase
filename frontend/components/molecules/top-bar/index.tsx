import { cn } from "@/lib/utils";
import { CalendarDays } from "lucide-react";
import Link from "next/link";
import { FC } from "react";

interface TopBarProps {
    className?: string;
}

const TopBar: FC<TopBarProps> = ({ className }) => {
    return (
        <div className={cn("border-b-2", className)}>
            <Link className="h-full text-2xl font-bold flex items-center px-6 gap-2" href="/">
                <CalendarDays />
                <span>Планировщик</span>
            </Link>
        </div>
    )
}

export default TopBar;