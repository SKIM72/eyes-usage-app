# Dockerfile (최종 수정본)

# 1. 파이썬 3.9 표준 버전을 기반으로 시작
FROM python:3.9

# 2. 크롬 브라우저 설치 (apt-key를 사용하지 않는 최신 방식)
RUN apt-get update && apt-get install -y \
    gnupg \
    wget \
    # Google Chrome의 GPG 키를 다운로드하고 저장
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-archive-keyring.gpg \
    # Google Chrome 저장소를 시스템에 추가
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-archive-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    # 패키지 목록을 다시 업데이트하고 크롬 설치
    && apt-get update \
    && apt-get install -y google-chrome-stable

# 3. 작업 폴더 설정
WORKDIR /app

# 4. 파이썬 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 프로젝트 파일 복사
COPY . .

# 6. gunicorn을 사용해 웹 서버 실행
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]