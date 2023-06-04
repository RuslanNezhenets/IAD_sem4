import numpy
from sklearn.cluster import *
from scipy.cluster.hierarchy import *
from scipy.spatial.distance import pdist
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from statistics import mean

def GeomForSelf(centers):
    distances = pdist(centers, metric="euclidean")
    return distances

def GeomForCenter(coords, center):
    Distances = []
    for i in range(len(coords)):
        vec = [center[k] - coords[i][k] for k in range(len(coords[i]))]
        Distances.append(round(numpy.sqrt(sum([j * j for j in vec])), 2))
    return Distances

def Dispersion(coords, center):
    if len(coords) < 2:
        return 0
    Distances = []
    for i in range(len(coords)):
        Distances.append(list(pdist([coords[i], center], metric="euclidean"))[0])
    sum = 0
    for i in range(len(Distances)):
        sum += Distances[i]**2
    return sum/len(Distances)

metrics = ['euclidean', 'mahalanobis', 'minkowski']
methods = ['single', 'complete', 'median']

#Подготовка данных

dataset = pd.read_excel('Data3.xlsx')

sb.set_theme(style="ticks")
sb.pairplot(dataset)
plt.savefig('DatasetVisualization.png')
plt.show()

data = dataset.iloc[:, 1:-1].values

print("Визначення кофенетичних коефіцієнтів")
temp = ["Метод зв'язування"]
for method in methods:
    temp.append(method)
print(temp)

maxCoeff = 0
BestMetric = BestConnection = ''
BestDistances = []

for metric in metrics:
    distances = pdist(data,metric)
    temp = [metric]
    for method in methods:
        Linkage = linkage(distances, metric=metric, method = method)
        Coeff, Matrix = cophenet(Linkage, distances)
        temp.append(Coeff)
        if Coeff > maxCoeff:
            maxCoeff = Coeff
            BestMetric = metric
            BestConnection = method
            BestDistances = distances

    print(temp)

#Построение дендрограммы
print("\nНайкращий метод зв'язування:", BestMetric, BestConnection)
Linkage = linkage(distances, metric=BestMetric, method = BestConnection)
dend = dendrogram(Linkage)
plt.title('Дендрограма')
plt.ylabel('Дистанція')
plt.savefig('Dendrogram.png')
plt.show()

distances = pdist(data, BestMetric)
clustersAmount = [[], []]
correctDist = 0
for i in range(round(min(distances)), round(max(distances)) + 1, 1):
    clusters = fcluster(Linkage, i, criterion="distance")
    clustersAmount[0].append(i)
    clustersAmount[1].append(max(clusters))

plt.plot(clustersAmount[0], clustersAmount[1])
plt.xlabel("Максимальная дистанция между точками кластера")
plt.ylabel("Количество кластеров")
plt.show()

clusters = fcluster(Linkage, 8, criterion="maxclust")

dataset.insert(1, "Clusters", 0)
dataset["Clusters"] = clusters

dataset = dataset.sort_values(['Clusters'], ascending=[True])

print("\nРозбиття даних по кластерам (номер кластеру та кількість даних в ньому:")
print(dataset.groupby(['Clusters'])['Clusters'].count())

print("\nТаблица с центрами кластеров")
Centers = pd.DataFrame()
for i in range(len(data[0]), -1, -1):
    column = dataset.columns[i + 2]
    Centers.insert(0, column, 0)
    Centers[column] = dataset.groupby(["Clusters"])[column].mean()

print(Centers.transpose())

Centers['Clusters'] = ["C" + str(i) for i in range(1, len(Centers) + 1)]

print("\nВідстані між центрами кластерів.")
tempCenter = Centers.drop(["Clusters"], axis = 1)
print(pd.DataFrame(GeomForSelf(tempCenter)))

listGeomForCenter = []
print("\nГеометричні відстані від елементів до центрів кластерів,")
for i in range(len(Centers)):
    tempCoords = dataset.drop(["Products"], axis=1)[dataset["Clusters"] == i + 1].drop(["Clusters"], axis=1)
    tempCenter = Centers[Centers["Clusters"] == "C" + str(i + 1)].drop(["Clusters"], axis = 1)
    listGeomForCenter.append(GeomForCenter(tempCoords.values.tolist(), tempCenter.values.tolist()[0]))
print(pd.DataFrame(listGeomForCenter).transpose())

listDispersion = []
print("\nВнутрішньокластерна дисперсія отриманих кластерів")
for i in range(len(Centers)):
    tempCoords = pd.DataFrame(dataset.drop(["Products"], axis=1)[dataset["Clusters"] == i + 1]).drop(["Clusters"], axis=1)
    tempCenter = pd.DataFrame(Centers[Centers["Clusters"] == "C" + str(i + 1)]).drop(["Clusters"], axis=1)
    listDispersion.append(Dispersion(tempCoords.values.tolist(), tempCenter.values.tolist()[0]))
for i in range(len(listDispersion)):
    print("Кластер", i + 1,":", listDispersion[i])

dataset.to_excel("ResultDataset.xlsx")

dataset = pd.concat([dataset, Centers], ignore_index=True)

sb.pairplot(dataset, hue="Clusters", palette="Dark2",
            markers=[*["o" for i in range(len(Centers))], *["D" for i in range(len(Centers))]])
plt.savefig('Clasters.png')
plt.show()
