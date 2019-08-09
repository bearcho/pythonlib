import bs4
import urllib.request


url = "https://www.naver.com/"
html = urllib.request.urlopen(url)

bs_obj = bs4.BeautifulSoup(html, "html.parser")

top_right = bs_obj.find('div', {'class':'area_links'})
find_a = top_right.find('a')
print(find_a.text)