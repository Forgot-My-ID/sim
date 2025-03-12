import numpy as np
import matplotlib.pyplot as plt

def exponential_probability(rate_parameter, time):
    lambda_ = 1 / rate_parameter
    return 1 - np.exp(-lambda_ * time)

# Given rate parameter (average time between waves)
average_time_between_waves = 100

# Given time (in this case, 120 days)
time_for_next_wave = 120

# Calculate the probability for the given time using the Exponential distribution
probability = exponential_probability(average_time_between_waves, time_for_next_wave)

print(f"The probability that it will take more than 120 days for the next wave to occur is: {probability:.4f}")

# Simulate and plot Exponential distributions with different rate parameters
rate_parameters = [0.5, 1.0, 2.0, 4.0]
plt.figure(figsize=(12, 8))

for i, rate_parameter in enumerate(rate_parameters, 1):
    samples = np.random.exponential(scale=1 / rate_parameter, size=1000)
    mean_time = np.mean(samples)
    print(f"Simulated mean time between waves (rate parameter = {rate_parameter}): {mean_time:.2f} days")
    
    # Plot histogram for each rate parameter
    plt.subplot(2, 2, i)
    plt.hist(samples, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title(f'Rate Parameter = {rate_parameter}\nMean = {mean_time:.2f} days')
    plt.xlabel('Time between waves (days)')
    plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
