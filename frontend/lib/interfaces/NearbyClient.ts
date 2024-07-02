interface NearbyClient {
  client: Client;
  last_plan: Plan | null;
  last_shipment_plan: Plan | null;
}
