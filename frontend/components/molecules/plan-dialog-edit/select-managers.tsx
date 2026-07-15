"use client";

import { FC } from "react";
import { useManagers } from "./index.hooks";
import SharedSelectManagers, {
  SelectManagersProps,
} from "../shared/select-managers";

const SelectManagers: FC<Omit<SelectManagersProps, "allManagers">> = (
  props,
) => {
  const { managers } = useManagers();

  return <SharedSelectManagers {...props} allManagers={managers} />;
};

export default SelectManagers;
