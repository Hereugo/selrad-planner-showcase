import { useMeQuery } from "../backend/users";

export const useViewFeature = () => {
  const { data } = useMeQuery();
  const me = data?.data;

  return {
    isLoading: !me,
    canUseWorkFilter: !me?.is_accountant,
    canViewMaps: !me?.is_accountant,
    canViewDailyTracking: me?.permissions.includes(
      "managers.view_daily_tracking",
    ),
    canViewAccountant: me?.is_accountant,
    canCreateNewPlan: !me?.is_accountant,
    canCreateShop: me?.permissions.includes("clients.add_client"),
    canExportPlans: me?.permissions.includes("plans.export_plans"),
    canExportReport: me?.permissions.includes("plans.export_report"),
    canExportDispatchList: me?.permissions.includes("plans.get_dispatch_list"),
    canExportDispatchReport: me?.permissions.includes(
      "plans.get_dispatch_report",
    ),
    canExportCompareReport: me?.permissions.includes(
      "clients.export_compare_years",
    ),
    canExportPaymentReport: me?.permissions.includes(
      "plans.export_payment_report",
    ),
    canExportDistributionCostReport: me?.permissions.includes(
      "plans.export_distribution_cost_report",
    ),
    canDeletePlan: me?.permissions.includes("plans.delete_plans"),
    canDeleteOldPlan: me?.permissions.includes("plans.delete_old_plan"),
    canUpdateOldPlan: me?.permissions.includes("plans.change_old_plan"),
    canViewSettings: me?.permissions.includes("managers.view_settings"),
    canViewPaymentSettings: me?.permissions.includes(
      "managers.view_payments_section",
    ),
    canViewPaymnetRegistry: me?.permissions.includes(
      "plans.view_paymentregistry",
    ),
    canUpdatePaymnetRegistry: me?.permissions.includes(
      "plans.change_paymentregistry",
    ),
  };
};
