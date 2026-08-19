interface DailyTrackingManager {
  id: string;
  name: string;
  is_manager: boolean;
  is_driver: boolean;
  depot_lat: number | null;
  depot_lon: number | null;
}

interface DailyTrackingCursor {
  created_at: string;
  id: string;
}

interface DailyTrackingTimelineRow {
  id: string;
  type: "travel" | "inside_plan";
  type_label: string;
  route: string;
  start_at: string;
  end_at: string;
  duration_seconds: number;
  plan_id: string | null;
  from_plan_id: string | null;
  to_plan_id: string | null;
  geopoint_ids: string[];
}

interface DailyTrackingResponse {
  date: string;
  manager: DailyTrackingManager;
  plans: Plan[];
  geopoints: ManagerGeoPoint[];
  current_geopoint: ManagerGeoPoint | null;
  cursor: DailyTrackingCursor | null;
  timeline: DailyTrackingTimelineRow[];
}
