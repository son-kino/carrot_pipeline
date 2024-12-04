import pandas as pd
from crawling_functions import Crawl_Carrot
from datetime import datetime

district_urls = {
    "종로구": "https://www.daangn.com/kr/community/?in=종로구-2",
    "중구": 'https://www.daangn.com/kr/community/?in=중구-20',
    "용산구": 'https://www.daangn.com/kr/community/?in=용산구-36',
    "성동구": 'https://www.daangn.com/kr/community/?in=성동구-53',
    "광진구": 'https://www.daangn.com/kr/community/?in=광진구-71',
    "동대문구": 'https://www.daangn.com/kr/community/?in=동대문구-87',
    "중랑구": 'https://www.daangn.com/kr/community/?in=중랑구-102',
    "성북구": 'https://www.daangn.com/kr/community/?in=성북구-119',
    "강북구": 'https://www.daangn.com/kr/community/?in=강북구-140',
    "도봉구": 'https://www.daangn.com/kr/community/?in=도봉구-154',
    "노원구": 'https://www.daangn.com/kr/community/?in=노원구-169',
    "은평구": 'https://www.daangn.com/kr/community/?in=은평구-189',
    "서대문구": 'https://www.daangn.com/kr/community/?in=서대문구-206',
    "마포구": "https://www.daangn.com/kr/community/?in=마포구-221",
    "양천구": "https://www.daangn.com/kr/community/?in=양천구-238",
    "강서구": "https://www.daangn.com/kr/community/?in=강서구-257",
    "구로구": "https://www.daangn.com/kr/community/?in=구로구-278",
    "금천구": "https://www.daangn.com/kr/community/?in=금천구-294",
    "영등포구": "https://www.daangn.com/kr/community/?in=영등포구-305",
    "동작구": "https://www.daangn.com/kr/community/?in=동작구-324",
    "관악구": "https://www.daangn.com/kr/community/?in=관악구-340",
    "서초구": "https://www.daangn.com/kr/community/?in=서초구-362",
    "강남구": "https://www.daangn.com/kr/community/?in=강남구-381",
    "송파구": "https://www.daangn.com/kr/community/?in=송파구-404",
    "강동구": "https://www.daangn.com/kr/community/?in=강동구-432"
}

# 크롤링 시작
if __name__ == "__main__":
    # Crawl_Carrot 클래스 인스턴스 생성
    carrot_client = Crawl_Carrot()
    
    try:
        # 모든 구 데이터 크롤링
        current_time = datetime.now().strftime("%Y-%m-%d_%H")
        data = carrot_client.crawl_all_districts(district_urls)

        # 데이터 저장
        data.to_csv(f"data/crawling_{current_time}.csv", index=False, encoding="utf-8-sig")
        print("크롤링 완료: 데이터가 'all_district_data.csv'에 저장되었습니다.")
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
    finally:
        carrot_client.close()  # 드라이버 