import csv
from pathlib import Path

filepath = Path('data/books.csv')

if filepath.exists(): # вывод первых трех строк
    with open(filepath, 'r', encoding = 'utf-8-sig') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i < 3: 
                print(row)
else:
    print("Файл еще не создан")

    