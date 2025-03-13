import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import math
import time
import random

MAX_QUEUE_SIZE = 100  
SERVER_BUSY = 1       
SERVER_IDLE = 0       
event_type = 0        
customers_served = 0  
total_customers_needed = 0  
event_count = 2       
queue_length = 0      
server_state = SERVER_IDLE  
queue_area = 0.0      
server_busy_area = 0.0  
avg_arrival_time = 0.0  
avg_service_time = 0.0  
current_time = 0.0    
total_wait_time = 0.0  
arrival_times = [0.0] * (MAX_QUEUE_SIZE + 1)  
previous_event_time = 0.0  
next_event_times = [0.0] * 3  
wait_time_list = []  
customer_list = []  
entry_exit_times = []  

def generate_exponential(mean):
    return -mean * math.log(random.random())

def initialize():
    global current_time, server_state, queue_length, previous_event_time
    global customers_served, total_wait_time, queue_area, server_busy_area, next_event_times
    global customer_list, wait_time_list, entry_exit_times

    current_time = 0.0
    server_state = SERVER_IDLE
    queue_length = 0
    previous_event_time = 0.0
    customers_served = 0
    total_wait_time = 0.0
    queue_area = 0.0
    server_busy_area = 0.0
    customer_list = []
    wait_time_list = []
    entry_exit_times = []  

    next_event_times[1] = current_time + generate_exponential(avg_arrival_time)
    next_event_times[2] = 1.0e+30  

def find_next_event():
    global event_type, current_time
    next_time = 1.0e+29
    event_type = 0
    for i in range(1, event_count + 1):
        if next_event_times[i] < next_time:
            next_time = next_event_times[i]
            event_type = i

    if event_type == 0:
        print("\nError: Event list empty at time", current_time)
        exit(1)

    current_time = next_time

def process_arrival():
    global queue_length, server_state, customers_served, total_wait_time
    global customer_list, wait_time_list, entry_exit_times

    next_event_times[1] = current_time + generate_exponential(avg_arrival_time)  

    arrival = current_time
    service = generate_exponential(avg_service_time)
    customer_data = [arrival, service]
    customer_list.append(customer_data)

    entry_exit_times.append([arrival, None])  

    if server_state == SERVER_BUSY:
        queue_length += 1
        if queue_length > MAX_QUEUE_SIZE:
            print("\nError: Queue overflow at time", current_time)
            exit(2)
        arrival_times[queue_length] = current_time  
    else:
        wait_time = 0.0  
        total_wait_time += wait_time
        customers_served += 1
        server_state = SERVER_BUSY
        next_event_times[2] = current_time + service

        entry_exit_times[-1][1] = current_time + service  

def process_departure():
    global queue_length, server_state, customers_served, total_wait_time
    global customer_list, wait_time_list, entry_exit_times

    if queue_length == 0:
        server_state = SERVER_IDLE
        next_event_times[2] = 1.0e+30  
    else:
        queue_length -= 1
        wait_time = current_time - arrival_times[1]  
        total_wait_time += wait_time
        wait_time_list.append(wait_time)  
        customers_served += 1

        entry_exit_times[queue_length][1] = current_time + generate_exponential(avg_service_time)

        for i in range(1, queue_length + 1):
            arrival_times[i] = arrival_times[i + 1]

        next_event_times[2] = current_time + generate_exponential(avg_service_time)

def show_progress():
    progress = customers_served / total_customers_needed
    bar_length = 30
    filled_length = int(bar_length * progress)

    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    percent = progress * 100

    print(f"\rProgress: |{bar}| {percent:.1f}% ({customers_served}/{total_customers_needed} customers)", end='')

    if customers_served >= total_customers_needed:
        print()

def generate_report():
    global current_time, total_wait_time, customers_served

    print("\n" + "="*60)
    print(f"{'SINGLE-SERVER QUEUE SIMULATION RESULTS':^60}")
    print("="*60)

    print("\n Simulation Parameters:")
    print(f"  • Mean time between arrivals: {avg_arrival_time:.3f} minutes")
    print(f"  • Mean service time: {avg_service_time:.3f} minutes")
    print(f"  • Total customers simulated: {total_customers_needed}")

    print("\n Performance Metrics:")

    if customers_served > 0:
        avg_wait = total_wait_time / customers_served
        print(f"  • Average wait time in queue: {avg_wait:.3f} minutes")
    else:
        print("  • Average wait time in queue: N/A (No customers served)")

    if current_time > 0:
        avg_queue = queue_area / current_time
        utilization = server_busy_area / current_time
        print(f"  • Average number in queue: {avg_queue:.3f} customers")
        print(f"  • Server utilization: {utilization:.3f} ({utilization*100:.1f}%)")
        print(f"  • Simulation end time: {current_time:.3f} minutes")
    else:
        print("  • Average number in queue: N/A (Simulation has not started)")
        print("  • Server utilization: N/A (Simulation has not started)")
        print("  • Simulation end time: N/A (Simulation has not started)")

def update_statistics():
    global queue_area, server_busy_area, previous_event_time
    time_difference = current_time - previous_event_time
    previous_event_time = current_time
    queue_area += queue_length * time_difference  
    server_busy_area += server_state * time_difference  

def MM1():
    global customers_served, avg_arrival_time, avg_service_time, total_customers_needed

# 97 1083 70670
    random.seed(70670)  

    print("\n" + "="*60)
    print(f"{'QUEUE SIMULATION SYSTEM':^60}")
    print("="*60)
    print("\nStarting simulation with the following parameters:")
    print(f"  • Average arrival rate: 1 customer every {avg_arrival_time:.1f} minutes")
    print(f"  • Average service time: {avg_service_time:.1f} minutes per customer")
    print(f"  • Target customers to serve: {total_customers_needed}")
    print("\nRunning simulation...")

    initialize()

    progress_interval = max(1, total_customers_needed // 100)

    while customers_served < total_customers_needed:
        find_next_event()  
        update_statistics()  

        if event_type == 1:
            process_arrival()  
        elif event_type == 2:
            process_departure()  

        if customers_served % progress_interval == 0 or customers_served == total_customers_needed:
            show_progress()  
            time.sleep(0.005)  

    generate_report()  
    # plot_graph()

def plot_graph():
    customer_indices = np.arange(len(entry_exit_times))

    entry_times = np.array([entry_exit_times[i][0] for i in range(len(entry_exit_times))])
    exit_times = np.array([entry_exit_times[i][1] if entry_exit_times[i][1] is not None else current_time for i in range(len(entry_exit_times))])

    plt.barh(customer_indices, exit_times - entry_times, left=entry_times, color='skyblue', edgecolor='black')

    plt.xlabel('Time')
    plt.ylabel('Customer Index')
    
    
    plt.title('M/M/1 Queue')

    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.show()

if __name__ == "__main__":

    avg_arrival_time = 1.0  
    avg_service_time = 0.5  
    total_customers_needed = 1000

    MM1()