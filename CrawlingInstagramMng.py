#-*-coding:utf-8-*-

import requests

from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re


import UtillFileDirectot



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
        time.sleep(3)

    def searchInstaUrl(self, strUrl):
        url = "https://www.instagram.com/{0}".format(strUrl)
        self.driver.get(url)
        time.sleep(3)


    def select_first(self, strCss):
        first = self.driver.find_element_by_css_selector(strCss) 
        #find_element_by_css_selector 함수를 사용해 요소 찾기
        first.click()
        time.sleep(3) #로딩을 위해 3초 대기
    
    
    def get_content(self):
        #get_content()
        #현재 선택된 항목을 읽어온다.
        # return [URL, 게시글, 올린 날짜, 좋아요 개수, 지정 위치, 해쉬태그]

        ################################################
        # 1. 현재 페이지의 HTML 정보 가져오기
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')    
        
        
        ################################################
        ### 2. 본문 내용 가져오기
        #20200817 kjky12 : 엔터때문에 해쉬태그가 합쳐지는것같은 경우 발생!
        ##try:  			#여러 태그중 첫번째([0]) 태그를 선택  
        ##    content = str(soup.select('div.C4VMK > span')[0].text) 
        ###첫 게시글 본문 내용이 <div class="C4VMK"> 임을 알 수 있다.
        ###태그명이 div, class명이 C4VMK인 태그 아래에 있는 span 태그를 모두 선택.
        ##except:
        ##    content = ' ' 
        #tags = re.findall(r'#[^\s#,\\]+', content) # content 변수의 본문 내용 중 #으로 시작하며, #뒤에 연속된 문자(공백이나 #, \ 기호가 아닌 경우)를 모두 찾아 tags 변수에 저장

        #dataContent = list()
        contentTmp = str()
        try:  			#여러 태그중 첫번째([0]) 태그를 선택  
            content2 = soup.select('div.C4VMK > span')[0]
            for contentDetail in content2.contents :
                
                if( type(contentDetail).__name__ is "NavigableString") :
                    #공백, 스페이스 1번을 없애주기위해서.. len을 넣은 이유는 공백과 스페이스바를 추가해도 분기 무시를 안하는 경우가 있어서!
                    if contentDetail is not "" and contentDetail is not " " and len(contentDetail) is not 1 and len(contentDetail) is not 0: 
                        contentTmp += contentDetail + "\t"
                        #dataContent.append(contentDetail)
                elif( type(contentDetail).__name__ is "Tag") :
                    if contentDetail.text is not "" and contentDetail.text is not " " :
                        contentTmp += contentDetail.text + "\t"
                        #dataContent.append(contentDetail.text)

        #첫 게시글 본문 내용이 <div class="C4VMK"> 임을 알 수 있다.
        #태그명이 div, class명이 C4VMK인 태그 아래에 있는 span 태그를 모두 선택.
        except:
            content2 = ' ' 

        ################################################
        # 3. 본문 내용에서 해시태그 가져오기(정규표현식 활용)
        tags = re.findall(r'#[^\s#,\\]+', contentTmp) # content 변수의 본문 내용 중 #으로 시작하며, #뒤에 연속된 문자(공백이나 #, \ 기호가 아닌 경우)를 모두 찾아 tags 변수에 저장
        # 4. 작성 일자 가져오기
        try:
            #date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10] #앞에서부터 10자리 글자
            date = str(soup.select('time._1o9PC.Nzb55')[0]['datetime']) #앞에서부터 10자리 글자
        except:
            date = ''

        TIdx = date.find('T')
        dateValue = date[0:TIdx] + " " + date[TIdx + 1:TIdx+9]

        # 5. 좋아요 수 가져오기
        try:
            like = str(soup.select('div.Nm9Fw > button')[0].text[4:-1]) 
        except:
            like = 0
        # 6. 위치 정보 가져오기
        try:
            place = str(soup.select('div.JF9hh')[0].text)
        except:
            place = ''
        

        #self.close_content()

        data = [self.driver.current_url, contentTmp, dateValue, like, place, tags]

        #UtillFileDirectot.WriteCsv(UtillFileDirectot.GetCurrentYMD("InstagramHash"), data)

        return data

    def close_content(self):
        
        self.select_first('div.QBdPU')

    #선택한 개시물 다음 게시물 선택
    def move_next(self):
        try :
            right = self.driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow') 
            right.click()
            time.sleep(3)
            return True
        except :
            return False



    #해당 토큰의 개수를 카운트한다(읽어온 게시글 확인용!!)
    def find_content(self, strCss):
        # 1. 현재 페이지의 HTML 정보 가져오기
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')    
        
        return  len(soup.select(strCss))


    def ReadAllLink(self) :
        SCROLL_PAUSE_TIME = 1.0
        reallink = []

        while True :
            pageString = self.driver.page_source
            bsObj = BeautifulSoup(pageString, 'lxml')
        
            for link1 in bsObj.find_all(name='div', attrs={"class":"Nnq7C weEfm"}):
                for i in range(3):
                    title = link1.select('a')[i]
                    real = title.attrs['href']
                    reallink.append(real)

            last_height = self.driver.execute_script('return document.body.scrollHeight')
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = self.driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                    continue

        return reallink;