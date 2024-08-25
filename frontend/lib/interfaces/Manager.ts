interface Manager {
  id: string;
  name: string;
  geopoints: ManagerGeoPoint[];
}

interface Me extends Manager {
  permissions: string[];
}
