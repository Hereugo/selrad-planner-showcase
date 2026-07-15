import math

# WGS84 ellipsoid parameters
_A  = 6378137.0          # semi-major axis (m)
_E2 = 0.00669437999014   # first eccentricity squared  e² = 2f - f²


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Straight-line (geodesic) distance in kilometres between two WGS84 points.

    Args:
        lat1, lon1: first point in decimal degrees
        lat2, lon2: second point in decimal degrees

    Returns:
        Distance in kilometres.
    """
    phi1    = math.radians(lat1)
    phi2    = math.radians(lat2)
    dp      = phi2 - phi1                   # Δlat in radians
    dl      = math.radians(lon2 - lon1)     # Δlon in radians
    phi_mid = (phi1 + phi2) / 2             # midpoint latitude

    # ── Euler radius at midpoint ──────────────────────────────────────────
    sin2 = math.sin(phi_mid) ** 2
    W    = math.sqrt(1.0 - _E2 * sin2)
    M    = _A * (1.0 - _E2) / (W ** 3)     # meridional radius (N-S), metres
    N    = _A / W                          # normal radius     (E-W), metres

    az   = math.atan2(dl * math.cos(phi_mid), dp)   # segment azimuth
    cos2 = math.cos(az) ** 2

    R_km = (1.0 / (cos2 / M + (1.0 - cos2) / N)) / 1000.0

    # ── Standard haversine kernel ─────────────────────────────────────────
    a = (
        math.sin(dp / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dl / 2) ** 2
    )
    return R_km * 2 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a)) * .8
