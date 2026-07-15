from optimization.geo import haversine


# ---------------------------------------------------------------------------
# Route simulation
# ---------------------------------------------------------------------------

def _nn_tour(
    stops: list[tuple[float, float]],
    depot: tuple[float, float],
) -> list[tuple[float, float]]:
    """Nearest-neighbour greedy tour. Returns ordered stop list (depot excluded)."""
    remaining = list(stops)
    pos = depot
    tour: list[tuple[float, float]] = []
    while remaining:
        nearest = min(remaining, key=lambda s: haversine(pos[0], pos[1], s[0], s[1]))
        tour.append(nearest)
        pos = nearest
        remaining.remove(nearest)
    return tour


def _tour_km(
    tour: list[tuple[float, float]],
    depot: tuple[float, float],
) -> float:
    """Total distance for depot → tour[0] → … → tour[-1] → depot."""
    if not tour:
        return 0.0
    total = haversine(depot[0], depot[1], tour[0][0], tour[0][1])
    for i in range(len(tour) - 1):
        total += haversine(tour[i][0], tour[i][1], tour[i + 1][0], tour[i + 1][1])
    total += haversine(tour[-1][0], tour[-1][1], depot[0], depot[1])
    return total


def two_opt_tour(
    stops: list[tuple[float, float]],
    depot: tuple[float, float],
) -> list[tuple[float, float]]:
    """NN tour refined by 2-opt until no improving edge swap exists."""
    tour = _nn_tour(stops, depot)
    if len(tour) < 3:
        return tour
    improved = True
    while improved:
        improved = False
        for i in range(len(tour) - 1):
            for j in range(i + 2, len(tour)):
                a = tour[i - 1] if i > 0 else depot
                b = tour[i]
                c = tour[j]
                d = tour[j + 1] if j + 1 < len(tour) else depot
                if (
                    haversine(a[0], a[1], c[0], c[1]) + haversine(b[0], b[1], d[0], d[1])
                    < haversine(a[0], a[1], b[0], b[1]) + haversine(c[0], c[1], d[0], d[1]) - 1e-10
                ):
                    tour[i : j + 1] = tour[i : j + 1][::-1]
                    improved = True
    return tour


def cheapest_insertion_cost(
    tour: list[tuple[float, float]],
    depot: tuple[float, float],
    new_stop: tuple[float, float],
) -> float:
    """
    Minimum extra km to splice new_stop into an existing tour.
    Guaranteed non-negative by the triangle inequality.
    """
    if not tour:
        return 2.0 * haversine(depot[0], depot[1], new_stop[0], new_stop[1])
    sequence = [depot] + tour + [depot]
    best = float("inf")
    for i in range(len(sequence) - 1):
        a, b = sequence[i], sequence[i + 1]
        cost = (
            haversine(a[0], a[1], new_stop[0], new_stop[1])
            + haversine(new_stop[0], new_stop[1], b[0], b[1])
            - haversine(a[0], a[1], b[0], b[1])
        )
        if cost < best:
            best = cost
    return max(0.0, best)
