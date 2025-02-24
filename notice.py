import requests
from bs4 import BeautifulSoup

def crawl_mokpo_public_notice(page_number):
    url = f"https://www.mokpo.go.kr/www/mokpo_news/notification/public_notice?page={page_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    notices = soup.find_all("tr")  # 공지사항 리스트가 <tr> 태그에 있을 것이라고 가정
    data = []
    for notice in notices:
        try:
            title_tag = notice.find("a")
            if title_tag:
                title = notice.find('a')['title']
                title = title.replace("에 대한 글내용 보기.", "")  # "에 대한 글내용 보기." 삭제
                link = f"https://www.mokpo.go.kr{notice.find('a')['href']}"
                department = notice.find_all("td")[2].text.strip()  # 등록부서
                date = notice.find_all("td")[3].text.strip()  # 작성일
                data.append([title, department, date, link])
        except:
            continue  # 일부 항목이 없을 경우 오류를 무시

    return data

def crawl_mokpo_notice(page_number):
    url = f"https://www.mokpo.go.kr/www/mokpo_news/notice?page={page_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    notices = soup.find_all("tr")  # 공지사항 리스트가 <tr> 태그에 있을 것이라고 가정
    data = []
    for notice in notices:
        try:
            title_tag = notice.find("a")
            if title_tag:
                title = title_tag.text.strip()
                title = title.replace("새로운글", "")  # "새로운글" 삭제
                link = f"https://www.mokpo.go.kr{notice.find('a')['href']}"
                department = notice.find_all("td")[2].text.strip()  # 등록부서
                date = notice.find_all("td")[3].text.strip()  # 작성일
                data.append([title, department, date, link])
        except:
            continue  # 일부 항목이 없을 경우 오류를 무시

    return data

def crawl_jeonnam_notice(page_number):
    url = f"https://www.jeonnam.go.kr/J0203/boardList.do?infoReturn=&pageIndex={page_number}&menuId=jeonnam0203000000&searchType=&searchText=&displayHeader="
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    notices = soup.find_all("tr")  # 공지사항 리스트가 <tr> 태그에 있을 것이라고 가정
    data = []
    for notice in notices:
        try:
            title_tag = notice.find("a")
            if title_tag:
                title = title_tag.text.strip()
                title = title.replace("에 대한 글내용 보기.", "")  # "에 대한 글내용 보기." 삭제
                link = f"https://www.jeonnam.go.kr/{notice.find('a')['href']}"
                department = notice.find_all("td")[2].text.strip()  # 등록부서
                date = notice.find_all("td")[3].text.strip()  # 작성일
                data.append([title, department, date, link])
        except:
            continue  # 일부 항목이 없을 경우 오류를 무시

    return data
