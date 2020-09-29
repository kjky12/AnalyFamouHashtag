#-*-coding:utf-8-*-

import os
import configparser


from Utill  import UtillFileDirectot
from Utill import GoogleVisionApi


##########################################
####공통
strSearchKeyword = "이보라"
#데이터 저장 기본 경로
strSaveDataPath = "InstagramHash"
#테이블 이름, 이미지 저장 경로
strTableName = str()
#신규 제거 및 업데이트 여부 0:제거 후 생성, 1:이어서 처리
NewOrContinue = 1


##########################################
####키워드와 테이블명 매칭 INI 식별
configConvert = configparser.ConfigParser()
configConvert.read('ConvertKR_EN.ini', encoding='utf-8')
strTableName = configConvert[strSearchKeyword]['ER']
strUserId = configConvert[strSearchKeyword]['USER_ID']


strPath = strSaveDataPath +"\\"+ strTableName + "\\"
strFileNames = UtillFileDirectot.GetDiretoryInAllFile(strPath)


for strFileNameUnit in strFileNames :
    print(strFileNameUnit)
    GoogleVisionApi.run_quickstart(strPath + strFileNameUnit)
    print("\n\n")
    


#GoogleVisionApi.run_quickstart("IMG.jpg")
