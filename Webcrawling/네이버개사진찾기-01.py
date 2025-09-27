import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve

# 다운로드 폴더 생성
if not os.path.exists('dogs'):
    os.makedirs('dogs')

# 1. 웹 드라이버 설정 (Safari 사용)
driver = webdriver.Safari()

# 2. 네이버 이미지 검색 페이지 접속
driver.get('https://www.naver.com')
time.sleep(3)  # 페이지 로딩 시간을 충분히 줍니다.

# 3. 검색어 입력 및 검색
search_box = driver.find_element(By.ID, 'query')
search_box.send_keys('개')
search_box.send_keys(Keys.RETURN)
time.sleep(3)  # 검색 결과 로딩 시간을 충분히 줍니다.

# 4. 이미지 탭 클릭
try:
    image_tab = driver.find_element(By.LINK_TEXT, '이미지')
    image_tab.click()
    time.sleep(3)  # 이미지 탭 페이지 로딩 시간을 충분히 줍니다.
except Exception as e:
    print(f"이미지 탭을 찾을 수 없습니다: {e}")
    driver.quit()
    exit()

# 5. 이미지 URL 수집
img_urls = []
scroll_count = 0
while scroll_count < 10:  # 스크롤 횟수를 더 늘려서 더 많은 이미지를 로드합니다.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 스크롤 후 이미지 로드 시간을 줍니다.

    # CSS 선택자 변경 (네이버의 현재 구조에 맞게)
    images = driver.find_elements(By.CSS_SELECTOR, 'img.tile_item._fe_image_tab_photo_item')

    for image in images:
        try:
            # src 속성을 먼저 확인
            url = image.get_attribute('src')
            # src 속성이 없으면 data-src 속성 확인
            if not url:
                url = image.get_attribute('data-src')

            if url and url.startswith('https://'):
                img_urls.append(url)
        except Exception as e:
            print(f"이미지 URL 가져오기 실패: {e}")

    scroll_count += 1

# 중복 URL 제거
img_urls = list(set(img_urls))
print(f"총 {len(img_urls)}개의 이미지 URL을 찾았습니다.")

# 6. 이미지 다운로드
for i, url in enumerate(img_urls):
    try:
        filename = f"dogs/dog_{i + 1}.jpg"
        urlretrieve(url, filename)
        print(f"이미지 {i + 1} 다운로드 완료: {filename}")
    except Exception as e:
        print(f"이미지 다운로드 실패: {e}")

# 7. 웹 드라이버 종료
driver.quit()