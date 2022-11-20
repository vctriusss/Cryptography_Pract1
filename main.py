from substitution_cipher import substitution_encode, substitution_decode, substitution_freq_analysis
from affinean_cipher import affinean_encode, affinean_decode, affinean_freq_analysis, affinean_recurrent_freq


def main():
    mode = int(input('Выберите режим работы\n1) Шифр простой замены\n2) Афинный шифр\n3) Афинный рекуррентный шифр\n'))
    option = int(input('1) Зашифрование \n2) Расшифрование \n3) Криптоанализ\n'))
    f = open('input.txt', 'r')
    text = f.read()
    new_text = ''

    if mode == 1:
        if option == 1:
            new_text = substitution_encode(text)
        elif option == 2:
            key = input('Введите ключ: ')
            new_text = substitution_decode(text, key)
        elif option == 3:
            key = substitution_freq_analysis(text)
            print(f'Предположительный ключ: {key}')

    elif mode == 2:
        if option == 1:
            new_text = affinean_encode(text)
        elif option == 2:
            print('Введите ключ:')
            a = input('a: ')
            b = input('b: ')
            new_text = affinean_decode(text, (a, b))
        else:
            key = affinean_freq_analysis(text)
            print(f'Предположительный ключ: a = {key[0]}, b = {key[1]}')

    elif mode == 3:
        if option == 1:
            new_text = affinean_encode(text, recurrent=True)
        elif option == 2:
            print('Введите ключ:')
            a, b = input('a: '), input('b: ')
            print('Введите ключ 2:')
            a2, b2 = input('a2: '), input('b2: ')
            new_text = affinean_decode(text, (a, b), (a2, b2), recurrent=True)
        else:
            new_text = affinean_recurrent_freq(text)

    with open('output.txt', 'w') as out:
        out.write(new_text)
    f.close()


if __name__ == '__main__':
    main()
