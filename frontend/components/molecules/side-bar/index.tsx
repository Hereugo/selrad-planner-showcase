"use client";

import { FC } from "react";
import { Separator } from "../../ui/separator";
import { cn } from "@/lib/utils";
import NavigationLinks from "./navigation-links";
import NewPlanButton from "./new-plan-button";
import Filters from "./filters";
import { useMeQuery } from "@/lib/backend/users";

interface SideBarProps {
  className?: string;
}

const SideBar: FC<SideBarProps> = ({ className }) => {
  const { data: me } = useMeQuery();

  return (
    <div className={cn("border-r-2 z-50 px-4 py-6", className)}>
      <NewPlanButton className={me?.data.is_accountant ? "hidden" : ""} />

      <Separator
        orientation="horizontal"
        className={cn("my-4", me?.data.is_accountant ? "hidden" : "")}
      />

      <NavigationLinks />

      <Separator orientation="horizontal" className="my-4" />

      <Filters />
    </div>
  );
};

export default SideBar;
