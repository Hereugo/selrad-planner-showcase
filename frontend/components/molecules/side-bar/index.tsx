import { FC } from "react";
import { Separator } from "../../ui/separator";
import { cn } from "@/lib/utils";
import NavigationLinks from "./navigation-links";
import NewPlanButton from "./new-plan-button";
import Filters from "./filters";

interface SideBarProps {
  className?: string;
}

const SideBar: FC<SideBarProps> = ({ className }) => {
  return (
    <div className={cn("border-r-2 z-50 px-4 py-6", className)}>
      <NewPlanButton />

      <Separator orientation="horizontal" className="my-4" />

      <NavigationLinks />

      <Separator orientation="horizontal" className="my-4" />

      <Filters />
    </div>
  );
};

export default SideBar;
