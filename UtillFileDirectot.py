#-*-coding:utf-8-*-

import os
from datetime import date
import csv

# 현재 경로에 디렉토리를 만들고 오늘날짜로 디렉토리를를 생성한다.
def CreateCurrentDateDiretory(strPath) :
    #today = strPath + "\\" + str(date.today())
    if not(os.path.isdir(strPath)):
        os.makedirs(os.path.join(strPath))


def GetCurrentYMD(strPath) :    
    return strPath + "\\" + str(date.today())


def WriteCsv(strPath, lisT) :
    with open(strPath + ".csv", 'a', newline='', encoding='utf-8') as file :
        writer = csv.writer(file)
        writer.writerow(lisT)
        file.close()