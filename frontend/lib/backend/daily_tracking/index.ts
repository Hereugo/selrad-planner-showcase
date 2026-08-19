import { useQuery } from "@tanstack/react-query";
import { fetchWithAuth } from "../httpCalls";
import urls from "../urls";

interface DailyTrackingQueryProps {
  managerId?: string;
  date?: string;
  sinceCreatedAt?: string;
  sinceId?: string;
}

const dailyTrackingUrl = (props: DailyTrackingQueryProps) => {
  const params = new URLSearchParams();

  if (props.managerId) params.set("manager", props.managerId);
  if (props.date) params.set("date", props.date);
  if (props.sinceCreatedAt) params.set("since_created_at", props.sinceCreatedAt);
  if (props.sinceId) params.set("since_id", props.sinceId);

  return `${urls.base_backend.daily_tracking}?${params.toString()}`;
};

export const fetchDailyTracking = async (props: DailyTrackingQueryProps) => {
  const response = await fetchWithAuth<DailyTrackingResponse>(
    dailyTrackingUrl(props),
  );
  return response.data;
};

export const useDailyTrackingQuery = (
  props: DailyTrackingQueryProps,
  enabled: boolean,
) => {
  return useQuery({
    queryKey: ["useDailyTrackingQuery", props.managerId, props.date],
    queryFn: () => fetchDailyTracking(props),
    enabled,
  });
};
