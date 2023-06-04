import math
from prettytable import PrettyTable
import matplotlib.pyplot as plt

accuracy = 4

x = [-4.38, -3.84, -3.23, -2.76, -2.22, -1.67, -1.13, -0.6]
y = [2.25, 2.83, 3.44, 4.51, 5.29, 6.55, 8.01, 10.04]

n = len(x)

u = []
for i in range(n):
    u.append(round(1 / (x[i]), accuracy))

u2 = []
uy = []

for i in range(n):
    u2.append(round(u[i]*u[i], accuracy))
    uy.append(round(u[i]*y[i], accuracy))

table = PrettyTable()
table.add_column("u", u)
table.add_column("y", y)
table.add_column("u2", u2)
table.add_column("uy", uy)

print(table)

Mu = round(1/n * sum(u), accuracy)
print("Mu = ", Mu)

My = round(1/n * sum(y), accuracy)
print("My = ", My)

Mu2 = round(1/n * sum(u2), accuracy)
print("Mu2 = ", Mu2)

Muy = round(1/n * sum(uy), accuracy)
print("Muy = ", Muy)

print('=' * 30)
a = (Muy - Mu * My)/(Mu2-Mu*Mu)
a = round(a, accuracy)
print("a = ", a)

b = (Mu2 * My - Mu * Muy)/(Mu2-Mu*Mu)
b = round(b, accuracy)
print("b = ", b)


print("Гіперболічне рівняння регресії: y =", a, "/ x +", b)

y1 = []
for i in range(n):
    y1.append(a/x[i] + b)

e2 = []
for i in range(n):
    e2.append(round(pow(y[i] - y1[i], 2), accuracy))
print("Сума квадратів відхилень S =", round(sum(e2), accuracy))

print('=' * 100)

y2 = []
x2 = []
count = 0
for i in range(-100, 0):
    if i != 0:
        x2.append(i / 10)
        y2.append(a/x2[count] + b)
        count += 1

plt.plot(x, y, 'ro')
plt.plot(x2, y2)
plt.title("Гіперболічна регресія")
plt.show()