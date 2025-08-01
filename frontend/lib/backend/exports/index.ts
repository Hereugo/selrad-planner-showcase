import { fetchWithAuth } from "../httpCalls";
import urls from "../urls";

interface planExportQueryProps {
  start_date?: string;
  end_date?: string;
  ordering?: string;
  search?: string;
  managers?: Manager["id"][];
  work_items?: WorkItem["id"][];
}

export const planExportQuery = (props: planExportQueryProps = {}) => {
  const url = urls.base_backend.exports.plans;
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
  const url = urls.base_backend.exports.dispatch_report;
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

interface managerReportExportQueryProps {
  manager: Manager["id"];
  start_date?: string;
  end_date?: string;
  ordering?: string;
  search?: string;
  work_items?: WorkItem["id"][];
}

export const managerReportExportQuery = (
  props: managerReportExportQueryProps,
) => {
  const url = urls.base_backend.exports.report;
  const queryParams = [];

  if (props.start_date) queryParams.push(`start_date=${props.start_date}`);
  if (props.end_date) queryParams.push(`end_date=${props.end_date}`);
  if (props.ordering) queryParams.push(`ordering=${props.ordering}`);
  if (props.manager) queryParams.push(`manager=${props.manager}`);
  if (props.search) queryParams.push(`search=${props.search}`);
  if (props.work_items)
    queryParams.push(`work_items=${props.work_items.join(",")}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return fetchWithAuth<Blob>(urlWithParams, {
    responseType: "blob",
  });
};

interface dispatchListExportQueryProps {
  manager: Manager["id"];
  start_date?: string;
  end_date?: string;
  ordering?: string;
  search?: string;
  work_items?: WorkItem["id"][];
  only_shipment?: boolean;
  comment?: string;
  set_time_dispatch?: boolean;
}

export const dispatchListExportQuery = (
  props: dispatchListExportQueryProps,
) => {
  const url = urls.base_backend.exports.dispatch_list;
  const queryParams = [];

  if (props.start_date) queryParams.push(`start_date=${props.start_date}`);
  if (props.end_date) queryParams.push(`end_date=${props.end_date}`);
  if (props.ordering) queryParams.push(`ordering=${props.ordering}`);
  if (props.search) queryParams.push(`search=${props.search}`);
  if (props.manager) queryParams.push(`manager=${props.manager}`);
  if (props.work_items)
    queryParams.push(`work_items=${props.work_items.join(",")}`);
  if (props.only_shipment !== undefined)
    queryParams.push(`only_shipment=${props.only_shipment}`);
  if (props.comment) queryParams.push(`comment=${props.comment}`);
  if (props.set_time_dispatch !== undefined)
    queryParams.push(`set_time_dispatch=${props.set_time_dispatch}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return fetchWithAuth<Blob>(urlWithParams, {
    responseType: "blob",
  });
};

interface compareReportExportQueryProps {
  start_date?: string;
  end_date?: string;
  diff_year?: number;
  managers?: string[];
  work_items?: string[];
}

export const compareReportExportQuery = (
  props: compareReportExportQueryProps,
) => {
  const baseUrl = urls.base_backend.exports.compare_years;
  const url = `${baseUrl}`;
  const queryParams = [];

  if (props.start_date) queryParams.push(`start_date=${props.start_date}`);
  if (props.end_date) queryParams.push(`end_date=${props.end_date}`);
  if (props.diff_year) queryParams.push(`diff_year=${props.diff_year}`);
  if (props.managers) queryParams.push(`managers=${props.managers.join(",")}`);
  if (props.work_items)
    queryParams.push(`work_items=${props.work_items.join(",")}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return fetchWithAuth<Blob>(urlWithParams, {
    responseType: "blob",
  });
};

interface paymentReportExportQueryProps {
  start_date?: string;
  end_date?: string;
  managers?: string[];
  work_items?: string[];
  only_shipment?: boolean;
}

export const paymentReportExportQuery = (
  props: paymentReportExportQueryProps,
) => {
  const url = urls.base_backend.exports.payment_report;
  const queryParams = [];

  if (props.start_date) queryParams.push(`start_date=${props.start_date}`);
  if (props.end_date) queryParams.push(`end_date=${props.end_date}`);
  if (props.only_shipment)
    queryParams.push(`only_shipment=${props.only_shipment}`);
  if (props.managers) queryParams.push(`managers=${props.managers.join(",")}`);
  if (props.work_items)
    queryParams.push(`work_items=${props.work_items.join(",")}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return fetchWithAuth<Blob>(urlWithParams, {
    responseType: "blob",
  });
};

export const distributionCostReportExportQuery = (
  props: paymentReportExportQueryProps,
) => {
  const url = urls.base_backend.exports.distribution_cost_report;
  const queryParams = [];

  if (props.start_date) queryParams.push(`start_date=${props.start_date}`);
  if (props.end_date) queryParams.push(`end_date=${props.end_date}`);
  if (props.only_shipment)
    queryParams.push(`only_shipment=${props.only_shipment}`);
  if (props.managers) queryParams.push(`managers=${props.managers.join(",")}`);
  if (props.work_items)
    queryParams.push(`work_items=${props.work_items.join(",")}`);

  const urlWithParams = `${url}${queryParams.length > 0 ? "?" : ""}${queryParams.join("&")}`;

  return fetchWithAuth<Blob>(urlWithParams, {
    responseType: "blob",
  });
};
