"use client";

import { FC } from "react";
import PlanTable from "./plan-table";
import FinancialPlansTable from "../FinancialPlans/financial-plans-table";
import { useViewFeature } from "@/lib/hooks/useViewFeature";

interface PlansTemplateProps {}

const PlansTemplate: FC<PlansTemplateProps> = () => {
  const viewFeature = useViewFeature();

  if (viewFeature.canViewAccountant) {
    return <FinancialPlansTable />;
  }

  return <PlanTable />;
};

export default PlansTemplate;
