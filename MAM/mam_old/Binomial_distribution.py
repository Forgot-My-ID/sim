import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# Parameters for the Binomial distribution
n = 10      # Number of trials
p = 0.5     # Probability of success

# Generate a range of possible outcomes
x = np.arange(0, n + 1)

# Calculate the probability mass function for each outcome
binom_pmf = binom.pmf(x, n, p)

# Plot the Binomial distribution
plt.figure(figsize=(10, 6))
plt.bar(x, binom_pmf, color='blue', alpha=0.7)
plt.xlabel('Number of Successes')
plt.ylabel('Probability')
plt.title(f'Binomial Distribution (n={n}, p={p})')
plt.show()
