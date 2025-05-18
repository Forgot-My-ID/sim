import math
import random
import matplotlib.pyplot as plt

def func(x):
    val = 1-(x**2)
    val = math.sqrt(val)
    return val

m = 0
n = 0

for i in range(100):
    rx = random.randint(0,1000)
    rx = rx/1000
    ry = random.randint(0,1000)
    ry = ry/1000
    n+=1

    if ry <= func(rx):
        m+=1
        plt.scatter(rx,ry,color = "green")
    else:
        plt.scatter(rx,ry,color = "blue")

x = []
y = []
i=0
h=0.01
while i<=1:
    x.append(i)
    y.append(round(func(i),5))
    i+=h
    i = round(i, 2)
plt.plot(x,y,color = "red")
plt.show()