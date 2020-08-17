#-*-coding:utf-8-*-

import configparser
from CrawlingInstagramMng import *
import UtillFileDirectot
from CSqlite3 import *
import time

##########################################
####공통
strSearchKeyword = "노은동맛집추천"


##########################################
####키워드와 테이블명 매칭 INI 식별
configConvert = configparser.ConfigParser()
configConvert.read('ConvertKR_EN.ini', encoding='utf-8')
strTableName = configConvert[strSearchKeyword]['ER']


##########################################
####해당 키워드에서 생성된 url을 전부 얻어온다.
sqlc = CSqlite3()
sqlc.ConnectDb("INSTAGRAM")
strQry = "SELECT INSTA_URL FROM {0}".format(strTableName)
dataurl = sqlc.LoadData(strQry)


##########################################
####URL을 이용해 모두 검색하여 데이터베이스에 입력한다.
cimTemp = CrawlingInstagramMng("./chromedriver.exe")

data = list()
for url in dataurl :
    cimTemp.searchInstaUrl(url)
    data1 = cimTemp.get_content() #게시물 정보 가져오기

    try :
        strContent = data1[1]
    except : 
        strContent = ""

    try :
        strContent_date = data1[2]
    except : 
        strContent_date = ""

    try :
        strContent_like = data1[3]
    except : 
        strContent_like = ""

    try :
        strContent_place = data1[4]
    except : 
        strContent_place = ""


    try :
        strContent_tag = "".join(data1[5]) #어차피 해시태그여서 구분가능
    except : 
        strContent_tag = ""

    strQry = '''UPDATE {0} SET 
            CONTENT = "{1}",
            CONTENT_DATE = "{2}",
            CONTENT_LIKE = {3},
            CONTENT_PLACE = "{4}",
            CONTENT_TAG = "{5}",
            INSERT_DATE = datetime('now')
            WHERE INSTA_URL = "{6}" '''.format(strTableName, strContent, strContent_date,strContent_like,strContent_place, strContent_tag, url)

    data.append(data1)
    sqlc.ExecuteDb(strQry)


sqlc.DisconnectsDb()

