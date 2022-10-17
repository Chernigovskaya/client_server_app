# 5. Написать код, который выполняет пинг веб-ресурсов yandex.ru, youtube.com и преобразовывает
# результат из байтовового типа данных в строковый без ошибок для любой кодировки операционной системы.


import subprocess
import platform
import locale

urls = ['yandex.ru', 'youtube.com']
param = '-n' if platform.system().lower() == 'windows' else '-c'

for url in urls:
    args = ['ping', param, '2', url]
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in process.stdout:
        result = locale.getpreferredencoding(line)
        # print('result = ', result)
        line = line.decode(result).encode('utf-8')
        print(line.decode('utf-8'))



