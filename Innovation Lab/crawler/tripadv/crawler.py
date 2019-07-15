from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from selenium import webdriver
from selenium.webdriver.common.by import By

import time
from config import *

# https://www.tripadvisor.com/MetaPlacementAjax?placementName=airlines_lander_main&wrap=true&skipLocation=true&page=0

def get_first_home_page(url):
    '''
    获取一页, return html code
    '''
    try:
        html = urlopen(url)
        return html.read()
    except HTTPError as e:
        return None

def parse_first_home_page(html_txt):
    '''
    解析 html_txt
    return: 
        items_list_after: 类型是 list, 每个元素都是一个dict, 包含3个key:'name','reviews', 'link'
    '''
    bsObj = BeautifulSoup(html_txt, 'lxml')
    # 提取每一页中10个 items, items中包含了 1.航空公司名字; 2.其下有多少评论; 3.看所有评论(detail)
    # 将这3个 value 存储在 dict 中
    items_list_before = bsObj.findAll("div", attrs={"class": "prw_rup prw_airlines_airline_lander_card"})
    items_list_after = []
    for item in items_list_before:
        item_dict = {}
        item_dict['name'] = item.find("div", attrs={"class": "airlineName"})['data-name']
        item_dict['reviews'] = int(item.find("div", attrs={"class": "airlineReviews"}).contents[0].split(" ")[0].replace(',', ''))
        item_dict['link'] = item.find("a", attrs={"class": "detailsLink"})['href']
        item_dict['link'] = 'https://www.tripadvisor.com' + item_dict['link']
        
        items_list_after.append(item_dict)
    
    # # only for test, for goto_next_home_page()
    # button = bsObj.find("span", attrs={"class": "nav next taLnk ui_button primary"})
    # print(button)
    return items_list_after

def goto_next_home_page(url):
    '''
    进行翻页功能, 能够爬取到 home page 中所有的页面
    '''
    print("start")
    # browser = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
    # browser = webdriver.PhantomJS(executable_path=r'C:\Users\runyu\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    browser = webdriver.Chrome(executable_path='/Users/runshen/chromedriver') #Mac self
    browser = webdriver.Chrome(executable_path=r'C:\Users\runyu\Downloads\chromedriver.exe') #win10
    browser.get('https://www.tripadvisor.com/Airlines')
    time.sleep(5)
    print(browser.page_source)
    button = browser.find_element_by_class_name("nav next taLnk ui_button primary").click()  #why?
    # button = browser.find_element_by_link_text('Next')
    # button = browser.find_element(By.CLASS_NAME, r"nav next taLnk ui_button primary")
    print(button)
    # print(browser.page_source) #success
    # browser.close()
    print("end")

def get_parse_datail_page(url):
    '''
    input:
        url:是某一个航班的详细页面
    work:
        提取出所有评论, 包括: 评论时间, 总评分, 各个
    '''
    html = urlopen(url)
    bsObj = BeautifulSoup(html.read(), 'lxml')

    # 未完待续



if __name__ == '__main__':
    # HOME_URL_BEGIN = 'https://www.tripadvisor.com/Airlines'
    html_txt = get_first_home_page('https://www.tripadvisor.com/Airlines')
    home_page_items_list = parse_first_home_page(html_txt)  # first page
    print(home_page_items_list) # ok

    # goto_next_home_page(HOME_URL_BEGIN)

