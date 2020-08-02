
from CrawlingInstagramMng import *

#import CrawlingInstagramMng as cim


cimTemp = CrawlingInstagramMng("./chromedriver.exe")


#cim.ConnectChromdriver()

cimTemp.LoginInstagram("kjky12", "rn443392!!!")


cimTemp.searchKeyword("전민동") 

#nPostFind = cimTemp.find_content('div._9AhH0')






cimTemp.select_first('div._9AhH0')

data1 = cimTemp.get_content()

cimTemp.select_first('div._9AhH0')

data2 = cimTemp.get_content()


k = 0