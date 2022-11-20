from constants import *
from random import shuffle


def generate_keys() -> Dict[str, str]:  # генерирует ключ как перестановку букв алфавита
    key = list(ALPHABET)
    shuffle(key)
    key = dict(zip(ALPHABET, key))
    return key


def substitution_encode(text: str) -> str:  # функция шифрования текста простым шифром замены
    text = filter_text(text)
    key = generate_keys()
    print('Ключ:', ''.join(key.values()))
    encoded_text = ''
    for char_i in text:
        encoded_text += key[char_i]
    return encoded_text


def substitution_decode(text: str, key: str) -> str:  # функция расшифрования текста простым шифром замены
    decoded_text = ''
    key = dict(zip(key, ALPHABET))
    for char_i in text:
        decoded_text += key[char_i]
    return decoded_text


def substitution_freq_analysis(text: str) -> str:  # функция для частотного анализа шифра простой подстановки
    cnt = Counter(text)
    supp_subst = [x[0] for x in cnt.most_common(27)]
    supp_subst = dict(zip(list(ALPHABET_FREQUENCIES.keys()), supp_subst))
    supp_key = ''
    for letter in ALPHABET:
        supp_key += supp_subst[letter]
    return supp_key
