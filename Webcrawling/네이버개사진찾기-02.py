from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup

keyword= 'dog'

url = "https://search.naver.com/search.naver?ssc=tab.image.all&where=image&sm=tab_jum&query=%EA%B0%9C"

result = urlopen(url)

result_html = result.read()
result_soup = BeautifulSoup(result_html, "html.parser")