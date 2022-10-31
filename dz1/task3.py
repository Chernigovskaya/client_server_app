# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать
# в байтовом типе. Важно: решение должно быть универсальным, т.е. не зависеть от того,
# какие конкретно слова мы исследуем.


word1 = 'attribute'
word2 = 'класс'
word3 = 'функция'
word4 = 'type'


def byte_type_true(word):
    if word.isascii():
        print(f'Слово "{word}" можно записать в байтовом виде')
    else:
        print(f'Слово "{word}" невозможно записать в байтовом виде')


byte_type_true(word1)
byte_type_true(word2)
byte_type_true(word3)
byte_type_true(word4)
