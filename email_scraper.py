from bs4 import BeautifulSoup
import requests
import urllib.parse
from collections import deque
import re

user_url = str(input('[+] URL DAI SUKA: '))
urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0

try:
    while len(urls):
        count += 1
        if count == 100:
            break
        url = urls.popleft()
        scraped_urls.add(url)
        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url
        print('[%d] EBASHIM HOHLA %s' % (count, url))
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяет наличие ошибок HTTP
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            continue
        
        new_emails = set(re.findall(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", response.text, re.I))
        emails.update(new_emails)
        soup = BeautifulSoup(response.text, 'html.parser')  # Используем html.parser
        
        for anchor in soup.find_all("a"):
            try:
                link = anchor.attrs['href']
            except KeyError:
                continue  # Пропускаем ссылки без href
            
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link

            if link not in urls and link not in scraped_urls:
                urls.append(link)
except KeyboardInterrupt:
    print('[-] ZOV ZAKROI!!!')

for mail in emails:
    print(mail)
