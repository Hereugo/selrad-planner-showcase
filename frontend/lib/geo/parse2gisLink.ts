export interface Parsed2gisPoint {
  lat: number;
  lon: number;
}

const ALMATY_LAT_RANGE = [40, 47];
const ALMATY_LON_RANGE = [70, 85];

const isInRange = (value: number, [min, max]: number[]) => {
  return value >= min && value <= max;
};

const toPoint = (lonCandidate: string, latCandidate: string) => {
  const lon = Number(lonCandidate);
  const lat = Number(latCandidate);

  if (!Number.isFinite(lat) || !Number.isFinite(lon)) return undefined;
  if (!isInRange(lat, ALMATY_LAT_RANGE)) return undefined;
  if (!isInRange(lon, ALMATY_LON_RANGE)) return undefined;

  return { lat, lon };
};

export const parse2gisLink = (link: string): Parsed2gisPoint | undefined => {
  let decodedLink: string;
  try {
    decodedLink = decodeURIComponent(link.trim());
  } catch {
    return undefined;
  }
  if (!decodedLink) return undefined;

  const patterns = [
    /[?&]m=(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)/,
    /\/geo\/[^?#]*\/(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)/,
    /\/firm\/[^?#]*\/(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)/,
  ];

  for (const pattern of patterns) {
    const match = decodedLink.match(pattern);
    if (!match) continue;

    const point = toPoint(match[1], match[2]);
    if (point) return point;
  }

  return undefined;
};
