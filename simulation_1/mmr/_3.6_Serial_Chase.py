import math
from tabulate import tabulate

def distance(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

# Initialize positions
a = (10, 10)
b = (30, 10)
c = (30, 30)
d = (10, 30)

# Initialize velocities
va = 35
vb = 25
vc = 15
vd = 10

# Initialize time and time increment
time = 0
delt = 0.001

# Print table headers
print("   t           A                B                C               D")
print("--------------------------------------------------------------------------")

# List to store rows for tabulation
rows = []

while True:
    # Calculate distances between the objects
    distance_AB = distance(a, b)
    distance_BC = distance(b, c)
    distance_CD = distance(c, d)

    # Update the positions of the objects
    a = (a[0] + va * delt * (b[0] - a[0]) / distance_AB, a[1] + va * delt * (b[1] - a[1]) / distance_AB)
    b = (b[0] - vb * delt * (b[0] - c[0]) / distance_BC, b[1] + vb * delt * (c[1] - b[1]) / distance_BC)
    c = (c[0] - vc * delt * (c[0] - d[0]) / distance_CD, c[1] - vc * delt * (c[1] - d[1]) / distance_CD)
    d = (d[0] - vd * delt, d[1])  # D moves in a straight line in the y direction

    # Append the current positions to rows
    rows.append([f"{time:.3f}", f"({a[0]:.3f}, {a[1]:.3f})", f"({b[0]:.3f}, {b[1]:.3f})", 
                 f"({c[0]:.3f}, {c[1]:.3f})", f"({d[0]:.3f}, {d[1]:.3f})"])

    # Check for collisions
    if distance_AB < 0.005:
        print("A hits B")
        break
    elif distance_BC < 0.005:
        print("B hits C")
        break
    elif distance_CD < 0.005:
        print("C hits D")
        break

    # Increase time
    time += delt

# Print the table
print(tabulate(rows, headers=["Time", "A Position", "B Position", "C Position", "D Position"], tablefmt="grid"))
