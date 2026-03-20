from bs4 import BeautifulSoup

def parse_books(html):
    """
    Извлекает список книг из HTML.
    Возвращает список словарей.
    """
    soup = BeautifulSoup(html, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    result = []
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text.replace('£', '').strip()
        rating = _extract_rating(book)

        result.append({
            'title': title,
            'price': price,
            'rating': rating, 
        })

    return result


def _extract_rating(book):
    # """
    # Вспомогательная функция для извлечения рейтинга.
    # """
    # classes = book.find('p', class_='star-rating')['class']
    # return classes[0] if len(classes) > 1 else 'Unknown'

    """Извлечение названия книг с защитой от ошибок"""

    rating_tag = book.find('p', class_='star-rating')

    if not rating_tag:
        return 'No rating'
    
    classes = rating_tag.get('class', [])

    if len(classes) >= 2:
        return classes[1]
    
    return 'Unknown'



