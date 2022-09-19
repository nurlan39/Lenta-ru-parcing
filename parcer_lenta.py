
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


links = []
for i in range(1, 4):
    url = f'https://lenta.ru/parts/news/{i}/'
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    news = soup.find_all('a', class_='card-full-news _parts-news')

    for k in news:
        link = k.get('href')
        if 'https:' in link:
            links.append(link)
        else:
            links.append('https://lenta.ru'+ link)

print(len(links))

titles, full_texts, dates = [],[],[]
for link in tqdm(links):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    if 'moslenta' in link:
        title = soup.find('h1', class_='jsx-3143472280 title')
        date = soup.find('div', class_='_1Lg_CbTX _240YeLMx')
        full_text = ''
        text_news = soup.find_all('p', class_='jsx-1117196867')
        for j in text_news:
            full_text += j.text
    elif 'motor' in link:
        title = soup.find('h1', class_='jsx-1897426106 title')
        date = soup.find('div', class_='_1Lg_CbTX _240YeLMx')
        full_text = ''
        text_news = soup.find_all('p', class_='jsx-3332198469')
        for j in text_news:
            full_text += j.text
    else:
        title = soup.find('span', class_='topic-body__title')
        date = soup.find('time', class_='topic-header__item topic-header__time')
        full_text = ''
        text_news = soup.find_all('p', class_='topic-body__content-text')
        for j in text_news:
            full_text += j.text

    titles.append(title.text)
    full_texts.append(full_text)
    dates.append(date.text)

d = {'titles': titles, 'full_texts': full_texts, 'dates':dates}
df = pd.DataFrame(d)
df.to_excel('data.xlsx', index=False)

