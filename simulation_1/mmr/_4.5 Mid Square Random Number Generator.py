def mid_square_random_number_generator(seed, n):
    # Determine the number of digits in the seed
    var = int(len(str(seed)) / 2)
    rn = []

    for _ in range(n):
        # Square the seed
        x = seed ** 2
        
        # Convert to string to extract middle digits
        st = str(x)
        dig = len(st)
        
        # Determine the starting index to extract middle digits
        start = (dig // 2) - var
        end = (dig // 2) + var
        
        # Extract middle digits and update seed
        r = st[start:end]
        seed = int(r)
        
        # Append to the list of random numbers
        rn.append(seed)

    return rn

# User input for seed and number of random numbers to generate
seed_input = int(input("Enter a seed (4 or 6 digits): "))
n_input = int(input("Enter the number of random numbers to generate: "))

# Ensure the seed is valid (4 or 6 digits)
if len(str(seed_input)) not in [4, 6]:
    print("Please enter a valid 4 or 6 digit seed.")
else:
    random_numbers = mid_square_random_number_generator(seed_input, n_input)
    print("Generated Random Numbers:", random_numbers)
