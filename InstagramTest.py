
from CrawlingInstagramMng import *

#import CrawlingInstagramMng as cim


cimTemp = CrawlingInstagramMng("./chromedriver.exe")


#cim.ConnectChromdriver()

cimTemp.LoginInstagram("kjky12", "---")


cimTemp.searchKeyword("전민동")

nPostFind = cimTemp.find_content('div._9AhH0')

cimTemp.select_first('div._9AhH0')

data = cimTemp.get_content()

k = 0