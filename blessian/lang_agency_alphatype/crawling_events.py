from datetime import datetime, timedelta
from pathlib import Path
import re

from tqdm import tqdm
import requests
from bs4 import BeautifulSoup


today = datetime.now()
end_day = today + timedelta(weeks=(3*4))

url = "https://www.mcst.go.kr/kor/s_culture/festival/festivalList.jsp?pSeq=&pRo=&pCurrentPage=1&pOrder=01up&pPeriod=pTMonth"
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

num_pages = int(soup.find_all("div", "data_count")[0].find_all("span", "fl")[0].text.split("[1/")[1][:-3])

events = ""
for page_idx in tqdm(range(num_pages)):
    url = f"https://www.mcst.go.kr/kor/s_culture/festival/festivalList.jsp?pSeq=&pRo=&pCurrentPage={page_idx+1}&pOrder=01up&pPeriod=pTMonth"
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

    for events_elem in tqdm(soup.find_all("ul", "mediaWrap")[0].find_all("div", "text")):
        event = ""
        event += "제목: " + re.sub(r"[\n\r\t]", "", events_elem.find("p", "title").text)
        event += " 상세내용: " + re.sub(r"[\n\r\t]", "", events_elem.find("div", "ny").text)

        for idx, li in enumerate(events_elem.find_all("li")):
            if idx == 0:
                event += " 기간: " + re.sub(r"[\n\r\t]", "", li.text[4:])
            elif idx == 1:
                event += " 장소: " + re.sub(r"[\n\r\t]", "", li.text[4:])
            else:
                event += " 문의: " + re.sub(r"[\n\r\t]", "", li.text[4:])

        events += event + "\n"
        
p = Path("./data/data.txt")
p.write_text(events, encoding="utf-8")


# import os
# import dotenv
# from llama_index import VectorStoreIndex, SimpleDirectoryReader

# dotenv_file = dotenv.find_dotenv(str(Path("./").absolute().joinpath(".env")))
# dotenv.load_dotenv(dotenv_file)

# documents = SimpleDirectoryReader("./").load_data()
# index = VectorStoreIndex.from_documents(documents)

# query_engine = index.as_query_engine()
# response = query_engine.query("서울에서 열리는 축제를 추천해줘")