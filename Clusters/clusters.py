# Кластеризация

from math import sqrt
from pprint import pprint


# Загрузка данных из файла
def read_words(name):
    strings = [i for i in open(name, "r")]

    cols = strings[0].strip().split('\t')[1:]           # Список слов (столбцы)
    rows = []                                           # Название блога
    data = []                                           # повторяемость слов из списка в блоге rows -> data
    for s in strings[1:]:
        r = s.strip().split('\t')
        rows.append(r[0])
        data.append([float(i) for i in r[1:]])

    return rows, cols, data


# Подобие корреляцией Пирсона
def pearson(name1, name2):

    sum1 = sum(name1)
    sum2 = sum(name2)

    sum1_sq = sum([i ** 2 for i in name1])
    sum2_sq = sum([i ** 2 for i in name2])

    n = len(name1)
    p_sum = sum([name1[i] * name2[i] for i in range(n)])

    num = p_sum - sum1 * sum2 / n
    den = sqrt((sum1_sq - sum1**2/n) * (sum2_sq - sum2**2/n))

    if den == 0:
        return 0

    return 1 - num/den      # Расстояние тем меньше, чем более схожи списки


# Кластер
class BiCluster:
    def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id


# Строим множество(дерево) кластеров
def build_clusters(table, dist=pearson):
    distances = {}                                          # список растояния для всех пар (x, y): d
    current = -1

    clust = [BiCluster(table[i], id=i) for i in range(len(table))]    # формируем класс из каждой строки таблицы

    while len(clust) > 1:

        lowest_pair = (0, 1)                                # расстояние между clust[0] и clust[1]
        closest = dist(clust[0].vec, clust[1].vec)          # принимаем за наименьшее расстояние

        l = len(clust)
        for i in range(l):
            for j in range(i+1, l):
                if(clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = dist(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:                             # если новая дистанция меньше
                    closest = d
                    lowest_pair = (i, j)

        merge = [(clust[lowest_pair[0]].vec[i] + clust[lowest_pair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]

        new = BiCluster(merge, left=clust[lowest_pair[0]], right=clust[lowest_pair[1]], distance=closest, id=current)

        current -= 1
        del clust[lowest_pair[1]]
        del clust[lowest_pair[0]]
        clust.append(new)

    return clust[0]


def print_cluster(clust, labels=None, n=0):
    for i in range(n):
        print(' ')
        if clust.id < 0:
            print('-')
        else:
            if labels is None:
                print(clust.id)
            else:
                print(labels[clust.id])

        if clust.left is not None:
            print_cluster(clust.left, labels=labels, n=n+1)
        if clust.right is not None:
            print_cluster(clust.right, labels=labels, n=n+1)

# ================== MAIN ==================

rows, cols, data = read_words('blogdata.txt')
res = build_clusters(data)
print_cluster(res, labels=rows)
