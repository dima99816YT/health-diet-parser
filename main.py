import requests
from bs4 import BeautifulSoup
import csv
import json

r = requests.get('https://health-diet.ru/table_calorie/')
soup = BeautifulSoup(r.text, 'lxml')
all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')
all_categories = {}

for item in all_products_hrefs:
    item_name = item.text
    item_href = 'https://health-diet.ru' + item.get('href')
    all_categories[item_name] = item_href


with open('all_categories.json', 'r', encoding='utf-8') as f:
    all_categories = json.load(f)

for category_name, category_href in all_categories.items():
    r = requests.get(category_href)
    soup = BeautifulSoup(r.text, 'lxml')
    if soup.find(class_='uk-alert-danger'):
        continue
    tb_head = soup.find(
        class_='uk-overflow-container').find('tr').find_all('th')
    with open(f'{category_name}.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(
            [tb_head_name.text for tb_head_name in tb_head]
        )
        product_data = soup.find(
            class_='uk-overflow-container').find('tbody').find_all('tr')
        for item in product_data:
            writer.writerow(
                [product_field.text for product_field in item.find_all('td')]
            )
