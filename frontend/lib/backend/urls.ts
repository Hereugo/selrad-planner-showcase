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
    users: {
      users: `${BASE_BACKEND_V1}/users`,
      me: `${BASE_BACKEND_V1}/users/me`,
      drivers: `${BASE_BACKEND_V1}/users/drivers`,
      managers: `${BASE_BACKEND_V1}/users/managers`,
      warehousers: `${BASE_BACKEND_V1}/users/warehousers`,
    },
    payment_registries: `${BASE_BACKEND_V1}/payment_registries`,
    exports: {
      compare_years: `${BASE_BACKEND_V1}/exports/compare_years`,
      dispatch_list: `${BASE_BACKEND_V1}/exports/dispatch_list`,
      dispatch_report: `${BASE_BACKEND_V1}/exports/dispatch_report`,
      payment_report: `${BASE_BACKEND_V1}/exports/payment_report`,
      distribution_cost_report: `${BASE_BACKEND_V1}/exports/distribution_cost_report`,
      plans: `${BASE_BACKEND_V1}/exports/plans`,
      report: `${BASE_BACKEND_V1}/exports/manager_report`,
    },
  },
};

export default urls;
