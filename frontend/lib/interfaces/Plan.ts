interface Plan {
  id: string;
  assigned_date: string;
  worklist: Work[];
  client: Client;
  shipment_cost: number;
  shipment_cost_formula: string;
  comment: string;
  managers: Manager[];
  box_count: number;

  created_at: string;
  updated_at: string;
}
