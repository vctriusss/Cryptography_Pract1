from constants import *
from random import choice


def recurrent_key(key1: Key, key2: Key) -> Key:
    a, b = F_DICT[key1[0]], F_DICT[key1[1]]
    a2, b2 = F_DICT[key2[0]], F_DICT[key2[1]]
    a = np.polymul(a, a2)
    a = np.polydiv(a, POLY_F)[1]
    a = beautify(a)
    b = np.polyadd(b, b2)
    b = np.polydiv(b, POLY_F)[1]
    b = beautify(b)
    return F_DICT_REV[tuple(a)], F_DICT_REV[tuple(b)]


def generate_key() -> Key:
    a, b = choice(list(F_DICT_STAR.keys())), choice(list(F_DICT.keys()))
    return a, b


def affinean_encode(text: str, key=None, key2=None, recurrent=False) -> str:
    # if key is None and key2 is None:
    #     key = generate_key()
    #     key2 = generate_key()
    #     print(f'Ключ: a = "{key[0]}", b = "{key[1]}"')
    #     print(f'Ключ 2: a2 = "{key2[0]}", b2 = "{key2[1]}"')
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
        x = letter_to_coeffs(text[i])
        x = np.polymul(letter_to_coeffs(curr_key[0]), x)
        x = np.polyadd(x, letter_to_coeffs(curr_key[1]))
        x = np.polydiv(x, POLY_F)[1]
        x = tuple(beautify(x))
        encoded_text += F_DICT_REV[x]

    return encoded_text


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
        x = letter_to_coeffs(text[i])
        x = np.polysub(x, letter_to_coeffs(curr_key[1]))
        x = np.polymul(x, F_REVERSED[F_DICT[curr_key[0]]])
        x = np.polydiv(x, POLY_F)[1]
        x = tuple(beautify(x))
        decoded_text += F_DICT_REV[x]
    return decoded_text


def affinean_bruteforce(text: str) -> Key:
    supp_key = ('B', 'A')
    xi_max = 0
    for a in F_DICT_STAR.keys():
        for b in F_DICT.keys():
            curr_key = (a, b)
            decoded = affinean_decode(text, curr_key)
            xi = calculate_xi(decoded)
            print(xi)
            if xi > xi_max:
                xi_max = xi
                supp_key = curr_key
    return supp_key


# def affinean_recurrent_freq(text: str) -> str:
#     key1, key2 = generate_key(), generate_key()
#     xi = 0
#     while xi < 0.07:
#         text = affinean_encode(text, key1, key2, recurrent=True)
#         xi = calculate_xi(text)
#     return text
