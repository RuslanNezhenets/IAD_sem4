import math
from prettytable import PrettyTable
import matplotlib.pyplot as plt

accuracy = 5

#ln(y) = ln(a) + b ln(x)

x = [-4.38, -3.84, -3.23, -2.76, -2.22, -1.67, -1.13, -0.6]
y = [2.25, 2.83, 3.44, 4.51, 5.29, 6.55, 8.01, 10.04]

for i in range(len(x)):
    x[i] = math.fabs(x[i])

for i in range(len(x)):
    if x[i] < 0:
        x[i] = 1

lnx = []
lny = []
lnx2 = []
lny2 = []
lnxy = []

n = len(x)

for i in range(n):
    lnx.append(round(math.log(x[i]), accuracy))
    lny.append(round(math.log(y[i]), accuracy))
    lnx2.append(round(math.log(x[i])*math.log(x[i]), accuracy))
    lny2.append(round(math.log(y[i])*math.log(y[i]), accuracy))
    lnxy.append(round(math.log(x[i])*math.log(y[i]), accuracy))

table = PrettyTable()
table.add_column("ln(x)", lnx)
table.add_column("ln(y)", lny)
table.add_column("ln(x)^2", lnx2)
table.add_column("ln(y)^2", lny2)
table.add_column("ln(x)*ln(y)", lnxy)

print(table)

Mx = round(1/n * sum(lnx), accuracy)
print("Mx = ", Mx)

My = round(1/n * sum(lny), accuracy)
print("My = ", My)

Mx2 = round(1/n * sum(lnx2), accuracy)
print("Mx2 = ", Mx2)

Mxy = round(1/n * sum(lnxy), accuracy)
print("Mxy = ", Mxy)

print('=' * 30)

a = (Mxy - Mx * My)/(Mx2-Mx*Mx)
a = round(a, accuracy)
print("a = ", a)

b = (Mx2 * My - Mx * Mxy)/(Mx2-Mx*Mx)
b = round(b, accuracy)
print("b = ", b)

e = round(2.7182818284, accuracy)

print("Степеневе рівняння регресії: y =", round(pow(e, b), accuracy),  "* x^(", a, ")")

y1 = []

for i in range(n):
    y1.append(pow(x[i], a) * pow(e, b))
e2 = []
for i in range(n):
    e2.append(round(pow(y[i] - y1[i], 2), accuracy))
print("Сума квадратів відхилень S =", round(sum(e2), accuracy))

print('=' * 100)

y2 = []
x2 = []
count = 0
for i in range(100):
    if i != 0:
        x2.append(i / 10)
        y2.append(pow(x2[count], a) * pow(e, b))
        count += 1

plt.plot(x, y, 'ro')
plt.plot(x2, y2)
plt.title("Степенева регресія")
plt.show()