import sqlite3
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'data' / 'books.db'

def get_connect():
    """Возвращение подключение к базе данных"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Создание таблицы, если её нет"""
    conn = get_connect()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            price REAL NOT NULL,
            rating TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        )        
    ''')

    conn.commit()
    conn.close()
    logger.info(f"База данных инициализированна {DB_PATH}")

def save_books(books):
    """Сохраняет книги в базу
        Игнорирует дубликаты благодаря UNIQUE.
    """

    conn = get_connect()
    cursor = conn.cursor()

    for book in books:
        try:
            cursor.execute(''' 
                INSERT OR IGNORE INTO books (title, price, rating)
                VALUES (?, ?, ?)
            ''', (book['title'], book['price'], book['rating']))

            if cursor.rowcount > 0:
                saved_count += 1
            else:
                duplicate_count += 1

        except Exception as e:
            logger.error(f"Ошибка при сохранении {book['title']}: {e}")

    conn.commit()
    conn.close()

    logger.info(f"Сохранено: {saved_count}, дубликантов: {duplicate_count}")
    return saved_count, duplicate_count

def get_all_books():
    """Возвращение всех книг из базы"""
    conn = get_connect()
    cursor = conn.cursor()

    cursor.execute('SELECT title, price, rating FROM books')
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]

def search_books(max_price=None, min_rating=None):
    """Поиск книг с фильтрами
       Пример: найти все книги дешевле 20 с рейтингом 4 и выше"""
    conn = get_connect()
    cursor = conn.cursor()

    query = 'SELECT title, price, rating FROM books WHERE 1=1'
    params = []

    if max_price:
        query += 'AND price <= ?'
        params.append(max_price)

    if min_rating:
        query += 'AND rating = ?'
        params.append(min_rating)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]



