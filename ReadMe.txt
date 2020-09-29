
##################################
##FIX INFO
ConfigIni.py : 인스타그램 로그인 계정/패스워드 ini파일을 만들어준다.

ContentKewordFromInstaUrlToDB.py : 검색어로 모든 url을 DB에 저장한다!(링크만 저장하기 때문에 다음 Insert정보를 입력해 주어야한다.)
ContentUsrIdFromInstagUrlToDB.py : 사용자 ID의 모든 url을 DB에 저장한다!(링크만 저장하기 때문에 다음 Insert정보를 입력해 주어야한다.)

InsertKewordInstaUrlDataToDB.py : 링크를 읽어와 추가 데이터를 Update해준다.

Utill/CrawlingInstagramMng.py : 인스타그램 크롤링 버튼 및 저장 등의 함수를 관리해준다.
Utill/CSqlite3.py : DB를 관리하는 파이썬 코드(쿼리문을 통해 테이블을 만들고 EXECUTE해준다.)
Utill/GoogleVisionApi.py : GOOGLE CLOUD vision api를 이용해서 얼굴, 라벨 등을 처리해준다.
Utill/UtillFileDirectot.py : 파일 관리 및 디렉토리 관리 함수를 제공한다.




##################################
##2020-09-29 - kjky12
구글 비전 설치!!
pip install --upgrade google-api-python-client
pip install --upgrade google-cloud-vision


---------
참고 : https://blog.naver.com/PostView.nhn?blogId=rhrkdfus&logNo=221335357361&parentCategoryNo=&categoryNo=40&viewDate=&isShowPopularPosts=true&from=search
#info경로의 Google vision json파일을 경로에 추가해주어야함.(경로는 자유^_^)
setx GOOGLE_APPLICATION_CREDENTIALS (json 파일 위치)\(json 파일 이름).json



##################################
##2020-09-08 - kjky12
얼굴인식을 위한 라이브러리 설치!!
pip install matplotlib 
pip install numpy
pip install opencv-python



/****************************************/
오전 11:00 2020-08-25
1. CreateKewordInstaUrlToDB.py : 검색어로 링크를 DB에 저장한다!
2. InsertKewordInstaUrlDataToDB.py : 링크를 읽어와 추가 데이터를 Update해준다.

/****************************************/


##################################
##2020-08-14 - kjky12
#1. sqlite를 이용해 데이터를 저장 할 유닛 테스트 수행
 - 데이터베이스 생성 및 테이블 생성 테스트
 - 쿼리문 관리 클래스 생성!


#2. 인스타그램 크롤링 수정
 - 로그인 로직 일단 제외
 - 스크롤을 내리며 링크만 먼저 따는 로직으로 수정...

@ 추가적으로 링크를 얻고 링크마다 접속해서 데이터 읽어들이는 과정을 만들어야할듯....


##################################
##2020-08-01 - kjky12

제거 : python-instagram
추가 설치
1.1. pip install selenium
1.2. pip install BeautifulSoup4
1.3. pip install requests
1.4. pip install lxml
2. chromedriver_win32.zip파일 다운후 설치
url : https://sites.google.com/a/chromium.org/chromedriver/downloads
 - 크롬에서 [도움말]-[Chrom 정보]에서 버전에 맞춰서 다운받도록하자!



##################################
##2020-07-31 - kjky12
추가 설치
pip install python-instagram

비고