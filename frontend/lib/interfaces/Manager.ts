interface User {
  id: string;
  name: string;

  payment: number;

  is_driver: boolean;
  is_warehouser: boolean;
  is_accountant: boolean;
  is_manager: boolean;
}

interface Manager extends User {
  geopoints: ManagerGeoPoint[];
  depot_lat: string | null;
  depot_lon: string | null;
}

interface Me extends Manager {
  permissions: string[];
}
