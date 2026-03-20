import logging
import time
from .fetcher import fetch_page
from .parser import parse_books
from .storage import save_to_csv, check_duplicates
from pathlib import Path

import os # для создания папки logs


# os.makedirs('logs', exist_ok=True) # Создание папки Logs
# os.makedirs('data', exist_ok=True) # Создание папки Data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logs/parser.log',
    filemode='a',
    force = True # новое (3.2)
    )

logger = logging.getLogger(__name__)

def main():
    # Отладка: покажи текущую директорию (при исп. pathlib)
    print(f"Текущая директория: {Path.cwd()}")
    print(f"Папка data существует: {(Path.cwd() / 'data').exists()}")

    seen_titles = set()
    all_books = []

    url = ["https://books.toscrape.com/index.html"]

    for page in range(2, 6):
        url.append(f"https://books.toscrape.com/catalogue/page-{page}.html")

    for i, url in enumerate(url, 1):
        logging.info(f"Обработка страницы {i}/{len(url)}: {url}")

        html = fetch_page(url)
        if not html:
            logging.warning(f"Пропускаем страницу {i}")
            continue

        books = parse_books(html)
        books = check_duplicates(books, seen_titles)

        all_books.extend(books)
        logging.info(f"Страница {i}: добавлено {len(books)} книг (всего: {len(all_books)})")

        time.sleep(1)
    
    if all_books:
        save_to_csv(all_books)
        logging.info(f"Готово! Всего собрано: {len(all_books)} книг")
    else:
        logging.error("Не удалось собрать ни одной книги")

    # logging.info(f"Готово!\nОбработано {len(books)} книг!")

    # if __name__ == '__main__':
    #     main()

main()

    

