import csv
import logging
# import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Определяем путь относительно КОРНЯ проекта
# __file__ = путь к этому файлу (src/storage.py)
# .resolve() = полный абсолютный путь
# .parent.parent = поднимаемся на 2 уровня вверх (до корня)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'

def save_to_csv(books, filepath=None):
    """
    Сохраняет список книг
    """

    if filepath is None:
        # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # filepath = os.path.join(base_dir, 'data', 'books.csv')
        DATA_DIR.mkdir(exist_ok=True)
        filepath = DATA_DIR / 'books.csv'

    # os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'price', 'rating'])
        writer.writeheader()
        writer.writerows(books)

    logger.info(f"Сохранено {len(books)} книг в {filepath}")
    print(f'Файл сохранен: {filepath}')

def check_duplicates(books, seen_titles):
    """
    Фильтрует дупликаты по названию
    """
    unique_books = []
    for book in books:
        if book['title'] not in seen_titles:
            unique_books.append(book)
            seen_titles.add(book['title'])
    return unique_books


