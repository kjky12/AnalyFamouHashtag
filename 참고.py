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

ab = ddd

##########################################
####검색!!
cimTemp.searchInstaUrl(strSearchKeyword) 
##키워드에 해당하는 모든 링크 얻기!!
datalink = cimTemp.ReadAllLink()



##########################################
####데이터베이스 생성 및 테이블 추가 테스트!!
sqlc = CSqlite3()
sqlc.ConnectDb("INSTAGRAM")

##검색어_관련 테이블 생성
try :
    sqlc.DropTable(strTableName)
except :
    print("Can't Drop Table")

sqlc.CreateTable(strTableName)

#전체 데이터 링크를 비교
count = len(datalink)
##링크데이터 중복을 제거해준다!! -> 크롤링하며 얻어오는 과정에서 중복으로 입력되는 것!(스크롤내리면서 똑같은게 보일수 잇으니)
setlink = set(datalink)
listlink = list(setlink)

countCompare = len(listlink)

print("count = " + str(count), "RealCount =" + str(countCompare) )

#여기서 데이터베이스에 링크를 모두 넣어줌...
for link in listlink :    
    strQry = "INSERT INTO {0} (INSTA_URL) VALUES (\'{1}\') ".format(strTableName, link)
    print(sqlc.ExecuteDb(strQry))
sqlc.DisconnectsDb()



#nPostFind = cimTemp.find_content('div._9AhH0')


#cimTemp.select_first('div._9AhH0')

#data = []
#for i in range(100):
#    data1 = cimTemp.get_content() #게시물 정보 가져오기
#    data.append(data1)
#    bFlag = cimTemp.move_next()    

#    if bFlag == False :
#        break





#cimTemp.select_first('div._9AhH0')
#data1 = cimTemp.get_content()

#cimTemp.select_first('div._9AhH0')
#data2 = cimTemp.get_content()
