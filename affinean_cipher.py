from constants import *
from random import choice
from collections import Counter


def recurrent_key(key1: Key, key2: Key) -> Key:  # Генерирует ключ k_i рекуррентно с помощью k_i-1, k_i-2
    a, b = F_DICT[key1[0]], F_DICT[key1[1]]
    a2, b2 = F_DICT[key2[0]], F_DICT[key2[1]]
    a = np.polymul(a, a2)
    a = np.polydiv(a, POLY_F)[1]
    a = beautify(a)  # a_i = a_i-1 * a_i-2 (mod f)
    b = np.polyadd(b, b2)
    b = np.polydiv(b, POLY_F)[1]
    b = beautify(b)  # b_i = b_i-1 + b_i-2 (mod f)
    return F_DICT_REV[tuple(a)], F_DICT_REV[tuple(b)]


def generate_key() -> Key:  # генерирует случайный ключ, взяв a из мултипликативной группы, b из поля Галуа
    a, b = choice(list(F_DICT_STAR.keys())), choice(list(F_DICT.keys()))
    return a, b


def affinean_encode(text: str, key=None, key2=None, recurrent=False) -> str:
    """
    Функция шифрует текст аффинным/аффинным рекуррентным шифром.
    :param text: открытый текст
    :param key: ключ 1 (не обязательный)
    :param key2: ключ 2 (не обязательный)
    :param recurrent: флаг, который показывает каким типом аффинного шифра происходит шифрование
    :return: шифртекст
    """
    if key is None and key2 is None:
        key = generate_key()
        key2 = generate_key()
        print(f'Ключ: a = "{key[0]}", b = "{key[1]}"')
        if recurrent:
            print(f'Ключ 2: a2 = "{key2[0]}", b2 = "{key2[1]}"')
    keys = [key]

    if recurrent:
        keys.append(key2)
        keys.append(key)

    text = filter_text(text)
    encoded_text = ''
    for i in range(len(text)):
        if recurrent and i:
            keys.pop(0)
            keys.append(key2 if i == 1 else recurrent_key(keys[0], keys[1]))
        curr_key = keys[-1]
        x = F_DICT[text[i]]
        x = np.polymul(F_DICT[curr_key[0]], x)
        x = np.polyadd(x, F_DICT[curr_key[1]])
        x = np.polydiv(x, POLY_F)[1]
        x = tuple(beautify(x))
        encoded_text += F_DICT_REV[x]  # y = a * x + b (mod f)

    return encoded_text


# Функция расшифрования, параметры аналогично прошлой функции
def affinean_decode(text: str, key: Key, key2: Key = ('', ''), recurrent=False) -> str:
    keys = [key]
    if recurrent:
        keys.append(key2)
        keys.append(key)

    decoded_text = ''
    for i in range(len(text)):
        if recurrent and i:
            keys.pop(0)
            keys.append(key2 if i == 1 else recurrent_key(keys[0], keys[1]))
        curr_key = keys[-1]
        y = F_DICT[text[i]]
        y = np.polysub(y, F_DICT[curr_key[1]])
        y = np.polymul(y, F_REVERSED[F_DICT[curr_key[0]]])
        y = np.polydiv(y, POLY_F)[1]
        y = tuple(beautify(y))
        decoded_text += F_DICT_REV[y]  # x = (y - b) * a^-1 (mod f)
    return decoded_text


def affinean_freq_analysis(text: str) -> Key:
    cnt = Counter(text)
    cnt = cnt.most_common(2)
    y1, y2 = cnt[0][0], cnt[1][0]
    x1, x2 = ' ', 'E'
    dy = np.polysub(F_DICT[y2], F_DICT[y1])
    dx = np.polysub(F_DICT[x2], F_DICT[x1])
    dx = np.polydiv(dx, POLY_F)[1]
    for a in F_DICT_STAR.values():
        mul = np.polymul(dx, a)
        mul = np.polydiv(mul, POLY_F)[1]
        if beautify(mul) == beautify(dy):
            ax = np.polymul(a, F_DICT[x1])
            a = F_DICT_REV[a]
            b = np.polysub(F_DICT[y1], ax)
            b = np.polydiv(b, POLY_F)[1]
            b = F_DICT_REV[tuple(beautify(b))]
            return a, b


def affinean_recurrent_freq(text: str) -> str:
    key1, key2 = generate_key(), generate_key()
    xi = 0
    while xi < 0.07:
        text = affinean_encode(text, key1, key2, recurrent=True)
        xi = calculate_xi(text)
    return text
