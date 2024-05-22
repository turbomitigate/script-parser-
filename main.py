from bs4 import BeautifulSoup
import requests
import re
import time

url = 'https://news.mail.ru/politics/'

# Регулярные выражения для поиска всех падежей фамилий
zelen_pattern = re.compile(r'\bЗеленск[а-яё]*\b', re.IGNORECASE)
putin_pattern = re.compile(r'\bПутин[а-яё]*\b', re.IGNORECASE)

# Множество для хранения обработанных ссылок
processed_links = set()


def grab_news():
    page = requests.get(url)

    # Проверяю  подключение
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")

        # Нахожу все новости
        allNews = soup.findAll('div', class_='newsitem')

        for news in allNews:
            # Нахожу ссылку
            link_tag = news.find('a', class_='newsitem__title link-holder')
            if link_tag:
                link = link_tag['href']
            else:
                continue  

            # Проверяю, была ли новость уже обработана
            if link in processed_links:
                continue  # Пропускаю обработанную новость

            # Нахожу заголовок
            title_tag = news.find('span', class_='newsitem__title-inner')
            if title_tag:
                title = title_tag.text
            else:
                title = 'Заголовок отсутствует'

            # Ищу аннотацию
            annotation_tag = news.find('span', class_='newsitem__text')
            if annotation_tag:
                annotation = annotation_tag.text
            else:
                annotation = 'Аннотация отсутствует'

            # Проверяю наличие ключевых слов "Зеленский" и "Путин" в разных падежах
            if (zelen_pattern.search(title) or zelen_pattern.search(annotation) or
                    putin_pattern.search(title) or putin_pattern.search(annotation)):
                # Вывод деталей новости, если ключевые слова найдены
                print("\033[91mСсылка:\033[0m", link, "\033[91mЗаголовок:\033[0m", title, "\033[91mАннотация:\033[0m",
                      annotation)

                # Добавляю ссылку в множество обработанных ссылок
                processed_links.add(link)
    else:
        print(f"Не удалось получить страницу. {page.status_code}")


while True:
    grab_news()
    time.sleep(50)