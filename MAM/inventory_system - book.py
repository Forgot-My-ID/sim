import random
import math
from tabulate import tabulate

# Embedded input data
input_data = """
60 120 9 4 0.10 32 3.0 1.0 5.0 0.5 1
0.167 0.500 0.833 1.000
20 40
20 60
20 80
20 100
40 60
40 80
40 100
60 80
60 100
"""

# External definitions for inventory system.
initial_inv_level = 0
num_months = 0
num_policies = 0
num_values_demand = 0
mean_interdemand = 0.0
setup_cost = 0.0
incremental_cost = 0.0
holding_cost = 0.0
shortage_cost = 0.0
minlag = 0.0
maxlag = 0.0
prob_distrib_demand = [0.0] * 26
smalls = 0
bigs = 0
amount = 0
inv_level = 0
next_event_type = 0
num_events = 0
area_holding = 0.0
area_shortage = 0.0
total_ordering_cost = 0.0
sim_time = 0.0
time_last_event = 0.0
time_next_event = [0.0] * 5

# Function to read input parameters from embedded data
def read_input():
    global initial_inv_level, num_months, num_policies, num_values_demand, mean_interdemand, setup_cost, incremental_cost, holding_cost, shortage_cost, minlag, maxlag, prob_distrib_demand
    lines = input_data.strip().split('\n')
    initial_inv_level, num_months, num_policies, num_values_demand, mean_interdemand, setup_cost, incremental_cost, holding_cost, shortage_cost, minlag, maxlag = map(float, lines[0].split())
    num_values_demand = int(num_values_demand)  # Ensure num_values_demand is an integer
    prob_distrib_demand[1:num_values_demand+1] = list(map(float, lines[1].split()))

# Function to initialize the simulation
def initialize():
    global sim_time, inv_level, time_last_event, total_ordering_cost, area_holding, area_shortage, time_next_event, next_event_type
    sim_time = 0.0
    inv_level = initial_inv_level
    time_last_event = 0.0
    total_ordering_cost = 0.0
    area_holding = 0.0
    area_shortage = 0.0
    time_next_event[1] = 1.0e+30
    time_next_event[2] = sim_time + expon(mean_interdemand)
    time_next_event[3] = num_months
    time_next_event[4] = 0.0
    next_event_type = 0

# Function to handle order arrival event
def order_arrival():
    global inv_level, time_next_event
    inv_level += amount
    time_next_event[1] = 1.0e+30

# Function to handle demand event
def demand():
    global inv_level, time_next_event
    inv_level -= random_integer(prob_distrib_demand)
    time_next_event[2] = sim_time + expon(mean_interdemand)

# Function to handle inventory evaluation event
def evaluate():
    global amount, total_ordering_cost, time_next_event
    if inv_level < smalls:
        amount = bigs - inv_level
        total_ordering_cost += setup_cost + incremental_cost * amount
        time_next_event[1] = sim_time + uniform(minlag, maxlag)
    time_next_event[4] = sim_time + 1.0

# Function to generate a report
def report():
    avg_ordering_cost = total_ordering_cost / num_months
    avg_holding_cost = holding_cost * area_holding / num_months
    avg_shortage_cost = shortage_cost * area_shortage / num_months
    total_cost = avg_ordering_cost + avg_holding_cost + avg_shortage_cost
    return [smalls, bigs, total_cost, avg_ordering_cost, avg_holding_cost, avg_shortage_cost]

# Function to update time-averaged statistics
def update_time_avg_stats():
    global area_holding, area_shortage, time_last_event
    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time
    if inv_level < 0:
        area_shortage -= inv_level * time_since_last_event
    elif inv_level > 0:
        area_holding += inv_level * time_since_last_event

# Function to generate a random integer based on probability distribution
def random_integer(prob_distrib):
    u = random.random()
    for i in range(1, len(prob_distrib)):
        if u < prob_distrib[i]:
            return i
    return len(prob_distrib) - 1

# Function to generate a uniform random variate
def uniform(a, b):
    return a + random.random() * (b - a)

# Function to generate an exponential random variate
def expon(mean):
    return -mean * math.log(random.random())

# Function to determine the next event
def timing():
    global next_event_type, sim_time, time_next_event
    min_time_next_event = 1.0e+29
    next_event_type = 0
    for i in range(1, num_events + 1):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i
    if next_event_type == 0:
        raise Exception(f"Event list empty at time {sim_time}")
    sim_time = min_time_next_event

# Main function
def main():
    global num_policies, num_events, smalls, bigs
    read_input()
    num_events = 4
    results = []

    print("Single-product inventory system\n")
    print(f"Initial inventory level{int(initial_inv_level):24d} items\n")
    print(f"Number of demand sizes{int(num_values_demand):25d}\n")
    print("Distribution function of demand sizes ", end="")
    for i in range(1, num_values_demand + 1):
        print(f"{prob_distrib_demand[i]:8.3f}", end="")
    print("\n")
    print(f"Mean interdemand time{mean_interdemand:26.2f}\n")
    print(f"Delivery lag range{minlag:29.2f} to{maxlag:10.2f} months\n")
    print(f"Length of the simulation{int(num_months):23d} months\n")
    print(f"Setup cost (K) ={setup_cost:6.1f} \nIncremental cost (i) ={incremental_cost:6.1f} \nHolding cost (h) ={holding_cost:6.1f} \nShortest cost (pi) ={shortage_cost:6.1f}\n")
#   Setup cost (K)                          : 32.0  
#   Incremental cost (i)                    : 3.0  
#   Holding cost (h)                        : 1.0  
#   Shortest cost (pi)                      : 5.0  
    print(f"Number of policies{int(num_policies):29d}\n")


    lines = input_data.strip().split('\n')
    policies = [list(map(int, line.split())) for line in lines[2:2 + int(num_policies)]]

    for smalls, bigs in policies:
        # print(f"Running simulation for policy (smalls={smalls}, bigs={bigs})")
        initialize()
        while next_event_type != 3:
            timing()
            update_time_avg_stats()
            if next_event_type == 1:
                order_arrival()
            elif next_event_type == 2:
                demand()
            elif next_event_type == 4:
                evaluate()
            # print(f"sim_time={sim_time}, inv_level={inv_level}, next_event_type={next_event_type}")
        results.append(report())

    # Print results in tabular format
    headers = ["Policy", " Average Total Cost", "Average Ordering Cost", "Average Holding Cost", "Average Shortage Cost"]
    table = [[f"({s}, {b})", tc, oc, hc, sc] for s, b, tc, oc, hc, sc in results]
    # print("\n\n")
    print(tabulate(table, headers=headers, floatfmt=".2f"))

if __name__ == "__main__":
    main()