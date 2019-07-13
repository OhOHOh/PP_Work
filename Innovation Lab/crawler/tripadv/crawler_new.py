from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError

import time
import config

def get_page_html_txt(url):
    '''
    获取 url page 的源代码
    '''
    try:
        html = urlopen(url)
        return html.read()
    except HTTPError as e:
        return None

def parse_home_page(html):
    '''
    解析 home page 的源代码
    return:
        items_list: 类型是 list, 每个元素都是一个dict, 包含3个key: 'name'(航空公司名字),'reviews'(其下有几条评论), 'link'(details 的链接)
    ''' 
    # print(html)  # 网页源代码没有问题
    bsObj = BeautifulSoup(html, 'html.parser')
    # print(bsObj) #有问题, 换解析器
    items_from_page = bsObj.find_all("div", attrs={"class": "airlineData"})
    items_list = []
    for item in items_from_page:
        item_dict = {}
        # name
        item_dict['name'] = item.find("div", attrs={"class": "airlineName"})['data-name']
        # reviews
        try:
            item_dict['reviews'] = int(item.find("div", attrs={"class": "airlineReviews"}).contents[0].split(" ")[0].replace(',', ''))
        except AttributeError as e:
            item_dict['reviews'] = -1

        # link
        item_dict['link'] = item.find("a", attrs={"class": "detailsLink"})['href']
        item_dict['link'] = 'https://www.tripadvisor.com' + item_dict['link']

        items_list.append(item_dict)

    return items_list


if __name__ == '__main__':
    # HOME_URL = config.HOME_URL_NEW + "&page=0"
    # HOME_URL = 'https://www.tripadvisor.com/MetaPlacementAjax?placementName=airlines_lander_main&skipLocation=true&wrap=true' + "&page=20"
    # html_txt = get_page_html_txt(HOME_URL)
    # rtn = parse_home_page(html_txt)
    # print(len(rtn))

    page_index = 0
    Airlines = []
    while (True):
        HOME_URL = 'https://www.tripadvisor.com/MetaPlacementAjax?placementName=airlines_lander_main&skipLocation=true' + "&page=" + str(page_index)
        html_txt = get_page_html_txt(HOME_URL)
        airlines_per_page = parse_home_page(html_txt)
        print("{} -parse finished!".format(HOME_URL))
        Airlines.append(airlines_per_page)
        if len(airlines_per_page) < 10:
            print("{} -does not have 10 arilines!".format(HOME_URL))
            break
        page_index = page_index + 1
        time.sleep(2)

    print(Airlines)


