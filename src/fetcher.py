import requests
from requests.exceptions import RequestException
import logging

logger = logging.getLogger(__name__)

def fetch_page(url, timeout=10):
    """
    Docstring для fetch_page
    
    :param url: Описание
    :param timeout: Описание
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        logger.info(f"Успешная загрузка: {url}")
        return response.text
    except RequestException as e:
        logger.error(f"Ошибка загрузки {url}: {e}")
        return None
    