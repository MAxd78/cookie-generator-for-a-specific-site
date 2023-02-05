import requests
from lxml import etree
from selenium import webdriver

url_list = ["https://www.cloudflare.com/ru-ru/",
            "https://dstat.cc/index.php?id=Hetzner-4",
            "https://dnevnik.mos.ru/diary/diary/homeworks"]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
for url in url_list:
    session = requests.session()
    driver = webdriver.Chrome()
    driver.get(url)
    all_cookies = driver.get_cookies()

    for s_cookie in all_cookies:
        session.cookies.set(s_cookie['name'], s_cookie['value'])

    r = session.get(url, headers=headers)
    root = etree.fromstring(r.text, etree.HTMLParser())
    title = root.xpath('//title/text()')[0] if len(root.xpath('//title/text()')) > 0 else 'Default Title'
    response_code = r.status_code

    with open('cookies.txt', 'w') as f:
        for cookie in all_cookies:
            f.write(str(cookie)+'\n')

    driver.close()

    if response_code == 200 and title is not None:
        print('\nPage loaded successfully.')
        print('Response: {0}\nPage title: {1}'.format(response_code, title))
    else:
        print('\nSomething went wrong while loading the page.')
        print('Response: {0}\nPage title: {1}'.format(response_code, title))