from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# webdriver-manager 임포트
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# .env 파일은 로컬 테스트 시에만 사용됩니다.
load_dotenv()

def get_usage_data():
    """
    아이즈 모바일 웹사이트에 접속하여 실시간 사용량을 스크래핑하고
    결과를 딕셔너리 형태로 반환하는 함수입니다.
    """
    user_id = os.environ.get('EYES_ID')
    user_pw = os.environ.get('EYES_PW')
    main_page_url = 'https://www.eyes.co.kr/'
    usage_url = 'https://www.eyes.co.kr/mypage/main' 

    options = webdriver.ChromeOptions()
    # 서버 환경에서는 화면이 없으므로 headless 옵션이 필수입니다.
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

    # webdriver_manager를 사용하여 자동으로 드라이버를 설정합니다.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # --- 로그인 과정 ---
        driver.get(main_page_url)
        time.sleep(2)
        driver.execute_script("modalLoginOpen()")
        
        wait = WebDriverWait(driver, 10)
        id_input = wait.until(EC.visibility_of_element_located((By.ID, 'login_id'))) 
        id_input.send_keys(user_id)
        driver.find_element(By.ID, 'login_pw').send_keys(user_pw) 
        driver.find_element(By.ID, 'loginBtn').click()
        time.sleep(3) 

        # --- 데이터 추출 과정 ---
        driver.get(usage_url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 음성 정보 추출
        voice_usage_element = soup.select_one('li.type2 .info ul li:nth-of-type(1) strong')
        voice_total_element = soup.select_one('li.type2 .info ul li:nth-of-type(2) span')
        voice_usage = voice_usage_element.get_text(strip=True) if voice_usage_element else "정보 없음"
        voice_total = voice_total_element.get_text(strip=True) if voice_total_element else "정보 없음"

        # 문자 정보 추출
        sms_usage_element = soup.select_one('li.type3 .info ul li:nth-of-type(1) strong')
        sms_total_element = soup.select_one('li.type3 .info ul li:nth-of-type(2) span')
        sms_usage = sms_usage_element.get_text(strip=True) if sms_usage_element else "정보 없음"
        sms_total = sms_total_element.get_text(strip=True) if sms_total_element else "정보 없음"
        
        # 데이터 정보 추출
        data_remaining_element = soup.select_one('li.type1 .info .tit span')
        data_used_element = soup.select_one('li.type1 .info ul li:nth-of-type(1) strong')
        data_total_element = soup.select_one('li.type1 .info ul li:nth-of-type(2) span')
        data_remaining = data_remaining_element.get_text(strip=True) if data_remaining_element else "정보 없음"
        data_used = data_used_element.get_text(strip=True) if data_used_element else "정보 없음"
        data_total = data_total_element.get_text(strip=True) if data_total_element else "정보 없음"

        usage_data = {
            "voice_usage": voice_usage, "voice_total": voice_total,
            "sms_usage": sms_usage, "sms_total": sms_total,
            "data_used": data_used, "data_total": data_total,
            "data_remaining": data_remaining
        }
        return usage_data
        
    except Exception as e:
        print(f"스크래핑 중 오류 발생: {e}")
        return None
    finally:
        driver.quit()