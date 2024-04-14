"use client";

import React, { FC } from "react";
import { useMaps } from "./index.hooks";
import SelectManager from "./select-manager";
import SelectedPlan from "./selected-plan";

interface MapsTemplateProps {}

const MapsTemplate: FC<MapsTemplateProps> = () => {
  const {
    mapElementRef,
    selectedManager,
    selectedPlanId,
    setSelectedPlanId,
    setSelectedManager,
  } = useMaps();

  return (
    <div className="flex flex-col h-full gap-4">
      <SelectManager
        onSelect={setSelectedManager}
        selectedManager={selectedManager}
      />
      <div className="flex flex-1">
        <div
          className="flex-1 h-full rounded-lg overflow-clip duration-300"
          style={{ minHeight: "500px" }}
          ref={mapElementRef}
        />
        <SelectedPlan
          planId={selectedPlanId}
          onClose={() => setSelectedPlanId(undefined)}
          className={!!selectedPlanId ? "flex-[.5]" : ""}
        />
      </div>
    </div>
  );
};

export default MapsTemplate;
