import random
import matplotlib.pyplot as plt
import numpy as np

game_count = 7
total_profit = 0

all_iteration_counts = []
all_profits = []
game_numbers = list(range(1, game_count + 1))
cumulative_profit = []
running_profit = 0

for game in range(game_count):
    cumulative_H = 0
    cumulative_T = 0
    iteration_count = 0
    
    while abs(cumulative_H - cumulative_T) < 3:
        iteration_count += 1
        random_number = random.randint(0, 9)
        
        if random_number < 5:
            cumulative_H += 1
        else:
            cumulative_T += 1
    
    profit = 8 - iteration_count
    total_profit += profit
    
    all_iteration_counts.append(iteration_count)
    all_profits.append(profit)
    running_profit += profit
    cumulative_profit.append(running_profit)
    
    print(f"Game {game+1}:")
    print(f"  Iteration count: {iteration_count}")
    print(f"  Final H count: {cumulative_H}, Final T count: {cumulative_T}")
    print(f"  Profit/Loss: {profit}")

print(f"\nTotal games played: {game_count}")
print(f"Total profit/loss: {total_profit}")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.bar(game_numbers, all_iteration_counts, color='skyblue')
plt.title('Number of Iterations per Game')
plt.xlabel('Game Number')
plt.ylabel('Iteration Count')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.subplot(1, 2, 2)
plt.bar(game_numbers, all_profits, color=np.where(np.array(all_profits) >= 0, 'green', 'red'))
plt.axhline(y=0, color='black', linestyle='-')
plt.title('Profit/Loss per Game')
plt.xlabel('Game Number')
plt.ylabel('Profit/Loss')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.suptitle('Gambling Game Simulation Results', fontsize=16)
plt.subplots_adjust(top=0.9)

plt.show()

