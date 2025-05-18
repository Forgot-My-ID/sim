n = 10

ri = [12]
a = 13
b = 1
m = 97

i = 1
while i <= 10:
    rn = ((a * ri[i - 1]) + b) % m
    ri.append(rn)
    i += 1

for i in range(n + 1):
    ri[i] = ri[i] / 100
ri = ri[1:]

ri.sort()
print(ri)


one_by_n = []

i = 1
while i <= n:
    one_by_n.append(i / n)
    i += 1
one_by_n

one_by_n_sub_ri = []

for i in range(n):
    one_by_n_sub_ri.append(one_by_n[i] - ri[i])

positived = max(one_by_n_sub_ri)
positived

ri_sub_i_sub_1_div_n = ri.copy()

i = 1
while i < n:
    ri_sub_i_sub_1_div_n[i] = ri_sub_i_sub_1_div_n[i] - one_by_n[i - 1]
    i += 1

negatived = max(ri_sub_i_sub_1_div_n)
negatived

print("Positive deviation ",positived,"Negative deviation ", negatived)

longest_dev = max(positived, negatived)

print("Longest Deviation", longest_dev)

if longest_dev < 0.368:
    print("99%")
elif longest_dev < 0.410:
    print("95%")
else:
    print("Failed")