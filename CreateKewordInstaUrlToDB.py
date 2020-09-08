#-*-coding:utf-8-*-

import configparser
from CrawlingInstagramMng import *
import UtillFileDirectot
from CSqlite3 import *

##########################################
####공통
strSearchKeyword = "노은동맛집"
#데이터 저장 기본 경로
strSaveDataPath = "InstagramHash"
#테이블 이름, 이미지 저장 경로
strTableName = str()
#신규 제거 및 업데이트 여부 0:제거 후 생성, 1:이어서 처리
NewOrContinue = 1



#인스타그램 데이터를 저장할 디렉토리를 만들어준다.
UtillFileDirectot.CreateCurrentDateDiretory(strSaveDataPath)

cimTemp = CrawlingInstagramMng("./chromedriver.exe")


##########################################
####로그인!
##계정정보를 파일에서 불러온다.
config = configparser.ConfigParser()
config.read('config.ini')
InstaId = config['instagram']['Id']
examplePass = config['instagram']['password']
cimTemp.LoginInstagram(InstaId, examplePass)



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
sqlc.ConnectDb(strSaveDataPath + "\\INSTAGRAM")

if NewOrContinue == 0 :
    ##검색어_관련 테이블 생성
    try :
        sqlc.DropTable(strTableName)
    except :
        print("Can't Drop Table")

try :
    sqlc.CreateTable(strTableName)
except :
    print("Can't Create Table")


#print("RealCount =" + str(datalink) )

#여기서 데이터베이스에 링크를 모두 넣어줌...
for link in datalink :    
    strQry = "INSERT INTO {0} (INSTA_URL) VALUES (\'{1}\') ".format(strTableName, link)
    print(sqlc.ExecuteDb(strQry))
sqlc.DisconnectsDb()


print("FINISH!!!!!!!!!!!")