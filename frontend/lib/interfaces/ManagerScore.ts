interface ManagerScore {
  manager_id: Manager["id"];
  workload: number;
  route_km_delta?: number;
  is_day_off?: boolean;
}
