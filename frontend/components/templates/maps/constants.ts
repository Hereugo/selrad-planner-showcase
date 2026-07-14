export type CityKey = "almaty" | "astana";

export interface CityConfig {
  displayName: string;
  center: [number, number];
  zoom: number;
}

export const CITIES: Record<CityKey, CityConfig> = {
  almaty: {
    displayName: "Алматы",
    center: [43.238949, 76.889709],
    zoom: 12,
  },
  astana: {
    displayName: "Астана",
    center: [51.12822, 71.4305],
    zoom: 11,
  },
};

export const DEFAULT_CITY: CityKey = "almaty";
