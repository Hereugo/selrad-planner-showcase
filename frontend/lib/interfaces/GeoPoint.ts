interface GeoPoint {
  latitude: number;
  longitude: number;
  accuracy: number | null;
  speed: number | null;
  heading: number | null;
}

interface ManagerGeoPoint extends GeoPoint {
  id: string;
  manager: string;
  created_at: string;
}
