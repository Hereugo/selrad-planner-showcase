"use client";

import React, { FC } from "react";
import { useMaps } from "./index.hooks";
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
