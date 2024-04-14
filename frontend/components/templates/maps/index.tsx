"use client";

import React, { FC } from "react";
import { Polygon, Placemark, YMaps, Map } from "@pbe/react-yandex-maps";
import { useMaps } from "./index.hooks";
import PlanDialogEdit from "@/components/molecules/plan-dialog-edit";
import { Button } from "@/components/ui/button";
import { CircleXIcon, Earth, PackageOpenIcon, PenBoxIcon } from "lucide-react";
import { cn, formatPrice, managerFullName } from "@/lib/utils";
import { TengeReciept } from "@/components/icons/tenge-reciept";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import SelectManager from "./select-manager";

interface MapsTemplateProps {}

const MapsTemplate: FC<MapsTemplateProps> = () => {
  const { mapElementRef, setSelectedManager } = useMaps();

  return (
    <div className="flex flex-col h-full gap-4">
      <SelectManager onSelect={setSelectedManager} />
      <div
        className="flex-1 h-full rounded-lg overflow-clip duration-300"
        style={{ minHeight: "500px" }}
        ref={mapElementRef}
      />
    </div>
  );
};

export default MapsTemplate;
