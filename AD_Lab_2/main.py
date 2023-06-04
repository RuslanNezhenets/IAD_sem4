import matplotlib.pyplot as plt
import numpy as np

rounding = 5    #Округлення виводу до n-ого знаку

def f(x, y):
    return 20 + (x**2 - 10 * np.cos(2 * np.pi * x)) + (y**2 - 10 * np.cos(2 * np.pi * x))

x1 = -4
x2 = 4
y1 = -4
y2 = 4

#Створюємо массиви x та y з вказаними межами
x = np.linspace(x1, x2, 81)
y = np.linspace(y1, y2, 81)

#Створюємо графік
fig = plt.figure()
ax = plt.axes(projection='3d')

X, Y = np.meshgrid(x, y)
Z = f(X, Y)

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()

#====================== Простий стохастичний пошук ======================

N = 300        #кількість випадкових точок

# Реалізація рівномірно розподіленої випадкової величини
e = np.random.uniform(0, 1, N)

xk = []
yk = []
for i in range(N):
    xk.append(x1 + (x2 - x1)*e[i])
    yk.append(y1 + (y2 - y1)*e[i])

minX = minY = minZ = 10000

for i in range(N):
    for j in range(N):
        if f(xk[i], yk[j]) < minZ:
            minZ = f(xk[i], yk[j])
            minX = xk[i]
            minY = yk[j]

print("Простий стохастичний пошук")
print("[", round(minX, rounding), ",", round(minY, rounding), "] min Z =", round(minZ, rounding))

#====================== Метод імітації відпалу ======================

T0 = 0.001
T = 50
v = 0.99
M = 2

#Початкові наближення
X = [x1, y1]
Xnext = X.copy()

while True:
    z = np.random.normal(0, 1, M)   #Реалізація нормальної стандартизованої випадкової величини

    for i in range(M):
        Xnext[i] = X[i] + z[i] * T  #Генерація нових наближень

    if x1 < Xnext[0] < x2 and y1 < Xnext[1] < y2:       #Перевірка виконання граничних умов
        deltaE = f(Xnext[0], Xnext[1]) - f(X[0], X[1])  #Крок 4
        if deltaE < 0:
            X = Xnext.copy()                            #X = X'
        else:
            P = np.exp(-deltaE/T)                       #Імовірність переходу в нову точку

            E = np.random.uniform(0, 1, 1)              #Реалізація рівномірно розподіленої випадкової величини
            if E < P:                                   #Крок 5
                X = Xnext.copy()                        #X = X'
            else:
                T = v * T

        if T < T0:                                      #Крок 6
            break                                       #Завершити пошук


print("Метод імітації відпалу")
print("[", round(X[0], rounding), ",", round(X[1], rounding), "] min Z =", round(f(X[0], X[1]), rounding))