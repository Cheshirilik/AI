# Оценка подобия

from math import sqrt
from itertools import combinations

# Name: {film, rank, ...}
critics=\
{'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5, 'You, Me and Dupree':1.0, 'Superman Returns':4.0}}


# Подобие способом евклидова расстояния
def get_distance(obj, name1, name2):

    temp = {}
    for i in obj[name1]:
        if i in obj[name2]:
            temp[i] = 1

    if temp == {}:
        return 0

    summa = 0
    for i in temp:
        summa += pow(obj[name1][i] - obj[name2][i], 2)

    return 1/(1 + sqrt(summa))


# Подобие для всех пар в словаре (евклид)
def get_all(obj):
    temp = combinations(obj.keys(), 2)

    res = []
    for j in temp:
        res.append([j[0], j[1], get_distance(obj, j[0], j[1])])

    return res


res = sorted(get_all(critics), key=lambda x: x[2])                      # сортируем по третьему столбцу (подобию)
for k in res:
    print("Pair: {0} - {1}, distance is {2}:".format(k[0], k[1], k[2])) # печатаем все пары

l = len(res) - 1                                                        # находим наиболее и наименее похожие пары
print("\n\nLess similar pair: {0} - {1}, distance is {2}: \
      \nMore similar pair: {3} - {4}, distance is {5}: \
      ".format(res[0][0], res[0][1], res[0][2], res[l][0], res[l][1], res[l][2]))

