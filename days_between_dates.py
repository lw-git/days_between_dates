from datetime import date


def end_of_word(word, n):
    w = {'год': ['год', 'года', 'лет'],
         'месяц': ['месяц', 'месяца', 'месяцев'],
         'день': ['день', 'дня', 'дней']}

    if n == 0:
        return
    elif str(n).endswith(('11', '12', '13', '14')):
        return str(n) + ' ' + w[word][2]
    elif str(n)[-1] == '1':
        return str(n) + ' ' + w[word][0]
    elif str(n)[-1] in ('2', '3', '4'):
        return str(n) + ' ' + w[word][1]
    else:
        return str(n) + ' ' + w[word][2]


def is_intercalary(year):
    if year % 4 == 0 or (year % 100 == 0 and year % 400 == 0):
        return True
    else:
        return False


def compare_date(d1, d2, extraday=0):
    delta = (d2 - d1).days
    # если первая дата больше второй - меняем их местами
    if delta < 0:
        delta = (d1 - d2).days
        d1, d2 = d2, d1
    # если даты совпадают - то выводим сообщение
    elif delta == 0:
        return 'Даты совпадают'

    result = ''
    years = 0
    months = 0
    days = 0

    if d2.year != d1.year:
        if d2.month > d1.month:
            years = d2.year - d1.year
        elif d2.month == d1.month:
            if d2.day >= d1.day:
                years = d2.year - d1.year
            else:
                years = d2.year - d1.year - 1
        else:
            years = d2.year - d1.year - 1
    else:
        years = 0

    # по умолчанию для невысокосного года 29 февраля = 28 февраля
    # если extaraday = 1, то для невысокосного года 29 февраля = 1 марта
    if d1.day == 29 and d1.month == 2:
        d1 = date(d1.year + years, d1.month, d1.day - 1)
        if is_intercalary(d2.year):
            days = (d2 - d1).days - 1
        else:
            days = (d2 - d1).days - extraday
    else:
        d1 = date(d1.year + years, d1.month, d1.day)
        days = (d2 - d1).days

    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_intercalary(d2.year) or is_intercalary(d1.year):
        month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if d2.year != d1.year:
        for i in reversed(range(d2.month)):
            if days - month_days[i - 1] >= 0:
                days -= month_days[i - 1]
                months += 1

        if d2.month <= d1.month:
            for j in reversed(range(d1.month - 1, 12)):
                if days - month_days[j - 1] >= 0:
                    days -= month_days[j - 1]
                    months += 1
    else:
        for i in reversed(range(d1.month, d2.month)):
            if days - month_days[i - 1] >= 0:
                days -= month_days[i - 1]
                months += 1

    if months == 12:
        months = 0
        years += 1

    for s in [('год', years), ('месяц', months), ('день', days)]:
        s = end_of_word(*s)
        if s is not None:
            result += s + ', '

    return result[:-2]


# 29 февраля = 28 февраля
d1 = date(2016, 2, 29)
d2 = date(2019, 2, 28)
print(compare_date(d1, d2))

# 29 февраля = 1 марта
d1 = date(2016, 2, 29)
d2 = date(2019, 3, 1)
print(compare_date(d1, d2, extraday=1))
