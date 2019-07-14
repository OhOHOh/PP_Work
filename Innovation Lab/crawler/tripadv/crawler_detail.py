from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError

import time
import config

def get_page_html_txt(url):
    '''
    获取 url page 的源代码
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    try:
        html = requests.get(url, headers=headers)
        return html.text
    except HTTPError as e:
        return None

def parse_detail_page(html):
    '''
    抓取 detail page
    return:
        返回页面下所有人的标题、评论, 给航班的打分等
    '''
    bsObj = BeautifulSoup(html, 'html5lib')
    print(html)
    reviews_from_page = bsObj.find_all("div", attrs={"class": "location-review-review-list-parts-SingleReview__reviewContainer--N7DSv"}) # location-review-card-Card__ui_card--2Mri0 location-review-card-Card__card--o3LVm location-review-card-Card__section--NiAcw
    reviews_list = []
    print(reviews_from_page)
    # for review_item in reviews_from_page:
    #     reviews_dict = {}
    #     # title
    #     reviews_dict['title'] = review_item.find("div", attrs={"class": "location-review-review-list-parts-ReviewTitle__reviewTitle--2GO9Z"})
    #     print(reviews_dict['title'])
    #     # content

    #     reviews_list.append(reviews_dict)
    
    return reviews_list


if __name__ == '__main__':
    detail_page_url = 'https://www.tripadvisor.com/Airline_Review-d8728984-Reviews-Adria-Airways#REVIEWS'
    html_txt = get_page_html_txt(url=detail_page_url)
    rtn = parse_detail_page(html=html_txt)