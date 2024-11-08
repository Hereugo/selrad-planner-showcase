import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import urls from "../urls";
import {
  deleteWithAuth,
  fetchWithAuth,
  patchWithAuth,
  postWithAuth,
} from "../httpCalls";

interface plansQueryProps {
  start_date?: string;
  end_date?: string;
  limit?: number;
  ordering?: string;
  page?: number;
  search?: string;
  managers?: Manager["id"][];
  work_items?: WorkItem["id"][];
}

export const usePlansQuery = (props: plansQueryProps = {}) => {
  const url = urls.base_backend.plans;
  const queryParams = [];

  if (props.start_date) queryParams.push(`start_date=${props.start_date}`);
  if (props.end_date) queryParams.push(`end_date=${props.end_date}`);
  if (props.limit) queryParams.push(`limit=${props.limit}`);
  if (props.ordering) queryParams.push(`ordering=${props.ordering}`);
  if (props.page) queryParams.push(`page=${props.page}`);
  if (props.search) queryParams.push(`search=${props.search}`);
  if (props.managers) queryParams.push(`managers=${props.managers.join(",")}`);
  if (props.work_items)
    queryParams.push(`work_items=${props.work_items.join(",")}`);

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
  managers: Manager["id"][];
  work_items: WorkItem["id"][];
  shipment_cost_formula: string;
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
  work_items: string[];
  // shipment_cost: number;
  shipment_cost_formula: string;
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
  start_date?: string;
  end_date?: string;
  ordering?: string;
  search?: string;
  managers?: Manager["id"][];
  work_items?: WorkItem["id"][];
}

export const planExportQuery = (props: planExportQueryProps = {}) => {
  const url = urls.base_backend.plan_export;
  const queryParams = [];

  if (props.start_date) queryParams.push(`start_date=${props.start_date}`);
  if (props.end_date) queryParams.push(`end_date=${props.end_date}`);
  if (props.ordering) queryParams.push(`ordering=${props.ordering}`);
  if (props.search) queryParams.push(`search=${props.search}`);
  if (props.managers) queryParams.push(`managers=${props.managers.join(",")}`);
  if (props.work_items)
    queryParams.push(`work_items=${props.work_items.join(",")}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return fetchWithAuth<Blob>(urlWithParams, {
    responseType: "blob",
  });
};

export const dispatchExportQuery = (props: planExportQueryProps = {}) => {
  const url = urls.base_backend.dispatch_export_report;
  const queryParams = [];

  if (props.start_date) queryParams.push(`start_date=${props.start_date}`);
  if (props.end_date) queryParams.push(`end_date=${props.end_date}`);
  if (props.ordering) queryParams.push(`ordering=${props.ordering}`);
  if (props.search) queryParams.push(`search=${props.search}`);
  if (props.managers) queryParams.push(`managers=${props.managers.join(",")}`);
  if (props.work_items)
    queryParams.push(`work_items=${props.work_items.join(",")}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return fetchWithAuth<Blob>(urlWithParams, {
    responseType: "blob",
  });
};

export const managerReportExportQuery = (props: planExportQueryProps) => {
  const baseUrl = urls.base_backend.plan_export_report;
  const url = `${baseUrl}/${props.managers?.[0]}`;
  const queryParams = [];

  if (props.start_date) queryParams.push(`start_date=${props.start_date}`);
  if (props.end_date) queryParams.push(`end_date=${props.end_date}`);
  if (props.ordering) queryParams.push(`ordering=${props.ordering}`);
  if (props.search) queryParams.push(`search=${props.search}`);
  if (props.work_items)
    queryParams.push(`work_items=${props.work_items.join(",")}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return fetchWithAuth<Blob>(urlWithParams, {
    responseType: "blob",
  });
};
