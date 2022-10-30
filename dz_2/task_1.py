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


'''
def get_data():
    """Get data from txt-file"""

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []
    for i in range(1, 4):
        with open(f'info_{i}.txt', 'rb') as file_obj:
            data_bytes = file_obj.read()
            result = chardet.detect(data_bytes)
            data = data_bytes.decode(result['encoding'])

        # get a list of OS manufacturers
        os_prod_reg = re.compile(r'Изготовитель системы:\s*\S*')
        os_prod_list.append(os_prod_reg.findall(data)[0].split()[2])

        # get a list of OS names
        os_name_reg = re.compile(r'Windows\s\S*')
        os_name_list.append(os_name_reg.findall(data)[0])

        # get a list of products code
        os_code_reg = re.compile(r'Код продукта:\s*\S*')
        os_code_list.append(os_code_reg.findall(data)[0].split()[2])

        # get a list of systems type
        os_type_reg = re.compile(r'Тип системы:\s*\S*')
        os_type_list.append(os_type_reg.findall(data)[0].split()[2])

    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data.append(headers)

    data_for_rows = [os_prod_list, os_name_list, os_code_list, os_type_list]  # matrix 4 x 3

    # make matrix (4 x 3) from matrix (3 x 4)
    for idx in range(len(data_for_rows[0])):
        line = [row[idx] for row in data_for_rows]
        main_data.append(line)

    # variant 2
    # for idx in range(len(data_for_rows[0])):
    #     line = list(map(lambda row: row[idx], data_for_rows))
    #     main_data.append(line)

    # variant 3
    # for idx in range(len(data_for_rows[0])):
    #     main_data.append([os_prod_list[idx], os_name_list[idx], os_code_list[idx], os_type_list[idx])

    # variant 4 zip-transformation
    # list(zip([1, 2, 3],                [(1, 4),
    #          [4, 5, 6]))      ==>       (2, 5),
    #                                     (3, 6)]

    # variant 5 T-transformation in numpy
    # import numpy as np
    # main_data = np.array(main_data, dtype=str).T.tolist()
    # создаём массив numpy, трансформируем его (.T) и тут же снова превращаем в список (tolist)

    return main_data
'''


def write_to_csv(file_name):
    with open(file_name, 'w', encoding='utf-8') as file_write:
        write_csv = csv.writer(file_write, delimiter='|')
        data = get_data()
        for row in data:
            write_csv.writerow(row)


write_to_csv('result.csv')
