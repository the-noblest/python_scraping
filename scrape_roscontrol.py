from os import path

from bs4 import BeautifulSoup
import pandas as pd
import requests as r


SITE = 'https://roscontrol.com'
SORT = '?sort_val=desc&sort=rating'

goods_items = list()

response = r.get('https://roscontrol.com/category/produkti/')
soup = BeautifulSoup(response.text, 'html.parser').find('section', {'class': "main-container"})

results = soup.find_all('a', {'class': "catalog__category-item util-hover-shadow"})
categories = [res.find('div', {'class': "catalog__category-name"}).string for res in results]
sites = [res.get('href') for res in results]
items = list(zip(categories, sites))

for category in items:
    response = r.get(SITE + category[1] + SORT)
    soup = BeautifulSoup(response.text, 'html.parser').find('section', {'class': "main-container"})

    results = soup.find_all('a', {'class': "catalog__category-item util-hover-shadow"})
    sub_categories = [res.find('div', {'class': "catalog__category-name"}).string for res in results]
    sub_sites = [res.get('href') for res in results]
    sub_items = list(zip(sub_categories, sub_sites))

    safety_list = list()
    quality_list = list()

    for sub_category in sub_items:
        response = r.get(SITE + sub_category[1] + SORT)
        soup = BeautifulSoup(response.text, 'html.parser').find('section', {'class': "main-container"})

        names_list = soup.find_all('div', {'class': "product__item-link"})
        names_list = [name.string for name in names_list]

        rate_list = soup.find_all('div', {'class': "product-rating util-table-cell js-has_vivid_rows"})
        rates_list = soup.find_all('div', {'class': "rating-block"})

        for num in range(len(names_list)):
            try:
                rate_list[num] = rate_list[num].div.string.replace(' ', '')
            except AttributeError:
                rate_list[num] = '0'

            try:
                safety_list.append(rates_list[num].find_all('div', {'class': "right"})[0].string)
                quality_list.append(rates_list[num].find_all('div', {'class': "right"})[3].string)
            except IndexError:
                safety_list.append('0')
                quality_list.append('0')

            goods_items.append([
                names_list[num],
                category[0],
                sub_category[0],
                safety_list[num],
                quality_list[num],
                rate_list[num],
                'roscontrol.com'
            ])

df = pd.DataFrame(
    goods_items, columns=['Название', 'Категория', 'Подкатегория', 'Безопасность', 'Качество', 'Рейтинг', 'Источник']
)
df.to_csv(path.join('data', 'roscontrol.csv'), sep=';', index=False)
