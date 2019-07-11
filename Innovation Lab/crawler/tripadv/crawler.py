from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from selenium import webdriver

from config import *

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

    return items_list_after

def update_home_page(url):
    '''
    进行翻页功能, 能够爬取到 home page 中所有的页面
    '''
    print("start")
    # browser = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
    # browser = webdriver.PhantomJS(executable_path=r'C:\Users\runyu\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    browser = webdriver.Chrome(executable_path='/Users/runshen/chromedriver') #Mac self
    browser.get('https://www.tripadvisor.com/Airlines')
    # button = browser.find_element_by_class_name("nav next taLnk ui_button primary")
    button = browser.find_element_by_link_text('Next')
    print(button)
    # print(browser.page_source)
    # browser.close()
    # print("end")


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
    # html_txt = get_first_home_page('https://www.tripadvisor.com/Airlines')
    # home_page_items_list = parse_first_home_page(html_txt)  # first page
    # print(home_page_items_list) # ok

    update_home_page(HOME_URL_BEGIN)

