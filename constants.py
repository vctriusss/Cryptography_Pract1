from string import ascii_letters
import numpy as np
from typing import Dict, Tuple, List
from collections import Counter

ALPHABET = ascii_letters[26:] + ' '
POLY_F = [1, 2, 0, 1]  # коэффиценты неприводимого многочлена
Key = Tuple[str, str]

# стандартные частоты встречаемости символов в алфавите
ALPHABET_FREQUENCIES = {' ': 0.1870232, 'E': 0.1045473, 'T': 0.0764007, 'A': 0.0663082, 'O': 0.0624635, 'I': 0.0578739,
                        'N': 0.0573886, 'S': 0.0537923, 'H': 0.050431, 'R': 0.0503084, 'D': 0.0335061, 'L': 0.0331454,
                        'C': 0.0229697, 'U': 0.002254, 'M': 0.0204494, 'W': 0.0200068, 'F': 0.0171872, 'G': 0.016388,
                        'Y': 0.0151698, 'P': 0.0143949, 'B': 0.0126916, 'V': 0.0080253, 'K': 0.0056544, 'X': 0.0014204,
                        'J': 0.0009829, 'Q': 0.0008433, 'Z': 0.0005169}


def filter_text(text: str) -> str:  # фильтрует текст и приводит к верхнему регистру
    new_text = []
    for char in text:
        char = char.upper()
        if char not in ALPHABET:
            continue
        new_text.append(char)

    return ''.join(new_text)


# функция ниже генерирует словарь F_DICT вида (буква : коэффиценты многочлена из поля Галуа, соответствющему этой букве)
# также генерирует обратный словарь F_DICT_REV вида (коэффиценты : буква)
def generate_field_dict(p: int, m: int) -> Tuple[Dict[str, Tuple[int, ...]], Dict[Tuple[int, ...], str]]:
    field_dict, field_dict_rev = dict(), dict()
    for j in range(p ** m):
        tmp = [j // (p ** i) % p for i in range(m - 1, -1, -1)]
        field_dict[ALPHABET[j]] = tuple(tmp)
        field_dict_rev[tuple(tmp)] = ALPHABET[j]
    return field_dict, field_dict_rev


def beautify(np_arr: np.array) -> List[int]:  # приводит Numpy-массив к обычному читаемому виду
    np_arr = list(map(lambda y: int(y % 3), np_arr))
    np_arr = [0] * (3 - len(np_arr)) + np_arr
    return np_arr


# функция ниже вычисляет обратный элемент к элементу поля Галуа с заданными коэффицентами
def calculate_inversed(arr: List[int]) -> Tuple[int, ...]:
    prev, curr = arr.copy(), arr.copy()
    while curr != [0, 0, 1]:
        prev = curr.copy()
        curr = np.polymul(curr, arr)
        curr = np.polydiv(curr, POLY_F)[1]
        curr = beautify(curr)
    return tuple(prev)


F_DICT, F_DICT_REV = generate_field_dict(3, 3)
F_DICT_STAR = F_DICT.copy()  # словарь аналогичный F_DICT, но ключи принадлежат мультипликативной группе поля Галуа
del F_DICT_STAR['A']

# сгенерированный словарь, который ставит в соответствие каждому
# элементу мультипликативной группы поля Галуа обратный ему элемент
F_REVERSED = {p: calculate_inversed(list(p)) for p in F_DICT_STAR.values()}


def calculate_xi(text: str) -> float:  # вычисляет коэффицент принадлежности текста естественному языку (max=0.079)
    xi = 0
    curr_freqs = Counter(text)
    for letter in curr_freqs:
        xi += ALPHABET_FREQUENCIES[letter] * curr_freqs[letter]
    xi /= len(text)
    return xi
