interface Manager {
  id: string;
  name: string;
  geopoints: ManagerGeoPoint[];

  payment: number | null;

  is_driver: boolean;
  is_warehouser: boolean;
  is_accountant: boolean;
  is_manager: boolean;
}

interface Me extends Manager {
  permissions: string[];
}
