import logging
import time
from .fetcher import fetch_page
from .parser import parse_books
from .storage import save_to_csv, check_duplicates
from .database import init_db, save_books, search_books
from pathlib import Path

from dotenv import load_dotenv

import os # для создания папки logs

load_dotenv()

BASE_URL = os.getenv('BASE_URL', 'https://books.toscrape.com')

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

    init_db()

    seen_titles = set()
    all_books = []

    urls = ["https://books.toscrape.com/index.html"]

    for page in range(2, 6):
        urls.append(f"https://books.toscrape.com/catalogue/page-{page}.html")

    for i, url in enumerate(urls, 1):
        logging.info(f"Обработка страницы {i}/{len(urls)}: {urls}")

        html = fetch_page(url)
        if not html:
            continue
            # logging.warning(f"Пропускаем страницу {i}")
            # continue

        books = parse_books(html)
        books = check_duplicates(books, seen_titles)

        all_books.extend(books)
        logging.info(f"Страница {i}: добавлено {len(books)} книг (всего: {len(all_books)})")

        time.sleep(1)
    
    if all_books:
        save_to_csv(all_books)
        saved, duplicates = save_books(all_books)
        logging.info(f"Готово! Книг собрано новых: {saved}, дубликатов: {duplicates}")
    else:
        logging.error("Не удалось собрать ни одной книги")

    cheap_books = search_books(max_price=20)
    logging.info(f"Книг дешевле 20: {len(cheap_books)}")
    for book in cheap_books[:5]:
        logging.info(f"- {book['title']}: {book['price']}")

    # logging.info(f"Готово!\nОбработано {len(books)} книг!")

    # if __name__ == '__main__':
    #     main()

main()

    

