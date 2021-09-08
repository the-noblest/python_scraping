from os import path

from bs4 import BeautifulSoup
import pandas as pd
import requests as r


SITE = 'https://rskrf.ru'

response = r.get('https://rskrf.ru/ratings/produkty-pitaniya/')
soup = BeautifulSoup(response.text, 'html.parser').find('div', id="page-content")

results = soup.find_all(class_="category-item")
categories = [res.find(class_="h5").string for res in results]
sites = [res.a.get('href') for res in results]
items = list(zip(categories, sites))

for category in items:
    goods_items = list()

    response = r.get(SITE + category[1])
    soup = BeautifulSoup(response.text, 'html.parser').find('div', id="page-content")

    results = soup.find_all(class_="category-item")
    sub_categories = [res.find(class_="d-xl-block d-none").string for res in results]
    sub_sites = [res.a.get('href') for res in results]
    sub_items = list(zip(sub_categories, sub_sites))

    for sub_category in sub_items:
        response = r.get(SITE + sub_category[1])
        soup = BeautifulSoup(response.text, 'html.parser').find('div', id="page-content")

        results = [res.get('href') for res in soup.find_all('a')]
        good_sites = list(filter(lambda x: x is not None and x.startswith('/goods/') and x != '/goods/', results))

        for good_site in good_sites:
            response = r.get(SITE + good_site)
            soup = BeautifulSoup(response.text, 'html.parser').find('div', id="page-content")

            name = soup.find('p').string.replace('\n', '').replace('  ', '')
            rate = soup.find('div', {'class': "starrating readonly d-inline-flex flex-row-reverse"}).span.string
            results = soup.find_all('div', {'class': "rating-item"})

            try:
                safety = \
                 [res.find('div', {'class': "starrating readonly d-inline-flex flex-row-reverse float-right"}).span.string
                  for res in results if res.span.string == 'Безопасность'][0]
            except IndexError:
                safety = '-'

            try:
                quality = \
                 [res.find('div', {'class': "starrating readonly d-inline-flex flex-row-reverse float-right"}).span.string
                  for res in results if res.span.string == 'Качество'][0]
            except IndexError:
                quality = '-'

            goods_items.append([name, category[0], sub_category[0], safety, quality, rate, 'rskrf.ru'])

    df = pd.DataFrame(
        goods_items, columns=['Название', 'Категория', 'Подкатегория', 'Безопасность', 'Качество', 'Рейтинг', 'Источник']
    )
    df.to_csv(path.join('data', f'rskrf_{category[0]}.csv'), sep=';', index=False)
