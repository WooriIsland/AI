import re
import time
import json
import multiprocessing as mp
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement


# browser options
options = webdriver.ChromeOptions()
options.add_argument('--headless')                                      # 메뉴바 같은 불필요한 요소들을 없앤다.
options.add_argument('--no-sandbox')                                    # 보안 관련 설정 끄기(쿠키 수락 같은 팝업들을 방지하기 위함)
options.add_argument('--disable-dev-shm-usage')                         # 개발자 도구 끄기.
options.add_experimental_option('detach', True)                         # 실행이 멈춰도 웹브라우저가 꺼지지 않게 하는 옵션

# initialize driver
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

# get page
driver.get("https://korean.visitkorea.or.kr/kfes/list/wntyFstvlList.do")
driver.implicitly_wait(10)
time.sleep(1)

def get_info(url: str) -> str:
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
    else :
        print(response.status_code)
        return str(response.status_code)

    title = soup.select_one("#festival_head").get_text()

    period = soup.select_one("body > main > div > div > section.poster_title > div > div > div.schedule > span:nth-child(2)").get_text()

    content = soup.select_one("body > main > div > div > section.poster_detail > div > div.poster_info_content > div.m_img_fst > div").get_text()
    content = re.sub(r"[\n\r\t]", "", content)[:-3]

    return f"축제이름: {title}\n기간: {period}\n내용: {content}"

def get_events(query: str) -> str:
    json_obj = json.loads(query)
    period = json_obj["period"]
    region = json_obj["region"]
    
    select_date_element = driver.find_element(By.ID, "searchDate")
    select_date = Select(select_date_element)
    select_date.select_by_visible_text(period)

    select_area_element = driver.find_element(By.ID, "searchArea")
    select_area = Select(select_area_element)
    select_area.select_by_visible_text(region)

    driver.find_element(By.ID, "btnSearch").send_keys(Keys.ENTER)
    driver.implicitly_wait(10)
    time.sleep(2)

    ul_element = driver.find_element(By.ID, "fstvlList")
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")
    urls = [elem.find_element(By.TAG_NAME, "a").get_attribute("href") for elem in li_elements]


    # cpu 개수
    num_cpu = mp.cpu_count()

    # 병렬 처리에 사용할 프로세스 개수 지정
    pool = Pool(processes=num_cpu)

    # 병렬 처리 실행
    result = pool.map(get_info, urls)
    
    return {
        "recommend": "\n\n".join(result),
        "next_action": "general_conversation"
    }