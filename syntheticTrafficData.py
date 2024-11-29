import random
import pandas as pd
from datetime import timedelta, datetime

# Step 1: Define Routes and Buses
num_routes = 5
stops_per_route = 10
buses_per_route = 3  # Number of buses per route

# Generate routes
routes = {}
for route_id in range(1, num_routes + 1):
    routes[f"Route_{route_id}"] = [f"Stop_{i}" for i in range(1, stops_per_route + 1)]

# Assign buses to routes
buses = [f"Bus_{i}" for i in range(1, num_routes * buses_per_route + 1)]
route_bus_map = {route: [f"Bus_{i}" for i in range(start, start + buses_per_route)]
                 for start, route in enumerate(routes.keys(), start=1)}

# Step 2: Generate Randomized Traffic Data
traffic_levels = {"low": 1, "medium": 1.2, "high": 1.5}
base_time = 5  # Base travel time in minutes
traffic_data = []

for route, stops in routes.items():
    for i in range(len(stops) - 1):
        traffic = random.choice(list(traffic_levels.keys()))
        traffic_multiplier = traffic_levels[traffic]
        
        # Add base randomness (±20% of the base time)
        base_randomness = random.uniform(0.8, 1.2)
        
        # Add noise specific to traffic level
        traffic_noise = random.uniform(0, 2) if traffic == "low" else random.uniform(1, 4)
        
        # Calculate final travel time
        travel_time = base_time * base_randomness * traffic_multiplier + traffic_noise
        traffic_data.append({
            "Route": route,
            "From": stops[i],
            "To": stops[i+1],
            "Traffic_Level": traffic,
            "Travel_Time_Minutes": round(travel_time, 2)
        })

# Step 3: Simulate Bus Schedules with Multiple Buses
start_time = datetime.strptime("08:00", "%H:%M")  # Start at 8:00 AM
bus_schedule = []

for route, bus_list in route_bus_map.items():
    for bus_id in bus_list:
        current_time = start_time  # Each bus starts at the initial time
        for data in [d for d in traffic_data if d["Route"] == route]:
            travel_time_minutes = data["Travel_Time_Minutes"]
            start_time_str = current_time.strftime("%H:%M")
            arrival_time = current_time + timedelta(minutes=travel_time_minutes)
            arrival_time_str = arrival_time.strftime("%H:%M")
            bus_schedule.append({
                "Route": data["Route"],
                "Bus": bus_id,
                "From": data["From"],
                "To": data["To"],
                "Traffic_Level": data["Traffic_Level"],
                "Travel_Time_Minutes": data["Travel_Time_Minutes"],
                "Start_Time": start_time_str,
                "Arrival_Time": arrival_time_str
            })
            current_time = arrival_time  # Update current time for the next stop
        start_time += timedelta(minutes=15)  # Stagger start times for buses on the same route

# Step 4: Save and Visualize
df = pd.DataFrame(bus_schedule)
df.to_csv("bus_traffic_data_randomized.csv", index=False)

print("Data saved to 'bus_traffic_data_randomized.csv'!")