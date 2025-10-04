from flask import Flask, render_template
from scraper import get_usage_data 
import time

app = Flask(__name__)

@app.route("/")
def show_usage():
    """
    메인 페이지 접속 시 스크래핑 함수를 실시간으로 호출하고,
    결과를 HTML 템플릿에 담아 사용자에게 보여줍니다.
    """
    print("사용량 데이터 조회를 시작합니다...")
    scraped_data = get_usage_data() 
    print(f"조회 결과: {scraped_data}")
    
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')

    return render_template('index.html', data=scraped_data, updated_time=current_time)

if __name__ == "__main__":
    # 이 부분은 로컬 테스트 시에만 사용됩니다.
    app.run(host='0.0.0.0', port=8080, debug=True)