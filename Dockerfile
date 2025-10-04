# Dockerfile

# 1. 파이썬 3.9 버전을 기반으로 시작
FROM python:3.9

# 2. 크롬 브라우저 설치에 필요한 패키지 및 크롬 브라우저 설치
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# 3. 작업 폴더 설정
WORKDIR /app

# 4. 파이썬 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 프로젝트 파일 복사
COPY . .

# 6. gunicorn을 사용해 웹 서버 실행 (Render는 기본적으로 10000번 포트를 사용)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]