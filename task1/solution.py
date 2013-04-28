def what_is_my_sign(day, month):
    signs = ["Овен", "Телец", "Близнаци", "Рак", "Лъв", "Дева", "Везни",
             "Скорпион", "Стрелец", "Козирог", "Водолей", "Риби"]

    start_days = [21, 21, 21, 21, 22, 23, 23, 23, 22, 22, 20, 19]

    month_offset = 3
    sign_index = month - month_offset

    if day < start_days[sign_index]:
        return signs[sign_index - 1]
    else:
        return signs[sign_index]
