import math
from itertools import permutations


def calculate_distance(point1, point2):

    R = 6371

    lat1 = math.radians(point1["lat"])
    lat2 = math.radians(point2["lat"])

    dlat = math.radians(point2["lat"] - point1["lat"])
    dlon = math.radians(point2["lon"] - point1["lon"])

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return R * c


def optimize_route(assigned_deliveries, deliveries, depot):

    if len(assigned_deliveries) <= 1:
        return assigned_deliveries

    best_route = assigned_deliveries
    best_distance = float("inf")

    for route in permutations(assigned_deliveries):

        distance = 0
        current_point = depot

        for delivery in route:

            next_point = deliveries[delivery]

            distance += calculate_distance(
                current_point,
                next_point
            )

            current_point = next_point

        distance += calculate_distance(
            current_point,
            depot
        )

        if distance < best_distance:
            best_distance = distance
            best_route = list(route)

    return best_route