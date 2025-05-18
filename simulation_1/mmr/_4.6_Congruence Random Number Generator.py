def linear_congruential_generator(seed, a, c, m, n):
    random_numbers = []
    X = seed

    for _ in range(n):
        # Apply the linear congruential formula
        X = (a * X + c) % m
        random_numbers.append(X)

    return random_numbers

# User input for seed and parameters
seed_input = int(input("Enter a seed (integer): "))
a_input = int(input("Enter the multiplier (a): "))
c_input = int(input("Enter the increment (c): "))
m_input = int(input("Enter the modulus (m): "))
n_input = int(input("Enter the number of random numbers to generate: "))

# Generate random numbers using LCG
random_numbers = linear_congruential_generator(seed_input, a_input, c_input, m_input, n_input)
print("Generated Random Numbers:", random_numbers)
