# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными


import json

"""Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра."""


def write_order_to_json(item, quantity, price, buyer, date):
    data = {'order': [item, quantity, price, buyer, date]}
    with open('orders.json', 'w', encoding='utf-8') as write_json:
        json.dump(data, write_json,  indent=4,
                  ensure_ascii=False)
        write_json.seek(2)

    with open('orders.json') as open_json:
        print(open_json.read())


write_order_to_json('помада', 2, 500.00, 'Иванова И.Т', '03.10.2022')

