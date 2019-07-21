from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import pandas as pd

import time
import datetime


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

def get_page_html_txt_selenium(url, browser):
    '''
    使用 selenium 
    '''
    while(True):
        try:
            browser.get(url)
            # "read more" 按钮不可点击, 正文才可点击, 点击之后出来完整的正文内容
            # button = browser.find_element_by_class_name("common-text-ReadMore__ctaWrapperNewline--1iDIz") # common-text-ReadMore__content--2X4LR
            button = WebDriverWait(browser, 20, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "common-text-ReadMore__ctaWrapperNewline--1iDIz")))
            button.click()
            
            break
        except:
            print("{} failed access".format(url))
            # browser.quit()
            time.sleep(10)
            continue
    return browser.page_source

def parse_detail_page(html, companyName):
    '''
    抓取 detail page 中的内容, 每个 review item 都会返回一个字典, 其中的keys如下：
    'title', 'content','cabin', 'origin', 'destination', 'region', 'DOV', 'DOW', 'contribution', 'helpful', 'Tscore', 'LR', 'SC', 'FE', 'CS', 'VM', 'CL', 'CB', 'FB'
    return:
        返回某个deatil页面下所有人的标题、评论, 给航班的打分等
        返回某个deatil页面是否是当前航空公司的评论页面的最后一页
    '''
    # 使用 bs 对网页进行解析
    bsObj = BeautifulSoup(html, 'html5lib')
    # print(html)
    # 判断这个page是不是最后一页
    is_last_page = False
    is_next_button_clickable = bsObj.find("span", attrs={"class": "ui_button nav next primary disabled"})
    if is_next_button_clickable != None:
        is_last_page = True

    reviews_from_page = bsObj.find_all("div", attrs={"class": "location-review-review-list-parts-SingleReview__reviewContainer--N7DSv"}) # location-review-card-Card__ui_card--2Mri0 location-review-card-Card__card--o3LVm location-review-card-Card__section--NiAcw
    reviews_list = []
    if reviews_from_page == None:  # 如果该页面的 reviews 没有抓取到, 那么直接返回 None
        return (None, is_last_page)
    
    for review_item in reviews_from_page: # 一条一条 review 来分析
        reviews_dict = {}
        # companyName
        reviews_dict['companyName'] = companyName
        # title
        tmp_title = review_item.find("div", attrs={"class": "location-review-review-list-parts-ReviewTitle__reviewTitle--2GO9Z"})
        reviews_dict['title'] = tmp_title.a.span.span.string
        # content
        tmp_content = review_item.find("div", attrs={"class": "common-text-ReadMore__content--2X4LR"})
        reviews_dict['content'] = tmp_content.get_text()
        # cabin, origin, destination, region
        tmp = review_item.find("div", attrs={"class": "location-review-review-list-parts-RatingLine__labelsContainer--rSajH"})
        tmp_list = tmp.contents
        reviews_dict['cabin'] = tmp_list[-1].get_text()
        reviews_dict['origin'] = tmp_list[0].get_text().split(" - ")[0]
        reviews_dict['destination'] = tmp_list[0].get_text().split(" - ")[1]
        reviews_dict['region'] = tmp_list[1].get_text()
        # date of travel (maybe not exist) 
        try:
            reviews_dict['DOV'] = review_item.find("div", attrs={"class": "location-review-review-list-parts-EventDate__event_date--1epHa"}).get_text()[16:]
        except AttributeError as e:
            reviews_dict['DOV'] = None
        # date of write (maybe not exist)
        try:
            reviews_dict['DOW'] = review_item.find("div", attrs={"class": "social-member-event-MemberEventOnObjectBlock__event_type--3njyv"}).get_text().split("wrote a review ")[-1]
            # 如果是 yesterday
            if reviews_dict['DOW'] == 'Yesterday':
                yesterday_date = datetime.datetime.now() - datetime.timedelta(days=1)
                reviews_dict['DOW'] = yesterday_date.strftime("%b %d")
        except AttributeError as e:
            reviews_dict['DOW'] = None
        # contribution, helpful
        tmp_contribution = review_item.find_all("span", attrs={"class": "social-member-MemberHeaderStats__stat_item--34E1r"})
        reviews_dict['contribution'] = 0
        reviews_dict['helpful'] = 0
        # print(len(tmp_contribution))
        if len(tmp_contribution) == 1:
            reviews_dict['contribution'] = tmp_contribution[0].span.span.string
        if len(tmp_contribution) == 2:
            reviews_dict['contribution'] = tmp_contribution[0].span.span.string
            reviews_dict['helpful'] = tmp_contribution[1].span.span.string
        # print("{}, {}".format(reviews_dict['contribution'], reviews_dict['helpful']))
        # score: total score + other 8 scores
        # total score
        tmp_total_score = review_item.find("div", attrs={"class": "location-review-review-list-parts-RatingLine__bubbles--GcJvM"})
        total_score = tmp_total_score.span.attrs['class'][-1].split("_")[-1]
        reviews_dict['Tscore'] = int(total_score) / 10
        # print(reviews_dict['Tscore'])
        # other scores (maybe not exist)
        other_scores_list = []
        other_scores_name_list = ['LR', 'SC', 'FE', 'CS', 'VM', 'CL', 'CB', 'FB']
        switch = {
            'Legroom': 'LR',
            'Seat comfort': 'SC',
            'In-flight Entertainment': 'FE',
            'Customer service': 'CS',
            'Value for money': 'VM', 
            'Cleanliness': 'CL', 
            'Check-in and boarding': 'CB',
            'Food and Beverage': 'FB'
        }
        reviews_dict['LR'] = -1 # LegRoom
        reviews_dict['SC'] = -1 # Seat comfirt
        reviews_dict['FE'] = -1 # In-flight Entertainment
        reviews_dict['CS'] = -1 # Customer Service
        reviews_dict['VM'] = -1 # Value for Money
        reviews_dict['CL'] = -1 # Cleanliness
        reviews_dict['CB'] = -1 # Check-in and Boarding
        reviews_dict['FB'] = -1 # Food and Beverage
        try:
            tmp_other_scores_item = review_item.find("div", attrs={"class": "location-review-review-list-parts-AdditionalRatings__ratings--hIt-r"})            
            tmp_other_socres = tmp_other_scores_item.find_all("div", attrs={"class": "location-review-review-list-parts-AdditionalRatings__rating--1_G5W"})
            # print(len(tmp_other_socres))
            for score in tmp_other_socres:
                # print("{}, {}".format(switch[score.contents[-1].string], int(score.span.span.attrs['class'][-1].split("_")[-1]) / 10))
                reviews_dict[switch[score.contents[-1].string]] = int(score.span.span.attrs['class'][-1].split("_")[-1]) / 10      
        except Exception as e:
            # print(e)
            pass

        reviews_list.append(reviews_dict)

    df = pd.DataFrame(data=reviews_list, columns=['companyName', 'title', 'content','cabin', 'origin', 'destination', 'region', 'DOV', 'DOW', 'contribution', 'helpful', 'Tscore', 'LR', 'SC', 'FE', 'CS', 'VM', 'CL', 'CB', 'FB'])
    # print(df)
    
    return (df, is_last_page)

def make_detail_page_url(url, page_index):
    '''
    input

        page_index: 第几页
    output
        生成好的 url
    '''
    urls = url.split("-")
    result = urls[0] + "-" + urls[1] + "-" + urls[2] + "-or" + str(page_index) + "-"
    for i in range(3, len(urls)):
        result = result + urls[i] + "-"
    return result[:-1]


if __name__ == '__main__':
    # detail_page_url = 'https://www.tripadvisor.com/Airline_Review-d8728984-Reviews-Adria-Airways'
    #         tmp_url = 'https://www.tripadvisor.com/Airline_Review-d8728984-Reviews-or15-Adria-Airways#REVIEWS'
    # 静默模式使用 selenium
    # options.add_argument("headless")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    # browser = webdriver.Chrome(executable_path='/Users/runshen/chromedriver') #Mac self
    browser = webdriver.Chrome(executable_path=r'C:\Users\Runshen\Downloads\chromedriver.exe', options=options) # Runshen
    result = pd.DataFrame(columns=['companyName', 'title', 'content','cabin', 'origin', 'destination', 'region', 'DOV', 'DOW', 'contribution', 'helpful', 'Tscore', 'LR', 'SC', 'FE', 'CS', 'VM', 'CL', 'CB', 'FB'])
    home_page_df = pd.read_csv(r"C:\Users\Runshen\Documents\GitHub\PP_Work\Innovation Lab\crawler\home_page_info.csv")
    for ix, company in home_page_df.iterrows():
        page_index = 0
        print("{} is crawling ... totally {} reviews".format(company['name'], company['reviews']))
        # while(page_index < company['reviews']):
        # while(page_index < 1):
        while(True):
            company_detail_page_url = make_detail_page_url(company['link'], page_index)
            html_txt = get_page_html_txt_selenium(url=company_detail_page_url, browser=browser)
            df, is_last_page = parse_detail_page(html=html_txt, companyName=company['name'])
            # df.to_csv(r"./detail_page_tmp/{}.csv".format(company['name']))
            if df is not None:
                print("    page {:5} is finshed!".format(int(page_index/5)))
                result = pd.concat(objs=[result, df], ignore_index=True)
            if is_last_page:
                break
            else:
                time.sleep(5)
            page_index = page_index + 5
    result.to_csv("./reviews_info.csv")

    
    # test for make_detail_page_url
    # url = 'https://www.tripadvisor.com/Airline_Review-d11831132-Reviews-Aerogaviota'
    # rtn = make_detail_page_url(url, 10)
    # print(rtn)
    
    # test for one detail page
    # html_txt = get_page_html_txt_selenium(url=detail_page_url)
    # rtn = parse_detail_page(html=html_txt)
    # rtn.to_csv("./test_detail_one_page.csv")
    

"""
Error 记录
https://www.tripadvisor.com/Airline_Review-d8728986-Reviews-or905-Aer-Lingus:
    File "c:/Users/Runshen/Documents/GitHub/PP_Work/Innovation Lab/crawler/tripadv/crawler_detail.py", line 177, in <module>
    df, is_last_page = parse_detail_page(html=html_txt)
    File "c:/Users/Runshen/Documents/GitHub/PP_Work/Innovation Lab/crawler/tripadv/crawler_detail.py", line 80, in parse_detail_page
    tmp_list = tmp.contents
    AttributeError: 'NoneType' object has no attribute 'contents'
"""
