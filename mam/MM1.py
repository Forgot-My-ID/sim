import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import gridspec


def visualize_exponential_distribution(lambda_param, title):
    x = np.linspace(0, 5/lambda_param, 1000)
    y = lambda_param * np.exp(-lambda_param * x)
    
    samples = np.random.exponential(1/lambda_param, 1000)
    
    return x, y, samples


def MM1(maximum_number_of_customers, mean_arrival_time, mean_service_time):
    arrival_rate = 1 / mean_arrival_time
    service_rate = 1 / mean_service_time
    
    x_arrival, y_arrival, arrival_samples = visualize_exponential_distribution(arrival_rate, f"Arrival Rate (λ={arrival_rate:.4f} per minute)")
    x_service, y_service, service_samples = visualize_exponential_distribution(service_rate, f"Service Rate (μ={service_rate:.4f} per minute)")
    
    fig_dist = plt.figure(figsize=(15, 10))
    
    ax_arrival_pdf = plt.subplot(2, 2, 1)
    ax_arrival_pdf.plot(x_arrival, y_arrival, 'b-', linewidth=2, 
                       label=f"PDF: λ={arrival_rate:.4f} (λ=1/mean arrival time={1/mean_arrival_time:.4f})")
    ax_arrival_pdf.fill_between(x_arrival, y_arrival, alpha=0.3)
    ax_arrival_pdf.set_title("Exponential Distribution: Arrival Rate")
    ax_arrival_pdf.set_xlabel("Time (minutes)")
    ax_arrival_pdf.set_ylabel("Probability Density")
    ax_arrival_pdf.grid(True, alpha=0.3)
    ax_arrival_pdf.legend()
    
    ax_arrival_hist = plt.subplot(2, 2, 2)
    ax_arrival_hist.hist(arrival_samples, bins=30, density=True, alpha=0.6, label="Samples Histogram")
    ax_arrival_hist.plot(x_arrival, y_arrival, 'b-', linewidth=2, 
                        label=f"Theoretical PDF: λ={arrival_rate:.4f} (λ=1/{mean_arrival_time:.2f})")
    ax_arrival_hist.set_title("Random Samples: Arrival Rate")
    ax_arrival_hist.set_xlabel("Time (minutes)")
    ax_arrival_hist.set_ylabel("Frequency")
    ax_arrival_hist.grid(True, alpha=0.3)
    ax_arrival_hist.legend()
    
    ax_service_pdf = plt.subplot(2, 2, 3)
    ax_service_pdf.plot(x_service, y_service, 'r-', linewidth=2, 
                       label=f"PDF: μ={service_rate:.4f} (μ=1/mean service time={1/mean_service_time:.4f})")
    ax_service_pdf.fill_between(x_service, y_service, alpha=0.3, color='red')
    ax_service_pdf.set_title("Exponential Distribution: Service Rate")
    ax_service_pdf.set_xlabel("Time (minutes)")
    ax_service_pdf.set_ylabel("Probability Density")
    ax_service_pdf.grid(True, alpha=0.3)
    ax_service_pdf.legend()
    
    ax_service_hist = plt.subplot(2, 2, 4)
    ax_service_hist.hist(service_samples, bins=30, density=True, alpha=0.6, color='salmon', label="Samples Histogram")
    ax_service_hist.plot(x_service, y_service, 'r-', linewidth=2, 
                        label=f"Theoretical PDF: μ={service_rate:.4f} (μ=1/{mean_service_time:.2f})")
    ax_service_hist.set_title("Random Samples: Service Rate")
    ax_service_hist.set_xlabel("Time (minutes)")
    ax_service_hist.set_ylabel("Frequency")
    ax_service_hist.grid(True, alpha=0.3)
    ax_service_hist.legend()
    
    fig_dist.suptitle("MM1 Queue: Exponential Distributions for Arrival and Service Rates", fontsize=16)
    plt.tight_layout()
    fig_dist.subplots_adjust(top=0.9)
    plt.show()
    
    customer = []
    wait_time = []
    service_time = []
    arrival_time = []
    departure_time = []
    system_idle_time = 0
    time = 0.0
    number_of_process = maximum_number_of_customers
    
    for i in range(number_of_process):
        arrival = np.random.exponential(1 / arrival_rate) * 60
        service = np.random.exponential(1 / service_rate) * 60
        data = [arrival, service]
        customer.append(data)
        service_time.append(service)
        arrival_time.append(arrival)

    customer.sort(key=lambda x: x[0])
    arrival_time.sort()
    
    print("Customer data (arrival time, service time):")
    print(customer)
    
    for i in range(number_of_process):
        if time < customer[i][0]:
            system_idle_time += abs(time - customer[i][0])
            time = customer[i][0]

        if time > customer[i][0]:
            wait_time.append(abs(time - customer[i][0]))
        else:
            wait_time.append(0)

        time = time + customer[i][1]
        departure_time.append(time)

    average_wait = sum(wait_time) / number_of_process
    system_utilization = ((time - system_idle_time) / time) * 100
    
    print("\nSimulation Results:")
    print(f"Average Delay in Queue: {round(average_wait, 2)} seconds")
    print(f"System Utilization: {round(system_utilization, 2)}%")
    print(f"Time Simulation Ended: {round(time, 2)} seconds")
    
    fig = plt.figure(figsize=(18, 12))
    gs = gridspec.GridSpec(2, 2, width_ratios=[1.5, 1], height_ratios=[1, 1])
    
    ax1 = plt.subplot(gs[0, 0])
    ax1.set_title("MM1 Queue Simulation: Customer Timeline")
    
    for i in range(number_of_process):
        ax1.plot(arrival_time[i], i, 'bo', markersize=8, label='Customer Arrival Point' if i == 0 else "")
        
        if wait_time[i] > 0:
            ax1.plot([arrival_time[i], arrival_time[i] + wait_time[i]], [i, i], 'r-', linewidth=2, 
                     label='Customer Waiting Period' if i == 0 else "")
        
        ax1.plot([arrival_time[i] + wait_time[i], departure_time[i]], [i, i], 'g-', linewidth=4,
                label='Customer Service Duration' if i == 0 else "")
        
        ax1.plot(departure_time[i], i, 'ko', markersize=8, label='Customer Departure Point' if i == 0 else "")
    
    ax1.set_xlabel("Time (seconds)")
    ax1.set_ylabel("Customer ID")
    ax1.grid(True, alpha=0.3)
    
    handles, labels = ax1.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax1.legend(by_label.values(), by_label.keys(), loc='best')
    
    ax2 = plt.subplot(gs[1, 0])
    
    events = [(t, 1) for t in arrival_time] + [(t, -1) for t in departure_time]
    events.sort(key=lambda x: x[0])
    
    times = [0]
    queue_lengths = [0]
    current_length = 0
    
    for event_time, event_type in events:
        current_length += event_type
        times.append(event_time)
        queue_lengths.append(current_length)
    
    ax2.step(times, queue_lengths, where='post', linewidth=2, label="Number of Customers in Queue")
    ax2.fill_between(times, queue_lengths, step="post", alpha=0.3, label="Queue Occupancy")
    ax2.set_title("MM1 Queue: Queue Length Over Time")
    ax2.set_xlabel("Time (seconds)")
    ax2.set_ylabel("Number of Customers in System")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='best')
    
    ax3 = plt.subplot(gs[0, 1])
    ax3.barh(y=[i for i in range(number_of_process)], width=wait_time, left=[i for i in arrival_time], 
             color='red', alpha=0.6, label='Customer Waiting Time (Queue Delay)')
    ax3.barh(y=[i for i in range(number_of_process)], width=service_time, 
             left=[arrival_time[i] + wait_time[i] for i in range(number_of_process)], 
             color='green', alpha=0.6, label='Customer Service Time (Processing Duration)')
    
    ax3.set_title("MM1 Queue: Customer Wait and Service Times")
    ax3.set_xlabel("Time (seconds)")
    ax3.set_ylabel("Customer ID")
    ax3.legend(loc='best')
    ax3.grid(True, alpha=0.3)
    
    ax4 = plt.subplot(gs[1, 1])
    labels = ['System Busy (Server Processing Customers)', 'System Idle (Server Waiting for Arrivals)']
    sizes = [system_utilization, 100 - system_utilization]
    colors = ['#66b3ff', '#ff9999']
    explode = (0.1, 0)
    
    ax4.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax4.axis('equal')
    ax4.set_title("MM1 Queue: System Utilization Distribution")
    
    plt.suptitle("MM1 Queue Simulation Analysis", fontsize=16)
    plt.tight_layout()
    fig.subplots_adjust(top=0.92)
    plt.show()


MM1(10, 53.33, 17.5)


"""
DETAILED FUNCTION EXPLANATIONS:

1. visualize_exponential_distribution(lambda_param, title):
   This function creates a visualization of the exponential distribution with the given lambda parameter.
   
   How it works:
   - It generates x values linearly spaced from 0 to 5/lambda_param (covering 5 times the mean)
   - It calculates the probability density function (PDF) values using the formula: λe^(-λx)
   - It generates 1000 random samples from the exponential distribution with mean 1/lambda_param
   - It returns the x values, y values (PDF), and the random samples
   
   Why it works:
   - The exponential distribution is defined by the PDF formula λe^(-λx)
   - The mean of an exponential distribution is 1/λ
   - Using np.linspace ensures we have enough points to create a smooth curve
   - np.random.exponential generates random values following the exponential distribution

2. MM1(maximum_number_of_customers, mean_arrival_time, mean_service_time):
   This function simulates an M/M/1 queuing system and visualizes the results.
   
   How it works:
   
   a) Distribution Visualization:
      - Converts mean times to rates (λ = 1/mean_arrival_time, μ = 1/mean_service_time)
      - Visualizes both the theoretical exponential distributions and random samples
      - Creates four subplots showing the PDFs and histograms of samples
   
   b) Simulation Process:
      - Initializes empty lists to store customer data
      - Generates random arrival and service times from exponential distributions
      - Converts times to seconds (multiplying by 60)
      - Sorts customers by arrival time
      - Processes each customer sequentially:
        * If a customer arrives when the system is idle, update system idle time
        * If a customer arrives when the system is busy, calculate their wait time
        * Update the simulation time after each customer's service
        * Record departure times
      - Calculates metrics like average wait time and system utilization
   
   c) Visualization of Results:
      - Creates a comprehensive visualization with four panels:
        1. Customer Timeline: Shows arrival, waiting, and service times for each customer
        2. Queue Length Over Time: Shows how many customers are in the system at any time
        3. Wait Times Bar Chart: Compares waiting and service times for each customer
        4. System Utilization Pie Chart: Shows the percentage of time the system is busy vs idle
   
   Why it works:
   - The M/M/1 queue assumes exponentially distributed interarrival and service times
   - The simulation uses a discrete-event approach, processing one customer at a time
   - By tracking the system state at each customer arrival and departure, we can calculate key metrics
   - The events-based approach to tracking queue length ensures we capture all changes in system state
   - The visualizations provide multiple perspectives on the queuing system's behavior
   
   Key Queue Theory Concepts:
   - Arrival Rate (λ): Average number of customers arriving per unit time
   - Service Rate (μ): Average number of customers served per unit time
   - Utilization (ρ): Percentage of time the server is busy (λ/μ)
   - For a stable queue, utilization must be less than 1 (λ < μ)
   - The exponential distribution models the "memoryless" property of Poisson processes
"""