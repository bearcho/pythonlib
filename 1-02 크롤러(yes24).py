import bs4
import urllib.request
import time
import datetime


def get_product_info(box):
    ptag = box.findAll('a')
    return ptag[0].text

def get_product_goods_info(info):
    names = info.find('div',{'class':'goods_name'})
    name = names.findAll('a')[0].text
    link = names.findAll('a')[0]['href']
    link = 'http://www.yes24.com/' + link
    price = info.find('em',{'class':'yes_b'}).text

    return {'name' : name, 'link' : link, 'price' : price}

def get_page(url):
    html = urllib.request.urlopen(url)

    bs_obj = bs4.BeautifulSoup(html, "html.parser")

    ul = bs_obj.find('ul', {'class': 'clearfix'})
    #boxes = ul.findAll('div', {'class': 'goods_name'})
    infos = ul.findAll('div', {'class': 'goods_info'})
    prod_info = [get_product_goods_info(info) for info in infos]

    return prod_info



baseurl = "http://www.yes24.com/24/Category/Display/001001046014?PageNumber="
pagenum = 1


while True:
    try:
        url = baseurl + str(pagenum)
        pagenum += 1
        page_products = get_page(url)
        print(url)
        for product in page_products:
            print(product['name'],product['price'],product['link'])
    except :
        print("끝")
        break


