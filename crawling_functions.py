# 좋아요 / 댓글
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import logging

class Crawl_Carrot():
    # Selenium WebDriver 설정 
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu') # GPU 가속 비활성화
        options.add_argument("headless") 
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--enable-unsafe-swiftshader")
        options.add_argument("--use-gl=swiftshader")  # 소프트웨어 렌더링 사용
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        options.add_experimental_option("detach", True)

        # ChromeDriver 경로 설정 (필요 시 수정)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.logger = self.setup_logger()
        
    def setup_logger(self):
        # 로깅 설정
        logger = logging.getLogger("DistrictCrawler")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger


    def get_title(self):
        # 제목을 가져오는 함수
        posts = self.driver.find_elements(By.CSS_SELECTOR, 'a.click_search_result_item')
        titles = [post.get_attribute('data-title') for post in posts]
        self.logger.info('성공 - 제목 - 데이터 수집')
        return pd.DataFrame({"title": titles})

    def get_article(self):
        # 본문 내용을 가져오는 함수
        articles = self.driver.find_elements(By.CSS_SELECTOR, 'p._588sy4192')
        article_texts = [article.text for article in articles]
        self.logger.info('성공 - 기사 - 데이터 수집')
        return pd.DataFrame({"article": article_texts})

    def get_etc(self):
        # 기타 등등의 내용을 가져오는 함수
        dongs = self.driver.find_elements(By.CSS_SELECTOR,
                                    'span._588sy418w._588sy4195._588sy41w._588sy41aw._588sy41b5._588sy42')
        dong_texts = [dong.text for dong in dongs]
        etc_data = pd.DataFrame({"etc": dong_texts[0::3]}).reset_index(drop=True)  # 3개씩 중 첫 번째
        self.logger.info('성공 - 기타 - 데이터 수집')
        return etc_data

    def get_time(self):
        # 시간을 가져오는 함수
        times = self.driver.find_elements(By.CSS_SELECTOR,
                                    'time._588sy418w._588sy4195._588sy41w._588sy41aw._588sy41b5._588sy42')
        time_texts = [time.text for time in times]
        current_time = [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * len(time_texts)
        self.logger.info('성공 - 시간 - 데이터 수집')
        return pd.DataFrame({"time": time_texts, "current_time": current_time})

    def get_like_comment(self):
        # 좋아요와 댓글을 가져오는 함수
        like_comments = self.driver.find_elements(By.CSS_SELECTOR, 'span._588sy4192._588sy41w._588sy41b2._588sy42')
        texts = [lc.text for lc in like_comments if '좋아요' in lc.text or '댓글' in lc.text]  # 필터링
        likes = texts[0::2]  # 좋아요
        comments = texts[1::2]  # 댓글
        self.logger.info('성공 - 댓글 - 데이터 수집')
        return pd.DataFrame({"like": likes, "comment": comments})
    
    # click_load_more 메서드 수정 (self.driver 사용)
    def click_load_more(self, max_clicks=2):
        click_count = 0
        while click_count < max_clicks:
            try:
                more_button = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._876es70._876es75._876es73._588sy462._588sy4r8'))
                )
                more_button.click()
                click_count += 1
                print(f"{click_count}번째 더보기 버튼 클릭 성공")
            except Exception as e:
                print(f"더 이상 더보기 버튼이 없거나 오류 발생: {e}")
                break

    def get_category_urls(self):
        """
        현재 페이지에서 카테고리 URL을 추출하는 함수.
        버튼 클릭을 대체하는 함수
        """
        self.logger.info("Extracting category URLs")
        category_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.click_filter_control.eii19e1'))
        )

        # href 추출
        category_urls = {
            element.get_attribute("data-label"): element.get_attribute("href") for element in category_elements
        }
        self.logger.info(f"Extracted URLs: {category_urls}")
        return category_urls


    def collect_data(self, district_name):
        """
        특정 구 데이터를 크롤링하는 함수.
        """
        # 데이터 수집
        try:
            # 더보기 버튼 클릭
            self.click_load_more()
            title_data = self.get_title()
            article_data = self.get_article()
            etc_data = self.get_etc()
            time_data = self.get_time()
            like_comment_data = self.get_like_comment()
        except:
            self.logger.warning('에러 - 데이터 수집 실패')
        # 데이터 병합
        try:
            district_data = pd.concat([title_data, article_data, etc_data, time_data, like_comment_data], axis=1)
            district_data["district"] = district_name  # 구 이름 추가
        except:
            self.logger.warning('에러 - 데이터 병합 실패')
        return district_data
    
    # def collect_data(self, district_name):
    #     start_time = time.time()
    #     try:
    #         self.measure_time(self.click_load_more)
    #         title_data = self.measure_time(self.get_title)
    #         article_data = self.measure_time(self.get_article)
    #         etc_data = self.measure_time(self.get_etc)
    #         time_data = self.measure_time(self.get_time)
    #         like_comment_data = self.measure_time(self.get_like_comment)
    #         district_data = pd.concat([title_data, article_data, etc_data, time_data, like_comment_data], axis=1)
    #         district_data["district"] = district_name
    #     except Exception as e:
    #         self.logger.warning(f"데이터 수집 실패: {e}")
    #         return pd.DataFrame()
    #     finally:
    #         elapsed_time = time.time() - start_time
    #         self.logger.info(f"'{district_name}' 데이터 수집 전체 시간: {elapsed_time:.2f}초")
    #     return district_data
    
    def crawl_district(self, url, district_name):
        """
        특정 구 데이터를 크롤링하는 함수.
        """
        self.driver.get(url)
        
        # 정적으로 페이지 로드 대기
        time.sleep(3)

        # 카테고리 URL 추출
        category_urls = self.get_category_urls()

        # 각 카테고리별로 URL로 이동해 데이터 크롤링
        all_category_data = pd.DataFrame()
        for category_name, category_url in category_urls.items():
            try:
                self.logger.info(f"Visiting category: {category_name}")
                self.driver.get(category_url)

                # 카테고리 페이지 로드 대기
                time.sleep(2)

                # 데이터 수집
                category_data = self.collect_data(district_name)
                category_data["category"] = category_name
                all_category_data = pd.concat([all_category_data, category_data], ignore_index=True)
            except Exception as e:
                self.logger.warning(f"Failed to collect data for category {category_name}: {e}")

        # 구 이름 추가
        all_category_data["district"] = district_name
        print(all_category_data)
        return all_category_data

    def crawl_all_districts(self, district_urls):
        """
        모든 구 데이터를 크롤링하는 함수.
        """
        all_data = pd.DataFrame()
        
        try:
            for district_name, url in district_urls.items():
                print(f"현재 구: {district_name}")
                try:
                    start_time = time.time()
                    district_data = self.crawl_district(url, district_name)
                    all_data = pd.concat([all_data, district_data], ignore_index=True)
                    elapsed_time = time.time() - start_time
                    print(f"{district_name}: {len(district_data)}개의 데이터 수집 완료 (소요 시간: {elapsed_time:.2f}초)")
                except Exception as e:
                    print(f"{district_name}: 크롤링 중 오류 발생 - {e}")
        finally:
            print(all_data)
            self.driver.quit()
            print(all_data)
        return all_data

