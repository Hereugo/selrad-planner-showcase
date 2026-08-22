"use client";

import { FC, ReactNode, useState } from "react";
import { Separator } from "../../ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import NavigationLinks from "./navigation-links";
import NewPlanButton from "./new-plan-button";
import Filters from "./filters";
import StagingIndicator from "./staging-indicator";
import { useViewFeature } from "@/lib/hooks/useViewFeature";
import { ChevronDown } from "lucide-react";

interface SideBarProps {
  className?: string;
}

const SideBar: FC<SideBarProps> = ({ className }) => {
  const viewFeature = useViewFeature();
  return (
    <div
      className={cn("border-r-2 z-50 px-4 py-6 flex flex-col gap-4", className)}
    >
      {viewFeature.canCreateNewPlan && (
        <div className="flex shrink-0 flex-col gap-4">
          <NewPlanButton />
          <Separator orientation="horizontal" />
        </div>
      )}

      <ScrollArea type="auto" className="-mr-4 min-h-0 flex-1">
        <div className="flex flex-col gap-4 pr-4">
          <SidebarSection title="Меню" defaultOpen>
            <NavigationLinks />
          </SidebarSection>

          <Separator orientation="horizontal" />

          <Filters />
        </div>
      </ScrollArea>

      <div className="shrink-0">
        <StagingIndicator />
      </div>
    </div>
  );
};

const SidebarSection = ({
  title,
  defaultOpen = false,
  children,
}: {
  title: string;
  defaultOpen?: boolean;
  children: ReactNode;
}) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="flex flex-col gap-2">
      <button
        type="button"
        aria-expanded={isOpen}
        className="flex items-center justify-between rounded-md px-2 py-1 text-sm font-semibold text-muted-foreground hover:bg-gray-100 hover:text-foreground"
        onClick={() => setIsOpen((current) => !current)}
      >
        <span>{title}</span>
        <ChevronDown
          className={cn("h-4 w-4 transition-transform", isOpen && "rotate-180")}
        />
      </button>
      {isOpen && children}
    </div>
  );
};

export default SideBar;
