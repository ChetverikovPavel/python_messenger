"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

text_list = ['разработка', 'администрирование', 'protocol', 'standard']
encode_list = []
decode_list = []

for el in text_list:
    encode_list.append(el.encode('utf-8'))

print(encode_list)
print()

for el in encode_list:
    decode_list.append(el.decode('utf-8'))

print(decode_list)
