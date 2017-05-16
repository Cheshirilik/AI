# Кластеризация

from math import sqrt


# Загрузка данных из файла
def read_words(name):
    strings = [i for i in open(name, "r")]

    cols = strings[0].strip().split('\t')[1:]           # Список слов (столбцы)
    rows = []                                           # Название блога
    data = []                                           # повторяемость слов из списка в блоге rows -> data
    for s in strings:
        r = s.strip().split('\t')
        rows.append(r[0])
        data.append([float(x) for x in r[1:]])

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

    if den == 0: return 0

    return 1 - num/den      # Расстояние тем меньше, чем более схожи списки

#================== MAIN ==================

st = read_words('blogdata.txt')
#print(st)

