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


# Составляем список фильмов для пары имен
def get_pairs(obj, name1, name2):
    res = []
    for i in obj[name1]:
        if i in obj[name2]:
            res.append(i)

    if res is []:
        return 0
    else:
        return res


# Подобие способом евклидова расстояния
def get_euc_distance(obj, name1, name2):
    mas = get_pairs(obj, name1, name2)

    if mas is []:
        return 0

    summa = 0
    for i in mas:
        summa += pow(obj[name1][i] - obj[name2][i], 2)

    #return 1 / (1 + summa)
    return 1/(1 + sqrt(summa))


# Подобие корреляцией Пирсона
def get_pirs_distance(obj, name1, name2):
    mas = get_pairs(obj, name1, name2)

    n = len(mas)
    if len == 0:
        return 0

    sum1 = sum([obj[name1][i] for i in mas])
    sum2 = sum([obj[name2][i] for i in mas])

    sum1_sq = sum([obj[name1][i]**2 for i in mas])
    sum2_sq = sum([obj[name2][i]**2 for i in mas])

    pSum = sum([(obj[name1][i] * obj[name2][i]) for i in mas])

    num = pSum - sum1 * sum2 / n
    den = sqrt((sum1_sq - sum1**2/n) * (sum2_sq - sum2**2/n))

    if den == 0:
        return 0

    return num/den


# Подобие для всех пар в словаре (евклид)
def get_all(obj):
    temp = combinations(obj.keys(), 2)

    res = []
    res1 = []
    for j in temp:
        res.append([j[0] + '-' + j[1], get_euc_distance(obj, j[0], j[1])])
        res1.append([j[0] + '-' + j[1], get_pirs_distance(obj, j[0], j[1])])

    return res, res1                # Евклид, Пирсон


res_e, res_p = get_all(critics)
res_e = sorted(res_e, key=lambda x: x[1])                      # сортируем по третьему столбцу (подобию)
res_p = sorted(res_p, key=lambda x: x[1])

for i in range(0, len(res_e)):
    #p = res_p.index(res_e[i][0])
    print("{0}, euclid = {1}:".format(res_e[i][0], res_e[i][1])) # печатаем все пары

for i in range(0, len(res_p)):
    print("{0}, pirson = {1}:".format(res_p[i][0], res_p[i][1]))  # печатаем все пары

l = len(res_e) - 1                                                        # находим наиболее и наименее похожие пары
print("\n\nLess similar euclid pair: {0}, distance is {1}: \
      \nMore similar uclid pair: {2}, distance is {3}: \
      ".format(res_e[0][0], res_e[0][1], res_e[l][0], res_e[l][1]))

print("\nLess similar pirson pair: {0}, distance is {1}: \
      \nMore similar pirson pair: {2}, distance is {3}: \
      ".format(res_p[0][0], res_p[0][1], res_p[l][0], res_p[l][1]))
