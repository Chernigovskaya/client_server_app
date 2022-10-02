# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор». Далее забыть о том,
# что мы сами только что создали этот файл и исходить из того, что перед нами файл в неизвестной кодировке.
# Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.

from chardet import detect


f = open('test_file.txt', 'w', encoding='utf-8')
f.write('сетевое программирование, \nсокет, \nдекоратор')
f.close()

# узнать кодировку
with open('test_file.txt', 'rb') as file_encod:
    content = file_encod.read()
encoding = detect(content)['encoding']
print('encoding: ', encoding)


with open('test_file.txt', 'r', encoding=encoding) as file_open:
    print(file_open.read())
