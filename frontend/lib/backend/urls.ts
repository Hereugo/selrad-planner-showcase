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
    managers: `${BASE_BACKEND_V1}/managers`,
    worklist: `${BASE_BACKEND_V1}/worklist`,
  },
};

export default urls;
