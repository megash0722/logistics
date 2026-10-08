def assign_deliveries(deliveries, vehicles):
    assignments = {}
    remaining_deliveries = deliveries.copy()

    for vehicle, capacity in vehicles.items():

        assignments[vehicle] = []
        used_capacity = 0

        for delivery, info in list(remaining_deliveries.items()):

            demand = info["demand"]

            if used_capacity + demand <= capacity:

                assignments[vehicle].append(delivery)
                used_capacity += demand

                del remaining_deliveries[delivery]

    return assignments, remaining_deliveries