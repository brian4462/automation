from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

#####################################
#진행하고자 하는 프로젝트 번호 ex:'202007-31200-04'
prjctMgtNo=input('프로젝트 번호를 입력하세요(ex:202007-31200-04): ')
user_id=input('아이디를 입력하세요: ')
user_pwd=input('패스워드를 입력하세요: ')
#####################################
#크롬브라우저 사용
driver = webdriver.Chrome()

#공가랑접속
driver.get("https://gongga.lx.or.kr/ehis/")
time.sleep(2)

#로그인
driver.find_element_by_css_selector(".login_area li.login").click()
time.sleep(2)
driver.find_element_by_name('i_usid').send_keys(user_id)
driver.find_element_by_name('i_pwd').send_keys(user_pwd)
driver.find_element_by_name('i_pwd').send_keys(Keys.RETURN)
time.sleep(2)

#빈집지도페이지 진입
try:
    alert = driver.switch_to_alert()
    alert.accept()
except:
    print('alert오류')
driver.find_element_by_css_selector(".binzipMap").click()
time.sleep(5)
#등급산정조사 페이지 open
driver.find_element_by_css_selector("#m_3000").click()
driver.find_element_by_css_selector("#m_3200").click()
driver.find_element_by_css_selector("#m_3240").click()

#새 팝업 페이지 제어
time.sleep(1)
driver.switch_to_window(driver.window_handles[1]) 
driver.get_window_position(driver.window_handles[1])

#목록조회
driver.find_element_by_css_selector("#prjList").click()
driver.find_element_by_css_selector("#prjList option[value='"+prjctMgtNo+"']").click()
driver.find_element_by_css_selector("#btnSearch").click()

#빈집 전체 개수 저장 (현재는 필요없음) 나중에 쓸일있을듯
time.sleep(1)
ehCntTxt = driver.find_element_by_css_selector(".ui-paging-info").get_attribute("innerHTML")
driver.find_element_by_css_selector("#location").click()
ehCnt = ehCntTxt.split('of')[1].strip()
if ehCnt.find(",") > 0:
    ehCnt = "".join(ehCnt.split(','))

#빈집고유번호파일 읽어와서 리스트에 저장
##############################################################
'''txt파일에 빈집고유번호만 한줄씩 넣어 저장 후 그 경로를 써준다'''
##############################################################
ehTargetList = []
f = open("captureList.txt", 'r')
while True:
    line = f.readline()
    if not line: break
    ehTargetList.append(line.strip())
f.close()

#반복 탐색 및 스냅샷
while True:
    #해당 페이지의 빈집고유번호 목록을 가져온다(10개)
    ehlist = driver.find_elements_by_css_selector("td[aria-describedby='mainGrid_ehEsntlNo']")
    for eh in ehlist:
        #txt파일 첫번째 줄과 일치하는 빈집고유번호가 있는지 체크
        if str(ehTargetList[0]) == str(eh.get_attribute('innerHTML')):
            print('-----------빈집고유번호-------------')
            print(ehTargetList[0])
            ehTargetList.pop(0)
            print('------------스냅샷실행--------------')
            eh.find_element_by_xpath('..').click()
            time.sleep(1)
            driver.find_element_by_css_selector("#SbtnSnap2").click()
            time.sleep(7)
            try:
                alert = driver.switch_to_alert()
                alert.accept()
            except:
                print('alert오류')
            time.sleep(1)
            #부모 페이지 제어
            driver.switch_to_window(driver.window_handles[0]) 
            driver.get_window_position(driver.window_handles[0])
            #새로고침
            driver.refresh()
            time.sleep(3)
            #팝업 페이지 제어
            driver.switch_to_window(driver.window_handles[1]) 
            driver.get_window_position(driver.window_handles[1])
            time.sleep(1)
            break
        if eh == ehlist[-1]:
            #목록에 일치하는 빈집번호가 없을경우 다음페이지 클릭
            driver.find_element_by_css_selector(".ui-icon.ui-icon-seek-next").click()
            time.sleep(2)
            break
    #txt파일의 남은 빈집번호가 없으면 loop 종료
    if(len(ehTargetList)==0):
        break

#팝업창 닫기
driver.close()
#부모창 닫기
driver.switch_to_window(driver.window_handles[0]) 
driver.get_window_position(driver.window_handles[0])
driver.close()
print('끝')