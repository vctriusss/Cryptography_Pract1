from string import ascii_letters
import numpy as np
from typing import Dict, Tuple, List
from collections import Counter

ALPHABET = ascii_letters[26:] + ' '
POLY_F = [1, 2, 0, 1]
Key = Tuple[str, str]

ALPHABET_FREQUENCIES = {' ': 0.1870232, 'E': 0.1045473, 'T': 0.0764007, 'A': 0.0663082, 'O': 0.0624635, 'N': 0.0578739,
                        'I': 0.0573886, 'S': 0.0537923, 'R': 0.050431, 'H': 0.0503084, 'L': 0.0335061, 'D': 0.0331454,
                        'U': 0.0229697, 'C': 0.002254, 'M': 0.0204494, 'F': 0.0200068, 'W': 0.0171872, 'G': 0.016388,
                        'P': 0.0151698, 'Y': 0.0143949, 'B': 0.0126916, 'V': 0.0080253, 'K': 0.0056544, 'X': 0.0014204,
                        'J': 0.0009829, 'Q': 0.0008433, 'Z': 0.0005169}


def filter_text(text: str) -> str:
    new_text = []
    for char in text:
        char = char.upper()
        if char not in ALPHABET:
            continue
        new_text.append(char)

    return ''.join(new_text)


def generate_field_dict(p: int, m: int) -> Tuple[Dict[str, Tuple[int, ...]], Dict[Tuple[int, ...], str]]:
    field_dict, field_dict_rev = dict(), dict()
    for j in range(p ** m):
        tmp = [j // (p ** i) % p for i in range(m - 1, -1, -1)]
        field_dict[ALPHABET[j]] = tuple(tmp)
        field_dict_rev[tuple(tmp)] = ALPHABET[j]
    return field_dict, field_dict_rev


def beautify(np_arr: np.array) -> List[int]:
    np_arr = list(map(lambda y: int(y % 3), np_arr))
    np_arr = [0] * (3 - len(np_arr)) + np_arr
    return np_arr


def calculate_inversed(arr: List[int]) -> Tuple[int, ...]:
    prev, curr = arr.copy(), arr.copy()
    while curr != [0, 0, 1]:
        prev = curr.copy()
        curr = np.polymul(curr, arr)
        curr = np.polydiv(curr, POLY_F)[1]
        curr = beautify(curr)
    return tuple(prev)


F_DICT, F_DICT_REV = generate_field_dict(3, 3)
F_DICT_STAR = F_DICT.copy()
del F_DICT_STAR['A']

F_REVERSED = {p: calculate_inversed(list(p)) for p in F_DICT_STAR.values()}
letter_to_coeffs = lambda letter: list(F_DICT[letter])


def calculate_xi(text: str) -> float:
    xi = 0
    curr_freqs = Counter(text)
    for letter in curr_freqs:
        if letter not in curr_freqs.keys():
            continue
        xi += ALPHABET_FREQUENCIES[letter] * curr_freqs[letter]
    xi /= len(text)
    return xi
