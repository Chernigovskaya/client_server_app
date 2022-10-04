# 3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
# Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число, третьему — вложенный словарь,
# где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
# Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с помощью
# параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;

import yaml

first_key = ['1€', '2ü', '€ã33']
second_key = 5
third_key = {'1Ò': 10, '2§': 20}

data = {'first_key': first_key, 'second_key': second_key, 'third_key': third_key}

with open('file.yaml', 'w', encoding='utf-8') as file_write:
    yaml.dump(data, file_write, allow_unicode=True, default_flow_style=False, sort_keys=False)
    #yaml.dump(data, file_write, allow_unicode=False, default_flow_style=False, sort_keys=False)


with open('file.yaml', 'r', encoding='utf-8') as file_read:
    content = yaml.load(file_read, Loader=yaml.FullLoader)
    print(content)
