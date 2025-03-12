import math
import time
import random

# Constants
MAX_QUEUE_SIZE = 100  # Maximum queue capacity
SERVER_BUSY = 1       # Server is serving a customer (flag value)
SERVER_IDLE = 0       # Server is available (flag value)

# Simulation state variables
event_type = 0        # Tracks which type of event is being processed (1=arrival, 2=departure)
customers_served = 0  # Counter for total number of customers who completed service
total_customers_needed = 0  # Target number of customers to process before ending simulation
event_count = 2       # Number of possible event types (arrival and departure)
queue_length = 0      # Current number of customers waiting in queue
server_state = SERVER_IDLE  # Current state of the server (busy or idle)

# Statistics tracking variables
queue_area = 0.0      # Accumulator for time-weighted queue length (for average calculation)
server_busy_area = 0.0  # Accumulator for time server is busy (for utilization calculation)
avg_arrival_time = 0.0  # Mean time between customer arrivals
avg_service_time = 0.0  # Mean time to serve a customer
current_time = 0.0    # Current simulation clock time
total_wait_time = 0.0  # Sum of all customer waiting times (for average calculation)

# Arrays to track customer data and event timing
arrival_times = [0.0] * (MAX_QUEUE_SIZE + 1)  # Records when each queued customer arrived
previous_event_time = 0.0  # Time of the last event (for statistical calculations)
next_event_times = [0.0] * 3  # Scheduled times of future events (index 1=arrival, 2=departure)

# Generate exponential random variate - models realistic inter-arrival and service times
# using negative exponential distribution common in queuing theory
def generate_exponential(mean):
    return -mean * math.log(random.random())

# Initialize simulation - sets up initial values and schedules first event
def initialize():
    global current_time, server_state, queue_length, previous_event_time
    global customers_served, total_wait_time, queue_area, server_busy_area, next_event_times
    
    # Reset simulation clock and state variables
    current_time = 0.0
    server_state = SERVER_IDLE
    queue_length = 0
    previous_event_time = 0.0
    
    # Reset statistical counters
    customers_served = 0
    total_wait_time = 0.0
    queue_area = 0.0
    server_busy_area = 0.0
    
    # Schedule first arrival, set departure to far future (effectively infinity)
    next_event_times[1] = current_time + generate_exponential(avg_arrival_time)
    next_event_times[2] = 1.0e+30  # Very large number to represent no departure scheduled

# Find the next event to process - determines which event happens next by finding earliest scheduled time
def find_next_event():
    global event_type, current_time
    
    # Find earliest event
    next_time = 1.0e+29
    event_type = 0
    
    for i in range(1, event_count + 1):
        if next_event_times[i] < next_time:
            next_time = next_event_times[i]
            event_type = i
    
    # Error if no events found (should never happen in proper simulation)
    if event_type == 0:
        print("\n❌ Error: Event list empty at time", current_time)
        exit(1)
    
    # Advance simulation time to the next event
    current_time = next_time

# Process a customer arrival - handles new customer entering the system
def process_arrival():
    global queue_length, server_state, customers_served, total_wait_time
    wait_time = 0.0
    
    # Schedule next arrival (arrivals happen regardless of system state)
    next_event_times[1] = current_time + generate_exponential(avg_arrival_time)
    
    # Check server status
    if server_state == SERVER_BUSY:
        # Server busy, add customer to queue
        queue_length += 1
        
        # Check queue overflow (simulation constraint)
        if queue_length > MAX_QUEUE_SIZE:
            print("\n❌ Error: Queue overflow at time", current_time)
            exit(2)
            
        # Record customer's arrival time for later wait time calculation
        arrival_times[queue_length] = current_time
    else:
        # Server idle, begin service immediately (customer doesn't wait)
        wait_time = 0.0
        total_wait_time += wait_time
        customers_served += 1
        server_state = SERVER_BUSY
        
        # Schedule this customer's departure
        next_event_times[2] = current_time + generate_exponential(avg_service_time)

# Process a customer departure - handles customer finishing service
def process_departure():
    global queue_length, server_state, customers_served, total_wait_time
    wait_time = 0.0
    
    # Check if queue is empty
    if queue_length == 0:
        # No more customers waiting, server goes idle
        server_state = SERVER_IDLE
        next_event_times[2] = 1.0e+30  # No departure scheduled (infinity)
    else:
        # Serve next customer from queue
        queue_length -= 1
        
        # Calculate how long this customer waited (current time - when they arrived)
        wait_time = current_time - arrival_times[1]
        total_wait_time += wait_time
        customers_served += 1
        
        # Schedule this customer's departure
        next_event_times[2] = current_time + generate_exponential(avg_service_time)
        
        # Shift queue - move everyone up one position since first person left queue
        for i in range(1, queue_length + 1):
            arrival_times[i] = arrival_times[i + 1]

# Display progress bar - provides visual feedback during simulation
def show_progress():
    progress = customers_served / total_customers_needed
    bar_length = 30
    filled_length = int(bar_length * progress)
    
    # Create progress bar with filled and empty sections
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    percent = progress * 100
    
    # Display progress
    print(f"\rProgress: |{bar}| {percent:.1f}% ({customers_served}/{total_customers_needed} customers)", end='')
    
    if customers_served >= total_customers_needed:
        print()  # New line after completion

# Generate simulation report - calculates and displays final performance metrics
def generate_report():
    print("\n" + "="*60)
    print(f"{'SINGLE-SERVER QUEUE SIMULATION RESULTS':^60}")
    print("="*60)
    
    print("\n📊 Simulation Parameters:")
    print(f"  • Mean time between arrivals: {avg_arrival_time:.3f} minutes")
    print(f"  • Mean service time: {avg_service_time:.3f} minutes")
    print(f"  • Total customers simulated: {total_customers_needed}")
    
    print("\n📈 Performance Metrics:")
    # Calculate and display average wait time if any customers were served
    if customers_served > 0:
        avg_wait = total_wait_time / customers_served
        print(f"  • Average wait time in queue: {avg_wait:.3f} minutes")
    else:
        print("  • Average wait time in queue: N/A (No customers served)")
    
    # Calculate and display time-averaged statistics if simulation ran
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
    
    # Keep original format for consistency with requirements
    print("\n\nSingle-server queueing system\n")
    print("Mean interarrival time{:11.3f} minutes".format(avg_arrival_time))
    print("Mean service time{:16.3f} minutes".format(avg_service_time))
    print("Number of customers{:14d}".format(total_customers_needed))
    
    if customers_served > 0:
        print("\n\nAverage delay in queue{:11.3f} minutes".format(total_wait_time / customers_served))
    else:
        print("\n\nAverage delay in queue: N/A (No customers have been delayed)")
    
    if current_time > 0:
        print("Average number in queue{:10.3f}".format(queue_area / current_time))
        print("Server utilization{:15.3f}".format(server_busy_area / current_time))
        print("Time simulation ended{:12.3f} minutes".format(current_time))
    else:
        print("Average number in queue: N/A (Simulation has not started)")
        print("Server utilization: N/A (Simulation has not started)")
        print("Time simulation ended: N/A (Simulation has not started)")

# Update time-weighted statistics - maintains accumulators for time-averaged metrics
def update_statistics():
    global queue_area, server_busy_area, previous_event_time
    
    # Calculate time elapsed since last event
    time_difference = current_time - previous_event_time
    previous_event_time = current_time
    
    # Update time-weighted statistical accumulators:
    # - queue_area tracks total customer-minutes spent in queue
    # - server_busy_area tracks total minutes server was busy
    queue_area += queue_length * time_difference
    server_busy_area += server_state * time_difference

# Main simulation function - controls overall simulation flow
def main():
    global customers_served, avg_arrival_time, avg_service_time, total_customers_needed
    
    # Simulation parameters
    avg_arrival_time = 1.0  # Mean time between arrivals (1 customer per minute on average)
    avg_service_time = 0.5  # Mean service time (half a minute per customer on average)
    total_customers_needed = 1000  # Simulation will run until this many customers served
    
    # Set random seed for reproducibility (optional)
    # Using a fixed seed ensures same results each run for testing/debugging
    random.seed(100)
    
    # Show welcome message
    print("\n" + "="*60)
    print(f"{'QUEUE SIMULATION SYSTEM':^60}")
    print("="*60)
    print("\nStarting simulation with the following parameters:")
    print(f"  • Average arrival rate: 1 customer every {avg_arrival_time:.1f} minutes")
    print(f"  • Average service time: {avg_service_time:.1f} minutes per customer")
    print(f"  • Target customers to serve: {total_customers_needed}")
    print("\nRunning simulation...")
    
    # Run simulation
    initialize()
    
    progress_interval = max(1, total_customers_needed // 100)
    
    # Process events until we reach required number of customers
    # This is the main event loop - heart of the discrete event simulation
    while customers_served < total_customers_needed:
        find_next_event()  # Find and advance to next event
        update_statistics()  # Update time-weighted statistics
        
        # Handle event based on type
        if event_type == 1:
            process_arrival()  # Handle customer arrival
        elif event_type == 2:
            process_departure()  # Handle customer departure
        
        # Show progress periodically
        if customers_served % progress_interval == 0 or customers_served == total_customers_needed:
            show_progress()
            time.sleep(0.005)  # Small delay to make progress visible
    
    # Output results
    generate_report()

# Program entry point
if __name__ == "__main__":
    main()