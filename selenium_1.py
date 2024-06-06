
from selenium_1 import webdriver
import selenium_1
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json

browser = webdriver.Chrome()
browser.delete_all_cookies()
browser.get('https://www.imdb.com/chart/top/')

elem = browser.find_element(By.CSS_SELECTOR,'#__NEXT_DATA__')
jsontext = json.loads(elem.get_attribute('innerHTML'))
jsontext = jsontext['props']['pageProps']['pageData']['chartTitles']['edges']
ids = list(map(lambda x: 'https://www.imdb.com/title/'+x+'?ref=chttp_t_1',[jsontext[item]['node']['id'] for item in range(len(jsontext))]))
print(ids)
print(len(ids))