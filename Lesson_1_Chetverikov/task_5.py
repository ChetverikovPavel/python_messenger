"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""
import chardet
import subprocess


def ping_site(args):
    ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in ping.stdout:
        result = chardet.detect(line)
        print(result)
        line = line.decode(result['encoding'])
        print(line)


ya_args = ['ping', 'yandex.ru']
youtube_args = ['ping', 'youtube.com']

ping_site(ya_args)
print()
ping_site(youtube_args)
