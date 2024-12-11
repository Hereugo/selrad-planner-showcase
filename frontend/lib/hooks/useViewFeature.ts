import { useMeQuery } from "../backend/users";

export const useViewFeature = () => {
  const { data } = useMeQuery();
  const me = data?.data;

  return {
    canUseWorkFilter: !me?.is_accountant,
    canViewMaps: !me?.is_accountant,
    canViewAccountant: me?.is_accountant,
    canCreateNewPlan: !me?.is_accountant,
    canExportPlans: me?.permissions.includes("plans.export_plans"),
    canExportReport: me?.permissions.includes("plans.export_report"),
    canExportDispatchList: me?.permissions.includes("plans.get_dispatch_list"),
    canExportDispatchReport: me?.permissions.includes(
      "plans.get_dispatch_report",
    ),
    canExportCompareReport: me?.permissions.includes(
      "clients.export_compare_years",
    ),
    canDeletePlan: me?.permissions.includes("plans.delete_plans"),
    canDeleteOldPlan: me?.permissions.includes("plans.delete_old_plan"),
    canUpdateOldPlan: me?.permissions.includes("plans.change_old_plan"),
  };
};
