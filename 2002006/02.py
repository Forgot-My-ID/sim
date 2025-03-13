import matplotlib.pyplot as plt
import numpy as np
import random

def random_walk_3d(steps):
    x, y, z = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    directions = ["LEFT", "RIGHT", "FORWARD", "BACKWARD", "UP", "DOWN"]
    step_probabilities = [0.25, 0.35, 0.30, 0.10, 0.80, 0.20]
    for i in range(1, steps):
        step = random.choices(directions, step_probabilities)[0]
        if step == "RIGHT":
            x[i], y[i], z[i] = x[i - 1] + 1, y[i - 1], z[i - 1]
        elif step == "LEFT":
            x[i], y[i], z[i] = x[i - 1] - 1, y[i - 1], z[i - 1]
        elif step == "FORWARD":
            x[i], y[i], z[i] = x[i - 1], y[i - 1] + 1, z[i - 1]
        elif step == "BACKWARD":
            x[i], y[i], z[i] = x[i - 1], y[i - 1] - 1, z[i - 1]
        elif step == "UP":
            x[i], y[i], z[i] = x[i - 1], y[i - 1], z[i - 1] + 1
        elif step == "DOWN":
            x[i], y[i], z[i] = x[i - 1], y[i - 1], z[i - 1] - 1
    return x, y, z

num_steps = 50
x_data, y_data, z_data = random_walk_3d(num_steps)

start_position = (x_data[0], y_data[0], z_data[0])
end_position = (x_data[-1], y_data[-1], z_data[-1])

print(f"Starting position: {start_position}")
print(f"Ending position: {end_position}")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(x_data, y_data, z_data, alpha=0.9)

ax.scatter(x_data[0], y_data[0], z_data[0], color='green', label="Start", s=100)
ax.scatter(x_data[-1], y_data[-1], z_data[-1], color='red', label="End", s=100)

ax.legend()

plt.show()