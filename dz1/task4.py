#4. Преобразовать слова «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).


# words = ['разработка', 'администрирование', 'protocol', 'standard']
# for word in words:
#     words_bytes = word.encode('utf-8')
#     words_str = words_bytes.decode('utf-8')
#     print(f'{type(words_bytes)} = {words_bytes}')
#     print(f'{type(words_str)} = {words_str}')
#     print('*' * 30)


def str_in_byte_in_str(word):
    word_bytes = word.encode('utf-8')
    word_str = word_bytes.decode('utf-8')
    print(f'word "{word}" in byte = {word_bytes}, type = {type(word_bytes)}')
    print(f'word = {word_str}, type = {type(word_str)}')


word1 = 'разработка'
str_in_byte_in_str(word1)
word2 = 'администрирование'
str_in_byte_in_str(word2)




