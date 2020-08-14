#-*-coding:utf-8-*-

import configparser
from CrawlingInstagramMng import *
import UtillFileDirectot

from CSqlite3 import *

#sqlc = CSqlite3()

#데이터베이스 생성 및 테이블 추가 테스트!!
#sqlc = CSqlite3()
#sqlc.ConnectDb("INSTAGRAM")
#sqlc.CreateTable("DOONSAN")

ab= dd

#인스타그램 데이터를 저장할 디렉토리를 만들어준다.
UtillFileDirectot.CreateCurrentDateDiretory('InstagramHash')



##계정정보를 파일에서 불러온다.
config = configparser.ConfigParser()
config.read('config.ini')
InstaId = config['instagram']['Id']
examplePass = config['instagram']['password']



cimTemp = CrawlingInstagramMng("./chromedriver.exe")


#cim.ConnectChromdriver()

#cimTemp.LoginInstagram(InstaId, examplePass)


cimTemp.searchKeyword("노은동맛집") 

##키워드에 해당하는 모든 링크 입력!
datalink = cimTemp.ReadAllLink()

#여기서 데이터베이스에 링크를 모두 넣어줌...
for link in datalink :    
    link



#nPostFind = cimTemp.find_content('div._9AhH0')


cimTemp.select_first('div._9AhH0')

data = []
for i in range(100):
    data1 = cimTemp.get_content() #게시물 정보 가져오기
    data.append(data1)
    bFlag = cimTemp.move_next()    

    if bFlag == False :
        break





#cimTemp.select_first('div._9AhH0')
#data1 = cimTemp.get_content()

#cimTemp.select_first('div._9AhH0')
#data2 = cimTemp.get_content()
