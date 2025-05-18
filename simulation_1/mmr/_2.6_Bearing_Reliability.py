import random
import matplotlib.pyplot as plt

# Define life and probability lists
life = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
probability = [0.10, .14, .24, .14, .12, .10, .06, .05, .03, 0.02]
probability = [int(i * 100) for i in probability]

# Cumulative probabilities for life
c_probability = [probability[0]]
for i in range(1, len(probability)):
    c_probability.append(c_probability[i - 1] + probability[i])

# Delay and probabilities
delay = [4, 6, 8]
delay_probability = [0.3, 0.6, 0.1]
delay_probability = [int(i * 10) for i in delay_probability]

# Cumulative probabilities for delay
c_delay_pro = [delay_probability[0]]
for i in range(1, len(delay_probability)):
    c_delay_pro.append(c_delay_pro[i - 1] + delay_probability[i])

# Functions to get bearing life and delays
def clock():
    x = random.randint(1, 100)
    for i, cp in enumerate(c_probability):
        if x <= cp:
            return life[i]

def late():
    x = random.randint(1, 10)
    for i, cp in enumerate(c_delay_pro):
        if x <= cp:
            return delay[i]

# Generate lifetimes for bearings
bearing1_life, bearing2_life, bearing3_life = [], [], []
for bearing_life in [bearing1_life, bearing2_life, bearing3_life]:
    lf = 0
    while lf < 20000:
        i = clock()
        lf += i
        bearing_life.append(i)

# Count two and three-down situations
two_down, three_down = 0, 0
for life1, life2, life3 in zip(bearing1_life, bearing2_life, bearing3_life):
    if life1 == life2 == life3:
        three_down += 1
    elif life1 == life2 or life2 == life3 or life3 == life1:
        two_down += 1

# Calculate costs
num_of_bearing = sum([len(bearing1_life), len(bearing2_life), len(bearing3_life)])
total_bearing_cost = num_of_bearing * 20

mechanic_delay = []
num_of_mechanic_call = num_of_bearing - two_down - (three_down * 2)
for _ in range(num_of_mechanic_call):
    mechanic_delay.append(late())
total_delay_cost = sum(mechanic_delay) * 5

time_needed = (num_of_bearing * 20) - (two_down * 10) - (three_down * 20)
total_repair_cost = (time_needed / 60) * 25

total_cost = total_bearing_cost + total_delay_cost + total_repair_cost

# New simulation with optimization
bearing_life = []
mechanic_delay_2 = []
lf = 0
while lf < 20000:
    life_of_bearings = [clock(), clock(), clock()]
    x = min(life_of_bearings)
    y = late()
    bearing_life.append(x)
    mechanic_delay_2.append(y)
    lf += x

# New cost calculation
total_bearing_cost = len(bearing_life) * 20
total_delay_cost = sum(mechanic_delay_2) * 5
total_repair_cost = ((len(bearing_life) * 40) / 60) * 25
total_cost_2 = total_bearing_cost + total_delay_cost + total_repair_cost

# Results
print("Previous Cost : ", total_cost)
print("New Cost : ", total_cost_2)
print("Saves : ", total_cost - total_cost_2)

# Visualization
plt.figure(figsize=(14, 8))

# Plot lifetimes
plt.subplot(2, 2, 1)
plt.plot(bearing1_life, label="Bearing 1", color="blue")
plt.plot(bearing2_life, label="Bearing 2", color="green")
plt.plot(bearing3_life, label="Bearing 3", color="red")
plt.title("Bearing Lifetimes")
plt.xlabel("Cycle")
plt.ylabel("Lifetime (hours)")
plt.legend()

# Plot delay distribution
plt.subplot(2, 2, 2)
plt.hist(mechanic_delay, bins=10, color="purple", edgecolor="black", alpha=0.7)
plt.title("Mechanic Delay Distribution")
plt.xlabel("Delay (hours)")
plt.ylabel("Frequency")

# Cost comparison
plt.subplot(2, 2, 3)
costs = [total_cost, total_cost_2]
labels = ["Previous Cost", "New Cost"]
plt.bar(labels, costs, color=["orange", "teal"])
plt.title("Cost Comparison")
plt.ylabel("Cost")

# Delay comparison for optimized scenario
plt.subplot(2, 2, 4)
plt.hist(mechanic_delay_2, bins=10, color="purple", edgecolor="black", alpha=0.7)
plt.title("Optimized Mechanic Delay Distribution")
plt.xlabel("Delay (hours)")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()
