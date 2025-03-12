import math


def binomial_distribution(n, x, p):
    # Calculate the binomial coefficient (n choose x)
    binom_coeff = math.comb(n, x)

    # Calculate the probability using the binomial formula
    probability = binom_coeff * (p ** x) * ((1 - p) ** (n - x))

    return probability


# Example usage
n = 10  # Total number of trials
x = 3  # Number of successes
p = 0.5  # Probability of success in each trial

result = binomial_distribution(n, x, p)
print(f'P(X = {x}) = {result:.5f}')
