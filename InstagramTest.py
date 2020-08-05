#-*-coding:utf-8-*-

import configparser
from CrawlingInstagramMng import *
import UtillFileDirectot

#인스타그램 데이터를 저장할 디렉토리를 만들어준다.
UtillFileDirectot.CreateCurrentDateDiretory('InstagramHash')


##with open('InstagramHash\\tes.csv', 'w', newline='') as file :
#        writer = csv.writer(file)
#        writer.writerow(['a','b','c'])



##계정정보를 파일에서 불러온다.
config = configparser.ConfigParser()
config.read('config.ini')
InstaId = config['instagram']['Id']
examplePass = config['instagram']['password']



cimTemp = CrawlingInstagramMng("./chromedriver.exe")


#cim.ConnectChromdriver()

cimTemp.LoginInstagram(InstaId, examplePass)


cimTemp.searchKeyword("전민동") 

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
