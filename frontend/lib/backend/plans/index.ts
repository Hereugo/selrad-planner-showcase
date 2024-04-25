import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import urls from "../urls";
import {
  deleteWithAuth,
  fetchWithAuth,
  patchWithAuth,
  postWithAuth,
} from "../httpCalls";

interface plansQueryProps {
  date_after?: string;
  date_before?: string;
  limit?: number;
  ordering?: string;
  page?: number;
  search?: string;
  manager_id?: string;
  worklist_id?: string;
}

export const usePlansQuery = (props: plansQueryProps = {}) => {
  const url = urls.base_backend.plans;
  const queryParams = [];

  if (props.date_after) queryParams.push(`date_after=${props.date_after}`);
  if (props.date_before) queryParams.push(`date_before=${props.date_before}`);
  if (props.limit) queryParams.push(`limit=${props.limit}`);
  if (props.ordering) queryParams.push(`ordering=${props.ordering}`);
  if (props.page) queryParams.push(`page=${props.page}`);
  if (props.search) queryParams.push(`search=${props.search}`);
  if (props.manager_id) queryParams.push(`manager_id=${props.manager_id}`);
  if (props.worklist_id) queryParams.push(`worklist_id=${props.worklist_id}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return useQuery(["usePlansQuery", urlWithParams], async () =>
    fetchWithAuth<Plan[]>(urlWithParams),
  );
};

export const usePlanQuery = (id: string) => {
  const url = urls.base_backend.plans;
  const urlParamed = `${url}/${id}/`;

  return useQuery(["usePlanQuery", id], async () =>
    fetchWithAuth<Plan>(urlParamed),
  );
};

interface planCreateMutationProps {
  assigned_date: string;
  client: string;
  managers: string[];
  worklist: string[];
  shipment_cost: number;
  box_count: number;
  comment: string;
}

export const usePlanCreateMutation = () => {
  const queryClient = useQueryClient();

  const url = urls.base_backend.plans + "/";

  const call = (plan: planCreateMutationProps) => {
    return postWithAuth(url, plan);
  };

  return useMutation(call, {
    onSuccess: () => {
      queryClient.invalidateQueries(["usePlansQuery"]);
    },
  });
};

interface planUpdateMutation {
  assigned_date: string;
  client: string;
  managers: string[];
  worklist: string[];
  shipment_cost: number;
  box_count: number;
  comment: string;
}

export const usePlanUpdateMutation = (id: string) => {
  const queryClient = useQueryClient();

  const url = urls.base_backend.plans;
  const urlParamed = `${url}/${id}/`;

  const call = (plan: planUpdateMutation) => {
    return patchWithAuth(urlParamed, plan);
  };

  return useMutation(call, {
    onSuccess: () => {
      queryClient.invalidateQueries(["usePlansQuery"]);
    },
  });
};

export const usePlanDeleteMutation = (id: string) => {
  const queryClient = useQueryClient();

  const url = urls.base_backend.plans;
  const urlParamed = `${url}/${id}/`;

  const call = () => {
    return deleteWithAuth(urlParamed);
  };

  return useMutation(call, {
    onSuccess: () => {
      queryClient.invalidateQueries(["usePlansQuery"]);
    },
  });
};

interface planExportQueryProps {
  date_after?: string;
  date_before?: string;
  manager_id?: string;
  ordering?: string;
  search?: string;
  worklist_id?: string;
}

export const planExportQuery = (props: planExportQueryProps = {}) => {
  const url = urls.base_backend.plan_export;
  const queryParams = [];

  if (props.date_after) queryParams.push(`date_after=${props.date_after}`);
  if (props.date_before) queryParams.push(`date_before=${props.date_before}`);
  if (props.ordering) queryParams.push(`ordering=${props.ordering}`);
  if (props.search) queryParams.push(`search=${props.search}`);
  if (props.manager_id) queryParams.push(`manager_id=${props.manager_id}`);
  if (props.worklist_id) queryParams.push(`worklist_id=${props.worklist_id}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return fetchWithAuth<Blob>(urlWithParams, {
    responseType: "blob",
  });
};

interface managerReportExportQueryProps {
  manager_id: Manager["id"];
}

export const managerReportExportQuery = (
  props: managerReportExportQueryProps,
) => {
  const url = urls.base_backend.plan_export_report;
  const urlWithParams = `${url}/${props.manager_id}`;

  return fetchWithAuth<Blob>(urlWithParams, {
    responseType: "blob",
  });
};
