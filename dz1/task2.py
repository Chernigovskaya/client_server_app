# 2. Каждое из слов «class», «function», «method» записать в байтовом типе.
# Сделать это необходимо в автоматическом, а не ручном режиме, с помощью добавления литеры b
# к текстовому значению, (т.е. ни в коем случае не используя методы encode, decode или функцию bytes)
# и определить тип, содержимое и длину соответствующих переменных.


word_1 = 'class'
word_2 = 'function'
word_3 = 'method'


def find_type_len(word):
    res = eval(f'b"{word}"')
    print(f'word "{word}" in byte = {res}, type = {type(res)}, len in byte = {len(res)}')


find_type_len(word_1)
find_type_len(word_2)
find_type_len(word_3)

