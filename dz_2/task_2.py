# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными


import json

"""Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра."""


def write_order_to_json(item, quantity, price, buyer, date):
    """Запись в json"""

    with open('orders.json', 'r', encoding='utf-8') as f_out:
        data = json.load(f_out)

    with open('orders.json', 'w', encoding='utf-8', ) as f_in:
        orders_list = data['orders']
        order_info = {'item': item, 'quantity': quantity,
                      'price': price, 'buyer': buyer, 'date': date}
        orders_list.append(order_info)
        json.dump(data, f_in, indent=4, ensure_ascii=False)


# initialisation (чтобы не удалять данные при каждой новой проверке скрипта)
with open('orders.json', 'w', encoding='utf-8') as f_in:
    json.dump({'orders': []}, f_in, indent=4)


write_order_to_json('помада', 2, 500.00, 'Иванова И.Т', '03.10.2022')
write_order_to_json('помада', 2, 500.00, 'Petrova И.Т', '03.10.2022')


'''    data = {'order': [item, quantity, price, buyer, date]}
    with open('orders.json', 'w', encoding='utf-8') as write_json:

        json.dump(data, write_json,  indent=4,
                  ensure_ascii=False)
        

    with open('orders.json', 'w', encoding='utf-8') as open_json:
        json.dump({'orders': []}, open_json, indent=4)


write_order_to_json('помада', 2, 500.00, 'Иванова И.Т', '03.10.2022')
write_order_to_json('помада', 2, 500.00, 'Petrova И.Т', '03.10.2022') '''


