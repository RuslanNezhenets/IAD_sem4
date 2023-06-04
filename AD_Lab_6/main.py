from scipy.spatial.distance import pdist
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from math import inf

def Q3(coords, U, k):
    Sum = 0
    distances = []
    for i in range(k):
        check = False
        temp = []
        for j in range(len(coords)):
            if U[j][0] == i + 1:
                temp.append(coords[j])
                if((len(temp)) == 2): check = True
        if check == True: distances = pdist(temp, metric="euclidean")
        else: distances = 0
        Sum += np.sum(distances)
    return Sum

#Подготовка данных

dataset = pd.read_excel('Data3.xlsx')

sb.set_theme(style="ticks")
sb.pairplot(dataset)
plt.savefig('DatasetVisualization.png')
plt.show()

data = dataset.iloc[:, 1:].values

def plot(data, centroids):
    plt.scatter(data[:, 0], data[:, 1], marker='.', color='gray', label='Точки данных')
    plt.scatter(centroids[:, 0], centroids[:, 1], color='red', label='Центроиды')

    plt.legend()
    plt.savefig('Centroids.png')
    plt.show()

# функция для вычисления евклидового расстояния
def distance(p1, p2):
    return np.sum((p1 - p2) ** 2)

# алгоритм инициализации
def Kmeans(data, k, e):
    Q_previous = inf
    m = 1
    #Крок 1
    #Инициализируем список центроидов и добавляем случайно выбранные точки данных в список
    centroids = []
    for i in range(k):
        centroids.append(data[np.random.randint(data.shape[0]), :])

    while(True):
        #Крок 2
        U = []
        for i in range(len(data)):
            point = data[i, :]
            dist = []

            #Вычислить расстояние "точки" от каждого выбранного центроида и сохранение минимального расстояния
            for j in range(len(centroids)):
                temp_dist = distance(point, centroids[j])
                dist.append(temp_dist)
            U.append([np.nanargmin(dist) + 1, round(min(dist), 5)])

        print(pd.DataFrame(U))

        # Крок 3
        Q = Q3(data, U, k)
        print("Q3 =", Q)
        print("Q3(прошлое) =", Q_previous)
        print("="*50)
        print()

        if(np.abs(Q - Q_previous) <= e):
            # Крок 6
            plot(data, np.array(centroids))
            print("Количество итераций:", m)
            return U, centroids
        else:
            # Крок 4
            centroids = []
            for i in range(k):
                cluster = []
                for j in range(len(data)):
                   if U[j][0] == i + 1:
                        cluster.append(data[j])

                center = []
                for j in range(len(cluster[0])):
                    Sum_coords = 0
                    for g in range(len(cluster)):
                        Sum_coords += cluster[g][j]
                    center.append(Sum_coords/len(cluster))
                centroids.append(center)

            # Крок 5
            Q_previous = Q
            m += 1


U, centroids = Kmeans(data, k=8, e=0.001)
clusters = []
for i in range(len(U)):
    clusters.append(U[i][0])

dataset.insert(1, "Clusters", 0)
dataset["Clusters"] = clusters
dataset = dataset.sort_values(['Clusters'], ascending=[True])

print("\nРозбиття даних по кластерам (номер кластеру та кількість даних в ньому):")
print(dataset.groupby(['Clusters'])['Clusters'].count())

dataset.to_excel("ResultDataset.xlsx")

centroids = pd.DataFrame(centroids)
temp = []
year = 2005
for i in range(len(data[0])):
    temp.append(year)
    year += 1
centroids.columns = temp

centroids['Clusters'] = ["C" + str(i) for i in range(1, len(centroids) + 1)]
dataset = pd.concat([dataset, centroids], ignore_index=True)

sb.pairplot(dataset, hue="Clusters", palette="Dark2",
            markers=[*["o" for i in range(len(centroids))], *["D" for i in range(len(centroids))]])
plt.savefig('Clusters.png')
plt.show()