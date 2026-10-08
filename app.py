import streamlit as st
import math
import folium
from streamlit_folium import st_folium
from logic import assign_deliveries
from route_optimizer import optimize_route, calculate_distance

# Page settings
st.set_page_config(
    page_title="Smart Urban Logistics",
    page_icon="🚚",
    layout="wide"
)

# Title
st.title("🚚 Smart Urban Logistics Optimizer")

st.write("An enhanced prototype for smart urban delivery planning.")
st.info(
    "🔄 How It Works: "
    "Enter delivery demand → Assign vehicles based on capacity → "
    "Optimize delivery routes → Calculate distance → "
    "Compare before and optimized routes."
)
st.divider()

# -------------------------
# DELIVERY INFORMATION
# -------------------------

st.header("📦 Delivery Information")

depot = {
    "lat": 13.0800,
    "lon": 80.2700
}

deliveries = {
    "D1": {"demand": 2, "lat": 13.0827, "lon": 80.2707},
    "D2": {"demand": 3, "lat": 13.0878, "lon": 80.2785},
    "D3": {"demand": 1, "lat": 13.0757, "lon": 80.2572},
    "D4": {"demand": 4, "lat": 13.0950, "lon": 80.2850},
    "D5": {"demand": 2, "lat": 13.0680, "lon": 80.2600}
}
st.subheader("📦 Adjust Delivery Demand")
st.info(
    "💡 Change delivery demand below to see automatic "
    "vehicle assignment and route optimization."
)

for delivery in deliveries:
    deliveries[delivery]["demand"] = st.number_input(
        f"{delivery} packages",
        min_value=1,
        max_value=20,
        value=deliveries[delivery]["demand"],
        key=f"demand_{delivery}"
    )

for delivery, info in deliveries.items():
    st.write(
        f"📍 {delivery} → {info['demand']} packages "
        f"(Location: {info['lat']:.4f}, {info['lon']:.4f})"
    )

# -------------------------
# VEHICLE INFORMATION
# -------------------------

st.header("🚚 Vehicle Information")

vehicles = {
    "Bike": 5,
    "Van": 10,
    "Truck": 20
}

for vehicle, capacity in vehicles.items():
    st.write(
        f"🚚 {vehicle} → Capacity: {capacity} packages"
    )

# -------------------------
# DISTANCE CALCULATION
# -------------------------

# -------------------------
# ASSIGN DELIVERIES
# -------------------------
assignments, remaining_deliveries = assign_deliveries(
    deliveries,
    vehicles
)

# -------------------------
# DISPLAY ASSIGNMENTS
# -------------------------

# -------------------------
# DISPLAY ASSIGNMENTS
# -------------------------

for vehicle, assigned in assignments.items():

    if assigned:
        optimized_route = optimize_route(
            assigned,
            deliveries,
            depot
        )

        st.write(
            f"🚚 **{vehicle}** → {', '.join(assigned)}"
        )

    else:
        st.write(
            f"🚚 **{vehicle}** → No deliveries assigned"
        )
# -------------------------
# ROUTE DISTANCE
# -------------------------

st.header("📏 Route Distance")

for vehicle, assigned in assignments.items():

    if assigned:

        total_distance = 0
        current_point = depot

        for delivery in assigned:

            delivery_point = deliveries[delivery]

            distance = calculate_distance(
                current_point,
                delivery_point
            )

            total_distance += distance
            current_point = delivery_point

        # Return to depot
        total_distance += calculate_distance(
            current_point,
            depot
        )

        st.write(
            f"🚚 **{vehicle}** → "
            f"{total_distance:.2f} km"
        )
# -------------------------
# ROUTE DETAILS
# -------------------------

# -------------------------
# ROUTE DETAILS
# -------------------------

st.header("🔄 Generated Routes")

for vehicle, assigned in assignments.items():

    if assigned:

        optimized_route = optimize_route(
            assigned,
            deliveries,
            depot
        )

        route = ["Depot"] + optimized_route + ["Depot"]

        st.write(
            f"🚚 **{vehicle}** → "
            f"{' → '.join(route)}"
        )
# REMAINING DELIVERIES
# -------------------------

if remaining_deliveries:

    st.warning(
        f"⚠️ These deliveries could not be assigned: "
        f"{', '.join(remaining_deliveries.keys())}"
    )

else:

    st.success(
        "✅ All deliveries successfully assigned!"
    )
# -------------------------
# ROUTE MAP
# -------------------------

# -------------------------
# ROUTE MAP
# -------------------------
# -------------------------
# ROUTE MAP
# -------------------------

st.header("🗺️ Route Map")

m = folium.Map(
    location=[depot["lat"], depot["lon"]],
    zoom_start=14
)

# Depot marker
folium.Marker(
    [depot["lat"], depot["lon"]],
    tooltip="🏢 Depot"
).add_to(m)

# Delivery markers
for delivery, info in deliveries.items():

    folium.Marker(
    [info["lat"], info["lon"]],
    tooltip=f"{delivery} - {info['demand']} packages",
    popup=f"{delivery}: {info['demand']} packages",
    icon=folium.Icon(icon="info-sign")
).add_to(m)

# Draw routes
for vehicle, assigned in assignments.items():

    if assigned:

        route_points = [
            [depot["lat"], depot["lon"]]
        ]

        for delivery in assigned:

            info = deliveries[delivery]

            route_points.append(
                [info["lat"], info["lon"]]
            )

        route_points.append(
            [depot["lat"], depot["lon"]]
        )

       # Draw routes

route_colors = {
    "Bike": "blue",
    "Van": "green",
    "Truck": "red"
}

for vehicle, assigned in assignments.items():

    if assigned:

        route_points = [
            [depot["lat"], depot["lon"]]
        ]

        for delivery in assigned:

            info = deliveries[delivery]

            route_points.append(
                [info["lat"], info["lon"]]
            )

        route_points.append(
            [depot["lat"], depot["lon"]]
        )

        folium.PolyLine(
            route_points,
            weight=5,
            color=route_colors.get(vehicle, "blue"),
            tooltip=f"{vehicle} Route"
        ).add_to(m)

st_folium(m, width=1000, height=500)
# -------------------------
# ANALYTICS
# -------------------------

st.header("📊 Logistics Analytics")
st.caption("Real-time summary of delivery planning and vehicle utilization.")

total_deliveries = len(deliveries)

total_packages = sum(
    info["demand"] for info in deliveries.values()
)

vehicles_used = sum(
    1 for assigned in assignments.values()
    if assigned
)

total_capacity = sum(
    vehicles[vehicle]
    for vehicle, assigned in assignments.items()
    if assigned
)

total_distance = 0

for vehicle, assigned in assignments.items():

    if assigned:

        current_point = depot

        for delivery in assigned:

            delivery_point = deliveries[delivery]

            total_distance += calculate_distance(
                current_point,
                delivery_point
            )

            current_point = delivery_point

        total_distance += calculate_distance(
            current_point,
            depot
        )

assigned_packages = sum(
    deliveries[delivery]["demand"]
    for assigned in assignments.values()
    for delivery in assigned
)

capacity_utilization = (
    assigned_packages / total_capacity * 100
    if total_capacity > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("📦 Deliveries", total_deliveries)
col2.metric("📦 Packages", total_packages)
col3.metric("🚚 Vehicles Used", vehicles_used)
col4.metric("📊 Capacity Utilization", f"{capacity_utilization:.1f}%")

st.metric(
    "📏 Total Estimated Distance",
    f"{total_distance:.2f} km"
)
# -------------------------
## -------------------------
# BEFORE VS OPTIMIZED
# -------------------------

st.header("⚖️ Before vs Optimized")

# BEFORE:
# Use the original delivery order for each vehicle

before_distance = 0

for vehicle, assigned in assignments.items():

    if assigned:

        current_point = depot

        for delivery in assigned:

            delivery_point = deliveries[delivery]

            before_distance += calculate_distance(
                current_point,
                delivery_point
            )

            current_point = delivery_point

        # Return to depot
        before_distance += calculate_distance(
            current_point,
            depot
        )


# OPTIMIZED:
# Find the best route order for each vehicle

optimized_distance = 0

for vehicle, assigned in assignments.items():

    if assigned:

        optimized_route = optimize_route(
            assigned,
            deliveries,
            depot
        )

        current_point = depot

        for delivery in optimized_route:

            delivery_point = deliveries[delivery]

            optimized_distance += calculate_distance(
                current_point,
                delivery_point
            )

            current_point = delivery_point

        # Return to depot
        optimized_distance += calculate_distance(
            current_point,
            depot
        )


# Calculate improvement

if before_distance > 0:

    improvement = (
        (before_distance - optimized_distance)
        / before_distance
    ) * 100

else:

    improvement = 0


# Display results

col1, col2, col3 = st.columns(3)

col1.metric(
    "📏 Before",
    f"{before_distance:.4f} km"
)

col2.metric(
    "📏 Optimized",
    f"{optimized_distance:.4f} km"
)

col3.metric(
    "📉 Improvement",
    f"{improvement:.1f}%"
)


# Result message

if improvement > 0:

    st.success(
        f"✅ Route distance reduced by {improvement:.1f}%"
    )

elif improvement == 0:

    st.info(
        "ℹ️ The current delivery order is already optimal."
    )

else:

    st.warning(
        "⚠️ Optimized route is longer than the baseline."
    )