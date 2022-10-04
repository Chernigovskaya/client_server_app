#1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt
# и формирующий новый «отчетный» файл в формате CSV.

from re import findall
import csv
from chardet import detect


list_file = ['info_1.txt', 'info_2.txt', 'info_3.txt']
templates = [
        r'Изготовитель системы:\s +(\w+)[\n]',
        r'Название ОС:\s+([a-zA-Z0-9А-Яа-я\s\.]{1,})[\n]',
        r'Код продукта:\s+([-0-9a-zA-Z]+)[\n]',
        r'Тип системы:\s+([-0-9a-zA-Z\s]+)[\n]',
                     ]


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for i in list_file:
        with open(i, 'rb') as file_encode:
            content = file_encode.read()
        encoding = detect(content)['encoding']
        with open(i, 'r', encoding=encoding) as file_open:
            content = file_open.read()

        os_prod_list.append(','.join(findall(templates[0], content)))
        os_name_list.append(','.join(findall(templates[1], content)))
        os_code_list.append(','.join(findall(templates[2], content)))
        os_type_list.append(','.join(findall(templates[3], content)))
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы'], [], [], []]
    for i in range(len(os_prod_list)):
        main_data[i + 1].append(os_prod_list[i])
        main_data[i + 1].append(os_name_list[i])
        main_data[i + 1].append(os_code_list[i])
        main_data[i + 1].append(os_type_list[i])
    return main_data


def write_to_csv(file_name):
    with open(file_name, 'w') as file_write:
        write_csv = csv.writer(file_write, delimiter='|')
        data = get_data()
        for row in data:
            write_csv.writerow(row)
        file_write.close()


write_to_csv('result.csv')
