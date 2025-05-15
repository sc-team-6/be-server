FROM python:3.9-alpine3.13

# 필수 빌드 툴 및 패키지 설치
RUN apk add --no-cache gcc musl-dev libffi-dev \
    openssl-dev python3-dev jq

# 작업 디렉토리 생성
WORKDIR /usr/src/app

# 소스 복사
COPY . ./

# requirements.txt 생성 및 설치
RUN jq -r '.default | to_entries[] | .key + .value.version' Pipfile.lock > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# 환경변수 설정
ENV DOT_ENV=test
ENV PORT=8000
ENV TZ=UTC

# FastAPI 실행
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]