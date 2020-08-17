#-*-coding:utf-8-*-

import configparser
from CrawlingInstagramMng import *
import UtillFileDirectot
from CSqlite3 import *

strSearchKeyword = "노은동맛집추천"


#인스타그램 데이터를 저장할 디렉토리를 만들어준다.
UtillFileDirectot.CreateCurrentDateDiretory('InstagramHash')

cimTemp = CrawlingInstagramMng("./chromedriver.exe")


##########################################
####로그인!
##계정정보를 파일에서 불러온다.
#config = configparser.ConfigParser()
#config.read('config.ini')
#InstaId = config['instagram']['Id']
#examplePass = config['instagram']['password']
#cimTemp.LoginInstagram(InstaId, examplePass)



##########################################
####검색!!
cimTemp.searchKeyword(strSearchKeyword) 
##키워드에 해당하는 모든 링크 얻기!!
datalink = cimTemp.ReadAllLink()


##########################################
####키워드와 테이블명 매칭 INI 식별
configConvert = configparser.ConfigParser()
configConvert.read('ConvertKR_EN.ini', encoding='utf-8')
strTableName = configConvert[strSearchKeyword]['ER']

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


print("FINISH!!!!!!!!!!!")