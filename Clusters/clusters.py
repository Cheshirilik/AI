# Кластеризация

from math import sqrt
from PIL import Image, ImageDraw
import random


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
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
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


# Печатаем кластеры
def print_cluster(clust, labels=None, n=0):
    for i in range(n):
        print(' ', end='')

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


# Вычисляем высоту сластеров для корректного отображения на графике
def get_height(clust):
    if (clust.left is None) and (clust.right is None):
        return 1

    return get_height(clust.left) + get_height(clust.right)


# Вычисляем глубину сластера
def get_depth(clust):
    if (clust.left is None) and (clust.right is None):
        return 0

    return max(get_depth(clust.left), get_depth(clust.right)) + clust.distance


# Рисуем узел
def draw_node(draw, clust, x, y, scal, labels):
    if clust.id < 0:
        h1 = get_height(clust.left) * 20
        h2 = get_height(clust.right) * 20

        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2

        l = clust.distance * scal

        draw.line((x, top + h1/2, x, bottom - h2/2), fill=(255, 0, 0))
        draw.line((x, top + h1/2, x + l, top + h1/2), fill=(255, 0, 0))
        draw.line((x, bottom - h2/2, x + l, bottom - h2/2), fill=(255, 0, 0))

        draw_node(draw, clust.left, x + l, top + h1/2, scal, labels)
        draw_node(draw, clust.right, x + l, bottom - h2/2, scal, labels)
    else:
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))


# Сохраняем кластер в *.jpg
def draw_diag(clust, labels, jpg="cluster.jpg"):
    h = get_height(clust) * 20
    d = get_depth(clust)
    w = 2000

    scal = float(w - 150) / d

    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h/2, 10, h/2), fill=(255, 0, 0))
    draw_node(draw, clust, 10, (h/2), scal, labels)
    img.save(jpg, "JPEG")


# Меняем местами столбцы и строки
def rotate(clust):
    new = []
    for i in range(len(clust)):
        new_r = [clust[j][i] for j in range(len(data))]
        new.append(new_r)

    return new


# Метод К-средних
def k_cluster(rows, dist=pearson, n=4):

    # Ищем минимум и максимум для каждого столбца (для генерации случайных центроидов)
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows])) for i in range(len(rows[0]))]

    # Генерируем случайные центроиды (n штук)
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                 for i in range(len(rows[0]))] for j in range(n)]

    last_matches = None
    for k in range(100):
        print("Итерация {0}".format(k))
        best_matches = [[] for i in range(n)]

        for j in range(len(rows)):
            row = rows[j]
            best = 0
            for i in range(n):
                d = dist(clusters[i], row)
                if d < dist(clusters[best], row):
                    best = i

            best_matches[best].append(j)

        if best_matches == last_matches:
            break

        last_matches = best_matches

        for i in range(n):
            avgs = [0.0] * len(rows[0])
            if len(best_matches[i]) > 0:
                for rowid in best_matches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(best_matches[i])
                clusters[i] = avgs

    return best_matches

# ================== MAIN ==================
rows, cols, data = read_words('blogdata.txt')
# res = build_clusters(data)
# # print_cluster(res, labels=rows)
# draw_diag(res, rows)
#
# new = rotate(data)
# res = build_clusters(data)
# draw_diag(res, cols, "rotate.jpg")

res = k_cluster(data, n=10)
#print(res)

s = [[rows[i] for i in res[j]] for j in range(len(res))]
print(s)