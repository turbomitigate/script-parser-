import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL для новостей
url = 'https://news.mail.ru/politics/'

# Регулярные выражения для поиска всех падежей фамилий
zelen_pattern = re.compile(r'\bЗеленск[а-яё]*\b', re.IGNORECASE)
putin_pattern = re.compile(r'\bПутин[а-яё]*\b', re.IGNORECASE)

# Множество для хранения обработанных ссылок
processed_links = set()

def get_full_article_text(article_url):
    try:
        article_page = requests.get(article_url)
        article_page.raise_for_status()

        article_soup = BeautifulSoup(article_page.text, 'html.parser')
        paragraphs = article_soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])

        return article_text
    except requests.RequestException as e:
        print(f"Не удалось получить страницу статьи: {e}")
        return ''

def grab_news():
    try:
        page = requests.get(url)
        page.raise_for_status()

        soup = BeautifulSoup(page.text, "html.parser")

        # Нахожу все новости
        all_news = soup.find_all('div', class_='newsitem')

        for news in all_news:
            # Нахожу ссылку
            link_tag = news.find('a', class_='newsitem__title link-holder')
            if not link_tag:
                continue

            link = urljoin(url, link_tag['href'])

            # Проверяю, была ли новость уже обработана
            if link in processed_links:
                continue  # Пропускаю обработанную новость

            # Нахожу заголовок
            title_tag = news.find('span', class_='newsitem__title-inner')
            title = title_tag.text if title_tag else 'Заголовок отсутствует'

            # Ищу аннотацию
            annotation_tag = news.find('span', class_='newsitem__text')
            annotation = annotation_tag.text if annotation_tag else 'Аннотация отсутствует'

            # Получаю полный текст статьи
            article_text = get_full_article_text(link)

            # Проверяю наличие ключевых слов "Зеленский" и "Путин" в разных падежах
            if (zelen_pattern.search(title) or zelen_pattern.search(annotation) or
                putin_pattern.search(title) or putin_pattern.search(annotation) or
                zelen_pattern.search(article_text) or putin_pattern.search(article_text)):
                # Вывод деталей новости, если ключевые слова найдены
                print("\033[91mСсылка:\033[0m", link, "\033[91mЗаголовок:\033[0m", title, "\033[91mАннотация:\033[0m", annotation)

                # Добавляю ссылку в множество обработанных ссылок
                processed_links.add(link)
    except requests.RequestException as e:
        print(f"Не удалось получить страницу: {e}")

while True:
    grab_news()
    time.sleep(50)