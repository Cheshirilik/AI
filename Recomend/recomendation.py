# Оценка подобия

from math import sqrt
from itertools import combinations

# Name: {film, rank, ...}
critics = \
{'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree':1.0, 'Superman Returns': 4.0}}

films = \
{'Lady in the Water': {'Lisa Rose': 2.5, 'Gene Seymour': 3.0, 'Michael Phillips': 2.5, 'Mick LaSalle': 3.0, 'Jack Matthews': 3.0},
 'Snakes on a Plane': {'Lisa Rose': 3.5, 'Gene Seymour': 3.5, 'Michael Phillips': 3.0, 'Claudia Puig': 3.5, 'Mick LaSalle': 4.0, 'Jack Matthews': 4.0, 'Toby': 4.5},
 'Just My Luck': {'Lisa Rose': 3.0, 'Gene Seymour': 1.5, 'Claudia Puig': 3.0, 'Mick LaSalle': 2.0},
 'Superman Returns': {'Lisa Rose': 3.5, 'Gene Seymour': 5.0, 'Michael Phillips': 3.5, 'Claudia Puig': 4.0, 'Mick LaSalle': 3.0, 'Jack Matthews': 5.0, 'Toby': 4.0},
 'You, Me and Dupree': {'Lisa Rose': 2.5, 'Gene Seymour': 3.5, 'Claudia Puig': 2.5, 'Mick LaSalle': 2.0, 'Jack Matthews': 3.5, 'Toby': 1.0},
 'The Night Listener': {'Lisa Rose': 3.0, 'Gene Seymour': 3.0, 'Michael Phillips': 4.0, 'Claudia Puig': 4.5, 'Mick LaSalle': 3.0, 'Jack Matthews': 3.0}}

# Составляем список фильмов для пары имен
def get_pairs(obj, name1, name2):
    return [i for i in obj[name1] if i in obj[name2]]


# Подобие способом евклидова расстояния
def get_euc_distance(obj, name1, name2):
    mas = get_pairs(obj, name1, name2)

    if mas is []:
        return 0

    summa = sum([(obj[name1][i] - obj[name2][i])**2 for i in mas])

    # return 1 / (1 + summa)
    return 1/(1 + sqrt(summa))


# Подобие корреляцией Пирсона
def get_pears_distance(obj, name1, name2):
    mas = get_pairs(obj, name1, name2)

    n = len(mas)
    if n == 0: return 0

    sum1 = sum([obj[name1][i] for i in mas])
    sum2 = sum([obj[name2][i] for i in mas])

    sum1_sq = sum([obj[name1][i]**2 for i in mas])
    sum2_sq = sum([obj[name2][i]**2 for i in mas])

    p_sum = sum([obj[name1][i] * obj[name2][i] for i in mas])

    num = p_sum - sum1 * sum2 / n
    den = sqrt((sum1_sq - sum1**2/n) * (sum2_sq - sum2**2/n))

    if den == 0: return 0

    return num/den


# Подобие с использовнаием коэф Танимото
# https://jcheminf.springeropen.com/articles/10.1186/s13321-015-0069-3
def get_tan_distance(obj, name1, name2):
    mas = get_pairs(obj, name1, name2)

    n_a = sum([obj[name1][i]**2 for i in mas])              # S(a)**2
    n_b = sum([obj[name2][i]**2 for i in mas])              # S(b)**2
    n_c = sum([obj[name1][i] * obj[name2][i] for i in mas]) # S(a*b)

    return n_c/(n_a + n_b - n_c)


# Подобие для всех пар в словаре
def get_all(obj):
    temp = combinations(obj.keys(), 2)

    res = []
    res1 = []
    res2 = []
    for i in temp:
        pair = i[0] + '-' + i[1]
        res.append([pair, get_euc_distance(obj, i[0], i[1])])
        res1.append([pair, get_pears_distance(obj, i[0], i[1])])
        res2.append([pair, get_tan_distance(obj, i[0], i[1])])

    return res, res1, res2                # Евклид, Пирсон, Танимото


# Поиск наиболее близких к name
def get_top(obj, name, n=5, func=get_pears_distance):
    mas = [(func(obj, name, other), other) for other in obj if other != name]

    mas.sort()
    mas.reverse()
    return mas[0:n]


# Расчет оценок фильмов ещё не просмотренных человеком, на основе оценок критиков
# На основании подобия человека и критика рассчитывается оценка, которую поставит человек ещё не просмотренному фильму
def get_recommendations(obj, name, func=get_pears_distance):
    total = {}
    sim_sum = {}

    for i in obj:                                       # Перебираем имена в словаре
        if i == name:
            continue
        sim = func(obj, name, i)                       # Вычисляем подобие между заданным человеком и очередным критиком

        if sim <= 0:
            continue

        for j in obj[i]:                                # Перебираем фильмы

            if j not in obj[name] or obj[name][j] == 0:  # выбираем только те фильмы, которые человек ещё не смотрел
                total.setdefault(j, 0)
                total[j] += obj[i][j] * sim             # суммарная оценка * коэф. подобия

                sim_sum.setdefault(j, 0)
                sim_sum[j] += sim                       # сумма коэф. подобия

    rankings = [(n, s/sim_sum[n]) for n, s in total.items()]

    rankings.sort()
    rankings.reverse()

    return rankings


# Преобразуем словарь критиков в словарь фильмов
def transform_dict(obj):
    result = {}
    for name in obj:
        for i in obj[name]:
            result.setdefault(i, {})
            result[i][name] = obj[name][i]

    return result


#================== MAIN ==================
res_e, res_p, res_t = get_all(critics)
res_e = sorted(res_e, key=lambda x: x[1])                                   # сортируем по второму столбцу (подобию)
res_p = sorted(res_p, key=lambda x: x[1])
res_t = sorted(res_t, key=lambda x: x[1])

l = len(res_e)
p = ""
t = ""
for i in range(0, l):
    for j in range(0, l):
        if res_p[j][0] == res_e[i][0]:
            p = res_p[j][1]
            break

    for k in range(0, l):
        if res_t[k][0] == res_e[i][0]:
            t = res_t[k][1]
            break

    print("{0:<30} e = {1:<8.5f} p = {2:<8.5f} t = {3:<8.5f}".format(res_e[i][0], res_e[i][1], p, t))
    # печатаем все пары, где    {<8.5f}  = <8 - выравнивание по правой стороне до восьми символов
    #                                    = .5f - показать пять знаков после запятой

l -= 1                                                                       # находим наиболее и наименее похожие пары
print("\nEuclid:\nless similar pair: {0}, coef is {1}:\nMore similar pair: {2}, coef is {3}: \
      ".format(res_e[0][0], res_e[0][1], res_e[l][0], res_e[l][1]))

print("\nPearson:\nless similar pair: {0}, coef is {1}:\nMore similar pair: {2}, coef is {3}: \
      ".format(res_p[0][0], res_p[0][1], res_p[l][0], res_p[l][1]))

print("\nTanimoto:\nless similar pair: {0}, coef is {1}:\nMore similar pair: {2}, coef is {3}: \
      ".format(res_t[0][0], res_t[0][1], res_t[l][0], res_t[l][1]))

print("\nTop critics:")
print(get_top(critics, "Toby", n=3))

print("\nEuclid recommendations:")
print(get_recommendations(critics, 'Toby', func=get_euc_distance))
print("\nPearson recommendations:")
print(get_recommendations(critics, 'Toby'))
print("\nTanimoto recommendations:")
print(get_recommendations(critics, 'Toby', func=get_tan_distance))

#print("\n\nTransformation:")
#transform_dict(critics)

print("\nFilm (Superman Returns) recomendations:")
print("Euclid:\n", get_top(films, "Superman Returns", func=get_euc_distance))
print("Pearson:\n", get_top(films, "Superman Returns"))
print("Tanimoto:\n", get_top(films, "Superman Returns", func=get_tan_distance))
