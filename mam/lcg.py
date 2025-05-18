import matplotlib.pyplot as plt
import numpy as np

def linear_congruential_method(x0, m, a, c, n):
    random_nums = [0] * n
    random_nums[0] = x0
    
    for i in range(1, n):
        random_nums[i] = ((random_nums[i - 1] * a) + c) % m
    
    return random_nums

def generate_and_plot_lcg(x0=5, m=7, a=3, c=3, n=10):
    random_nums = linear_congruential_method(x0, m, a, c, n)
    
    plt.figure(figsize=(12, 8))
    
    plt.plot(random_nums, marker='o', color='#3498db', linestyle='-', 
             linewidth=2, markersize=8, markerfacecolor='white', 
             markeredgecolor='#3498db', markeredgewidth=2)
    
    for i, val in enumerate(random_nums):
        plt.annotate(f'{val}', (i, val), textcoords="offset points", 
                    xytext=(0, 10), ha='center', fontsize=10, 
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    plt.title(f"Linear Congruential Generator\n$X_{{n+1}} = (a·X_n + c) \\, mod \\, m$ where a={a}, c={c}, m={m}, $X_0$={x0}", 
              fontsize=14, pad=20)
    
    plt.xlabel("Iteration", fontsize=12)
    plt.ylabel("Generated Value", fontsize=12)
    
    plt.xticks(range(n), [f'{i}' for i in range(n)])
    
    min_val, max_val = min(random_nums), max(random_nums)
    padding = (max_val - min_val) * 0.1 if max_val > min_val else 0.5
    plt.ylim(max(0, min_val - padding), max_val + padding)
    
    if min_val <= 0:
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.gca().set_facecolor('#f8f9fa')
    
    info_text = f"Period length: {len(set(random_nums))}\nRange: [{min_val}, {max_val}]"
    plt.figtext(0.02, 0.02, info_text, fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
    
    plt.fill_between(range(len(random_nums)), random_nums, alpha=0.2, color='#3498db')
    
    plt.tight_layout()
    plt.show()
    
    return random_nums

linear_congruential_method(5, 7, 3, 3, 10)
generate_and_plot_lcg(5, 7, 3, 3, 10)

# Explanations:
# -------------
# Linear Congruential Generator (LCG):
# This is a common pseudorandom number generator algorithm that uses the recurrence relation:
# X_{n+1} = (a·X_n + c) mod m
# 
# Where:
# - X_n is the current value in the sequence
# - X_{n+1} is the next value in the sequence
# - a is the multiplier
# - c is the increment
# - m is the modulus
# - X_0 is the initial seed value
# 
# The function linear_congruential_method() implements the LCG algorithm:
# - It initializes an array to store the generated random numbers
# - Sets the first element to the seed value X_0
# - Computes subsequent values using the LCG formula
# - Returns the array of generated values
# 
# The function generate_and_plot_lcg():
# - Generates random numbers using the LCG algorithm
# - Creates a visualization of the generated sequence
# - The plot displays each number in the sequence as a point on a line
# - Each point is labeled with its value
# - The title shows the LCG formula and the parameter values used
# - A summary of the sequence properties (period length and range) is shown in the bottom-left corner
# - The x-axis shows the iteration number (0, 1, 2, ...)
# - The y-axis shows the generated values
# 
# Style elements in the plot:
# - Blue line with white-filled circle markers
# - Value labels above each point
# - Light gray grid lines
# - Light blue shading under the curve
# - Light gray background
# - Information text in the bottom-left corner showing period length and range