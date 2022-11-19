from constants import *
from random import shuffle


F_DICT, F_DICT_REV = generate_field_dict(3, 3)
F_DICT_STAR = F_DICT.copy()
del F_DICT_STAR['A']


def generate_keys() -> Dict[str, str]:
    key = list(F_DICT.keys())
    shuffle(key)
    key = dict(zip(list(F_DICT.keys()), key))
    return key


def substitution_encode(text: str) -> str:
    text = filter_text(text)
    key = generate_keys()
    print('Ключ:', ''.join(key.values()))
    encoded_text = ''
    for char_i in text:
        encoded_text += key[char_i]
    return encoded_text


def substitution_decode(text: str, key: str) -> str:
    decoded_text = ''
    key = dict(zip(list(key), list(F_DICT.keys())))
    for char_i in text:
        decoded_text += key[char_i]
    return decoded_text
