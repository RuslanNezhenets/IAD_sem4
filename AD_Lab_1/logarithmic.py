import math
from prettytable import PrettyTable
import matplotlib.pyplot as plt

accuracy = 5

#y = a * ln(x) + b

x = [-4.38, -3.84, -3.23, -2.76, -2.22, -1.67, -1.13, -0.6]
y = [2.25, 2.83, 3.44, 4.51, 5.29, 6.55, 8.01, 10.04]

#Логарифмічну регресію не можливо застосувати до від'ємних іксів, тому візьмемо їх по модулю
for i in range(len(x)):
    x[i] = math.fabs(x[i])

lnx = []
y2 = []
lnx2 = []
xy = []

n = len(x)

for i in range(n):
    y2.append(round(y[i] * y[i], accuracy))
    lnx.append(round(math.log(x[i]), accuracy))
    xy.append(round(lnx[i] * y[i], accuracy))
    lnx2.append(round(math.log(x[i]) * math.log(x[i]), accuracy))

table = PrettyTable()
table.add_column("ln(x)", lnx)
table.add_column("y", y)
table.add_column("ln(x)^2", lnx2)
table.add_column("y^2", y2)
table.add_column("ln(x)*y", xy)

print(table)

Mx = round(1/n * sum(lnx), accuracy)
print("Mx = ", Mx)

My = round(1/n * sum(y), accuracy)
print("My = ", My)

Mx2 = round(1/n * sum(lnx2), accuracy)
My2 = round(1/n * sum(y2), accuracy)

Mxy = round(1/n * sum(xy), accuracy)
print("Mxy = ", Mxy)

print('=' * 30)

a = (Mxy - Mx * My)/(Mx2-Mx*Mx)
a = round(a, accuracy)
print("a = ", a)

b = (Mx2 * My - Mx * Mxy)/(Mx2-Mx*Mx)
b = round(b, accuracy)
print("b = ", b)

e = round(2.7182818284, accuracy)

print("Логарифмічна рівняння регресії: y =", a, "* ln(x) +", b)

y1 = []

for i in range(n):
    y1.append(a*math.log(x[i]) + b)

e2 = []
for i in range(n):
    e2.append(round(pow(y[i] - y1[i], 2), accuracy))
print("Сума квадратів відхилень S =", round(sum(e2), accuracy))

print('=' * 100)

y2 = []
x2 = []
for i in range(150):
    if i != 0:
        x2.append(i / 10)
        y2.append(a * math.log(x2[i-1]) + b)

plt.plot(x, y, 'ro')
plt.plot(x2, y2)
plt.title("Логарифмічна регресія")
plt.show()