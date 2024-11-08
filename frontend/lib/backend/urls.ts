const BASE_BACKEND_V1 = `${process.env.NEXT_PUBLIC_BASE_BACKEND_URL}/api/v1`;
const BASE_AUTH_V1 = `${process.env.NEXT_PUBLIC_BASE_BACKEND_URL}/api/auth/jwt`;

const urls = {
  auth_api: {
    create: `${BASE_AUTH_V1}/create`,
    refresh: `${BASE_AUTH_V1}/refresh`,
    verify: `${BASE_AUTH_V1}/verify`,
  },

  base_backend: {
    plans: `${BASE_BACKEND_V1}/plans`,
    clients: `${BASE_BACKEND_V1}/clients`,
    work_items: `${BASE_BACKEND_V1}/work_items`,
    plan_export: `${BASE_BACKEND_V1}/plans/export`,
    dispatch_export_report: `${BASE_BACKEND_V1}/plans/dispatch_report`,
    plan_export_report: `${BASE_BACKEND_V1}/plans/export_report/`,
    compare: `${BASE_BACKEND_V1}/plans/export_compare_years`,
    managers: `${BASE_BACKEND_V1}/users/managers`,
    warehousers: `${BASE_BACKEND_V1}/users/warehousers`,
    drivers: `${BASE_BACKEND_V1}/users/drivers`,
    me: `${BASE_BACKEND_V1}/users/me`,
    users: `${BASE_BACKEND_V1}/users`,
  },
};

export default urls;
