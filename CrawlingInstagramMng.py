import requests

from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re


class CrawlingInstagramMng(object):
    """Instagram 크롤링을 위한 클래스"""
    

    def __init__(self, strChromdriverPath):
        self.strChromdriverPath = strChromdriverPath
        
        options = Options()
        options.headless = False

        self.driver = wd.Chrome(executable_path=self.strChromdriverPath, options=options)
        


    def SetChromdriverPath(self, strPath) :
        self.strChromdriverPath = strPath

    def ReconnectChromdriver(self) :
        self.driver.close()
        #default option
        options = Options()
        options.headless = False
        self.driver = wd.Chrome(executable_path=strPath, options=options)

    def GetChromdriver() :
        return self.driver

    def LoginInstagram(self, strId, strPassword) :
        self.driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        time.sleep(3) #웹 페이지 로드를 보장하기 위해 3초 쉬기
        
        id_input = self.driver.find_elements_by_css_selector('#react-root > section > main > div > article > div > div > div > form > div > div > label > input')[0]
        id_input.send_keys(strId)
        password_input = self.driver.find_elements_by_css_selector('#react-root > section > main > div > article > div > div > div > form > div > div > label > input')[1]
        password_input.send_keys(strPassword)
        password_input.submit()
        
        time.sleep(3)


    def searchKeyword(self, strkeyword):
        url = "https://www.instagram.com/explore/tags/{}/".format(strkeyword)
        self.driver.get(url)
        time.sleep(1)


    def select_first(self, strCss):
        first = self.driver.find_element_by_css_selector(strCss) 
        #find_element_by_css_selector 함수를 사용해 요소 찾기
        first.click()
        time.sleep(3) #로딩을 위해 3초 대기
    
    
    def get_content(self):
        # 1. 현재 페이지의 HTML 정보 가져오기
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')    
        # 2. 본문 내용 가져오기
        try:  			#여러 태그중 첫번째([0]) 태그를 선택  
            content = soup.select('div.C4VMK > span')[0].text 
        #첫 게시글 본문 내용이 <div class="C4VMK"> 임을 알 수 있다.
        #태그명이 div, class명이 C4VMK인 태그 아래에 있는 span 태그를 모두 선택.
        except:
            content = ' ' 
        # 3. 본문 내용에서 해시태그 가져오기(정규표현식 활용)
        tags = re.findall(r'#[^\s#,\\]+', content) # content 변수의 본문 내용 중 #으로 시작하며, #뒤에 연속된 문자(공백이나 #, \ 기호가 아닌 경우)를 모두 찾아 tags 변수에 저장
        # 4. 작성 일자 가져오기
        try:
            date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10] #앞에서부터 10자리 글자
        except:
            date = ''
        # 5. 좋아요 수 가져오기
        try:
            like = soup.select('div.Nm9Fw > button')[0].text[4:-1] 
        except:
            like = 0
        # 6. 위치 정보 가져오기
        try:
            place = soup.select('div.JF9hh')[0].text
        except:
            place = ''
        
        data = [content, date, like, place, tags]
        return data

    #해당 토큰의 개수를 카운트한다(읽어온 게시글 확인용!!)
    def find_content(self, strCss):
        # 1. 현재 페이지의 HTML 정보 가져오기
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')    
        
        return  len(soup.select(strCss))