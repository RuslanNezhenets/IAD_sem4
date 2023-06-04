import numpy as np
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, train_test_split
from sklearn import tree, metrics
from sklearn.datasets import load_breast_cancer
#Для создание png для детального просмотра больших деревьев
from sklearn.tree import export_graphviz
from six import StringIO
from IPython.display import Image
import pydotplus

#Поиск альфы
def SearchForAlpha(trains, tests, alphas):
    indexOfBest = 0
    for i in range(len(ccp_alphas)):
        if trains[i] >= tests[i]:
            if tests[i] > tests[indexOfBest]:
                indexOfBest = i
            elif tests[i] == tests[indexOfBest]:
                if trains[i] > trains[indexOfBest]:
                    indexOfBest = i
                elif trains[i] == trains[indexOfBest]:
                    if ccp_alphas[i] > ccp_alphas[indexOfBest]:
                        indexOfBest = i
        else:
            if trains[i] > tests[indexOfBest]:
                indexOfBest = i
            elif trains[i] == trains[indexOfBest]:
                if tests[i] > tests[indexOfBest]:
                    indexOfBest = i
                elif tests[i] == tests[indexOfBest]:
                    if ccp_alphas[i] > ccp_alphas[indexOfBest]:
                        indexOfBest = i

    print("Количество узлов:", len(train_scores))
    print("Номер подходящего узла:", indexOfBest + 1)
    print("train:", trains[indexOfBest])
    print("test:", tests[indexOfBest])
    print("alpha:", alphas[indexOfBest])

    return alphas[indexOfBest]

#Создание png для просмотра дерева
def PNG(data_model, string):

    dot_data = StringIO()
    export_graphviz(data_model, out_file=dot_data,
                    filled=True, rounded=True,
                    special_characters=True,
                    feature_names=dataset.feature_names)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(string)
    Image(graph.create_png())

#Импорт таблицы
dataset = load_breast_cancer()

X = dataset.data
y = dataset.target

#Разбиение на тренировочные и тестовые данные
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
data_model = DecisionTreeClassifier()

data_model.fit(X_train, y_train)

#Точность построеного дерева
y_pred = data_model.predict(X_test)
print("Точность начального дерева:")
print(metrics.accuracy_score(y_test, y_pred))
print("="*50)

#Вывод дерева решений
tree.plot_tree(data_model, filled=True)
plt.show()

#Поиск альф
path = data_model.cost_complexity_pruning_path(X, y)
ccp_alphas = path.ccp_alphas
ccp_alphas = ccp_alphas[:-1]

#Строим деревья для каждой альфы
trees = []
for ccp_alpha in ccp_alphas:
    derevo = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
    derevo.fit(X_train, y_train)
    trees.append(derevo)

#Ищем точности на тренировочных и тестовых данных
train_scores = [derevo.score(X_train, y_train) for derevo in trees]
test_scores = [derevo.score(X_test, y_test) for derevo in trees]

#Поиск лучшей альфы для оптимизации дерева
bestAlpha = SearchForAlpha(train_scores, test_scores, ccp_alphas)

#Вывод графика отношение точности и альфы
fig, ax = plt.subplots()
ax.set_xlabel("альфа")
ax.set_ylabel("точность")
ax.set_title("Точность по сравнению с альфой для обучающих и тестовых наборов")
ax.plot(ccp_alphas, train_scores, marker="o", label="train", drawstyle="steps-post")
ax.plot(ccp_alphas, test_scores, marker="o", label="test", drawstyle="steps-post")
ax.legend()
plt.show()

PNG(data_model, 'Tree.png')

#Создание оптимизированного дерева
data_model = DecisionTreeClassifier(random_state=0, ccp_alpha=bestAlpha)
data_model.fit(X_train, y_train)

#Вывод оптимизированного дерева
tree.plot_tree(data_model, filled=True, feature_names=dataset.feature_names)
plt.show()

PNG(data_model, 'Tree2.png')

#Вывод точности оптимизированного дерева
print("="*50)
y_pred = data_model.predict(X_test)
print("Точность итогового дерева:")
print(metrics.accuracy_score(y_test, y_pred))