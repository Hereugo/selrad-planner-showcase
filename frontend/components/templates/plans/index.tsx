"use client";

import { FC } from "react";
import PlanTable from "./plan-table";
import { useMeQuery } from "@/lib/backend/users";
import FinancialPlansTable from "../FinancialPlans/financial-plans-table";

interface PlansTemplateProps {}

const PlansTemplate: FC<PlansTemplateProps> = () => {
  const { data: me } = useMeQuery();

  if (me?.data.is_accountant) {
    return <FinancialPlansTable />;
  }

  return <PlanTable />;
};

export default PlansTemplate;
