SIGNS = (
    ("Водолей", 20),
    ("Риби", 19),
    ("Овен", 21),
    ("Телец", 21),
    ("Близнаци", 21),
    ("Рак", 21),
    ("Лъв", 22),
    ("Дева", 23),
    ("Везни", 23),
    ("Скорпион", 23),
    ("Стрелец", 22),
    ("Козирог", 22)
)


def what_is_my_sign(day, month):
    sign_index = month - 1
    if day >= SIGNS[sign_index][1]:
        return SIGNS[sign_index][0]
    else:
        return SIGNS[sign_index - 1][0]
