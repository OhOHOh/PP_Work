from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from selenium import webdriver
from selenium.webdriver.common.by import By

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

def get_page_html_txt_selenium(url):
    '''
    使用 selenium 
    '''
    browser = webdriver.Chrome(executable_path=r'C:\Users\runyu\Downloads\chromedriver.exe') #win10
    browser.get(url)
    # "read more" 按钮不可点击, 正文才可点击, 点击之后出来完整的正文内容
    button = browser.find_element_by_class_name("common-text-ReadMore__ctaWrapperNewline--1iDIz") # common-text-ReadMore__content--2X4LR
    # print(button)
    button.click()
    # time.sleep(5)
    return browser.page_source


def parse_detail_page(html):
    '''
    抓取 detail page
    return:
        返回页面下所有人的标题、评论, 给航班的打分等
    '''
    # 使用 bs 对网页进行解析
    bsObj = BeautifulSoup(html, 'html5lib')
    # print(html)
    reviews_from_page = bsObj.find_all("div", attrs={"class": "location-review-review-list-parts-SingleReview__reviewContainer--N7DSv"}) # location-review-card-Card__ui_card--2Mri0 location-review-card-Card__card--o3LVm location-review-card-Card__section--NiAcw
    # print(reviews_from_page)
    reviews_list = []
    
    for review_item in reviews_from_page:
        reviews_dict = {}
        # title
        tmp_title = review_item.find("div", attrs={"class": "location-review-review-list-parts-ReviewTitle__reviewTitle--2GO9Z"})
        reviews_dict['title'] = tmp_title.a.span.span.string
        # content
        tmp_content = review_item.find("div", attrs={"class": "common-text-ReadMore__content--2X4LR"})
        reviews_dict['content'] = tmp_content.get_text()
        # category, start, end, region
        tmp = review_item.find("div", attrs={"class": "location-review-review-list-parts-RatingLine__labelsContainer--rSajH"})
        tmp_list = tmp.contents
        reviews_dict['category'] = tmp_list[-1].get_text()
        reviews_dict['start'] = tmp_list[0].get_text().split(" - ")[0]
        reviews_dict['end'] = tmp_list[0].get_text().split(" - ")[1]
        reviews_dict['region'] = tmp_list[1].get_text()
        # date of travel
        try:
            reviews_dict['DOV'] = review_item.find("div", attrs={"class": "location-review-review-list-parts-EventDate__event_date--1epHa"}).get_text()[16:]
        except AttributeError as e:
            reviews_dict['DOV'] = None
        # date of write
        try:
            reviews_dict['DOW'] = review_item.find("div", attrs={"class": "social-member-event-MemberEventOnObjectBlock__event_type--3njyv"}).get_text().split("wrote a review ")[-1]
        except AttributeError as e:
            reviews_dict['DOW'] = None

        # score: total score + other 8 scores
        # total score
        tmp_total_score = review_item.find("div", attrs={"class": "location-review-review-list-parts-RatingLine__bubbles--GcJvM"})
        total_score = tmp_total_score.span.attrs['class'][-1].split("_")[-1]
        reviews_dict['Tscore'] = int(total_score) / 10
        print(reviews_dict['Tscore'])

        reviews_list.append(reviews_dict)
    
    return reviews_list


if __name__ == '__main__':
    detail_page_url = 'https://www.tripadvisor.com/Airline_Review-d8728984-Reviews-Adria-Airways'
    html_txt = get_page_html_txt_selenium(url=detail_page_url)
    rtn = parse_detail_page(html=html_txt)
    # print(rtn)
    