from prettytable import PrettyTable
import matplotlib.pyplot as plt

accuracy = 4

x = [-4.38, -3.84, -3.23, -2.76, -2.22, -1.67, -1.13, -0.6]
y = [2.25, 2.83, 3.44, 4.51, 5.29, 6.55, 8.01, 10.04]

x2 = []
xy = []

n = len(x)

for i in range(n):
    x2.append(round(x[i]*x[i], accuracy))
    xy.append(round(x[i]*y[i], accuracy))

table = PrettyTable()
table.add_column("x", x)
table.add_column("y", y)
table.add_column("x^2", x2)
table.add_column("xy", xy)

print(table)

Mx = round(1/n * sum(x), accuracy)
print("Mx = ", Mx)

My = round(1/n * sum(y), accuracy)
print("My = ", My)

Mx2 = round(1/n * sum(x2), accuracy)
print("Mx2 = ", Mx2)

Mxy = round(1/n * sum(xy), accuracy)
print("Mxy = ", Mxy)

print('=' * 30)
a = (Mxy - Mx * My)/(Mx2-Mx*Mx)
a = round(a, accuracy)
print("a = ", a)

b = (Mx2 * My - Mx * Mxy)/(Mx2-Mx*Mx)
b = round(b, accuracy)
print("b = ", b)

print("Лінійне рівняння регресії: y =", a, "* x +", b)

y1 = []
for i in range(n):
    y1.append(a*x[i] + b)

e2 = []
for i in range(n):
    e2.append(round(pow(y[i] - y1[i], 2), accuracy))
print("Сума квадратів відхилень S =", round(sum(e2), accuracy))

print('=' * 100)


plt.plot(x, y, 'ro')
plt.plot(x, y1)
plt.title("Лінійна регресія")
plt.show()