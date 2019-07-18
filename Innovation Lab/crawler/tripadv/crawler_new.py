from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import pandas as pd

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

def parse_detail_page(html):
    '''
    抓取 detail page
    return:
        返回页面下所有人的标题、评论, 给航班的打分等
    '''
    bsObj = BeautifulSoup(html, 'html.parser')
    reviews_from_page = bsObj.findAll("div", attrs={"class": "location-review-review-list-parts-SingleReview__reviewContainer--N7DSv"}) # location-review-card-Card__ui_card--2Mri0 location-review-card-Card__card--o3LVm location-review-card-Card__section--NiAcw
    reviews_list = []
    for review_item in reviews_from_page:
        reviews_dict = {}
        # title
        reviews_dict['title'] = review_item.find("div", attrs={"class": "location-review-review-list-parts-ReviewTitle__reviewTitle--2GO9Z"})
        print(reviews_dict['title'])
        # content

        # reviews_list.append(reviews_dict)




if __name__ == '__main__':
# 单独 HOME_PAGE 页面的测试
    # HOME_URL = config.HOME_URL_NEW + "&page=0"
    # HOME_URL = 'https://www.tripadvisor.com/MetaPlacementAjax?placementName=airlines_lander_main&skipLocation=true&wrap=true' + "&page=20"
    # html_txt = get_page_html_txt(HOME_URL)
    # rtn = parse_home_page(html_txt)
    # print(len(rtn))

#   下面是完成可执行代码, 能够爬取所有 HOME_PAGE 上的所有航空公司的信息
    page_index = 0
    Airlines = []
    result = pd.DataFrame(data=Airlines, columns=['name', 'reviews', 'link'])
    while (True):
    # while (page_index < 2):
        HOME_URL = 'https://www.tripadvisor.com/MetaPlacementAjax?placementName=airlines_lander_main&skipLocation=true' + "&page=" + str(page_index)
        html_txt = get_page_html_txt(HOME_URL)
        airlines_per_page = parse_home_page(html_txt)
        print("{} -parse finished!".format(HOME_URL))
        df = pd.DataFrame(data=airlines_per_page, columns=['name', 'reviews', 'link'])
        result = pd.concat(objs=[result, df], ignore_index=True)
        Airlines.append(airlines_per_page)
        if len(airlines_per_page) < 10:
            print("{} -does not have 10 arilines!".format(HOME_URL))
            break
        page_index = page_index + 1
        time.sleep(2)

    print(Airlines)
    result.to_csv("./home_page_info.csv")
    
#   下面开始测试爬取 DETAIL_PAGE 的信息!
    # page_index = 0
    # Airlines = []
    # while (page_index < 2):
    #     HOME_URL = 'https://www.tripadvisor.com/MetaPlacementAjax?placementName=airlines_lander_main&skipLocation=true' + "&page=" + str(page_index)
    #     html_txt = get_page_html_txt(url=HOME_URL)
    #     airlines_per_home_page = parse_home_page(html=html_txt)
    #     Airlines.append(airlines_per_home_page)
    #     page_index = page_index + 1
    # for item in Airlines:
    #     print(item)

    # detail_page_url = 'https://www.tripadvisor.com/Airline_Review-d8728984-Reviews-Adria-Airways#REVIEWS'
    # html_txt = get_page_html_txt(url=detail_page_url)
    # print(html_txt)
    # rtn = parse_detail_page(html=html_txt)


