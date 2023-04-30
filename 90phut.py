import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_football_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        source_code = response.text
        pattern = r'https://91ptv.tv/truc-tiep/[^"]+'
        football_links = re.findall(pattern, source_code)
        return football_links
    else:
        print('Không thể truy cập trang web')
        return []

def get_m3u8_links(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    requests = driver.requests
    m3u8_links = []
    for request in requests:
        if '.m3u8' in request.url:
            m3u8_links.append(request.url)
    driver.quit()
    return m3u8_links

football_links = get_football_links('https://91ptv.tv/')
for link in football_links:
    print(f'Link xem bóng đá: {link}')
    m3u8_links = get_m3u8_links(link)
    for m3u8_link in m3u8_links:
        print(f'  Link M3U8: {m3u8_link}')