#-*-coding:utf-8-*-

import urllib.request
import configparser
from Utill  import CrawlingInstagramMng
from Utill  import UtillFileDirectot
from Utill  import CSqlite3
import time

##########################################
####공통
strSearchKeyword = "이보라"
#데이터 저장 기본 경로
strSaveDataPath = "InstagramHash"
#테이블 이름, 이미지 저장 경로
strTableName = str()
#신규 제거 및 업데이트 여부 0:제거 후 생성, 1:이어서 처리
NewOrContinue = 1

#인스타그램 데이터를 저장할 디렉토리를 만들어준다.
UtillFileDirectot.CreateCurrentDateDiretory(strSaveDataPath)

cimTemp = CrawlingInstagramMng.CrawlingInstagramMng("./chromedriver.exe")

##########################################
####로그인!
##계정정보를 파일에서 불러온다.
config = configparser.ConfigParser()
config.read('config.ini')
InstaId = config['instagram_PK']['Id']
examplePass = config['instagram_PK']['password']
cimTemp.LoginInstagram(InstaId, examplePass)


##########################################
####키워드와 테이블명 매칭 INI 식별
configConvert = configparser.ConfigParser()
configConvert.read('ConvertKR_EN.ini', encoding='utf-8')
strTableName = configConvert[strSearchKeyword]['ER']


##########################################
####해당 키워드에서 생성된 url을 전부 얻어온다.
sqlc = CSqlite3.CSqlite3()
#sqlc.ConnectDb("INSTAGRAM")
sqlc.ConnectDb(strSaveDataPath + "\\INSTAGRAM")
strQry = "SELECT INSTA_URL FROM {0}".format(strTableName)
dataurl = sqlc.LoadData(strQry)


##########################################
####URL을 이용해 모두 검색하여 데이터베이스에 입력한다.


data = list()
for url in dataurl :
    cimTemp.searchInstaUrl(url)
    data1 = cimTemp.get_content() #게시물 정보 가져오기

    try :
        strInstaId = data1[1]
    except : 
        strInstaId = ""

    try :
        strContent = data1[2]
    except : 
        strContent = ""

    try :
        strContent_date = data1[3]
    except : 
        strContent_date = ""

    try :
        strContent_like = data1[4]
    except : 
        strContent_like = ""

    try :
        strContent_place = data1[5]
    except : 
        strContent_place = ""

    try :
        strContent_tag = "".join(data1[6]) #어차피 해시태그여서 구분가능
    except : 
        strContent_tag = ""

    strQry = '''UPDATE {0} SET 
            INSTA_ID = "{1}",
            CONTENT = "{2}",
            CONTENT_DATE = "{3}",
            CONTENT_LIKE = "{4}",
            CONTENT_PLACE = "{5}",
            CONTENT_TAG = "{6}",
            INSERT_DATE = datetime('now')
            WHERE INSTA_URL = "{7}" '''.format(strTableName, strInstaId,strContent, strContent_date,strContent_like,strContent_place, strContent_tag, url)

    ImageurlData = cimTemp.get_imageUrl()

    data.append(data1)
    sqlc.ExecuteDb(strQry)

    UtillFileDirectot.CreateCurrentDateDiretory(strSaveDataPath + "\\" + strTableName)

    strImageName = url.replace("/", "@")
    Idx = 0
    for img in ImageurlData :
        urllib.request.urlretrieve(img, strSaveDataPath + "\\" + strTableName + "\\" +strInstaId + strImageName + "{0:03d}".format(Idx) + ".png")
        Idx += 1

    #strContentImagePath = strContent


sqlc.DisconnectsDb()

