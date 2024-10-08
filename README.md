# KERT 웹 정적 API 서버

- 실제 API 서비스와 연결하기 위해 FE개발에 임시로 사용하는 정적 서버입니다.
- ~~사실 혼자 대시보드 기능 개발할 때 쓰려고 만든 거~~

## 서버 실행

- 윈도우 파워셸 기준입니다.

0. 아래 명령어를 입력하여 Repo를 복제합니다.

```shell
git clone https://github.com/whitedev7773/KERT-WEB-STATIC-API
cd KERT-WEB-STATIC-API
```

1. 만약 clone 후 처음 실행하면 venv 가상환경 구축

```shell
python -m venv venv
```

```shell
./venv/Scripts/activate.ps1
```

2. FastAPI & Uvicorn 설치

```shell
pip install FastAPI uvicorn["standard"]
```

3. 서버 실행

```shell
uvicorn main:app --reload
```

4. API 문서 확인

- FastAPI는 자동으로 Swagger 기반의 API 문서가 작성됩니다.
- (API 요청) http://localhost:8000
- (API 문서) http://localhost:8000/docs

## 구현된 정적 API

- 서버 요청 시 0~2초 사이의 의도적인 통신 지연
- 연혁 전체 조회
- 연혁 추가
- 연혁 제거

## 라이브러리

- FastAPI
- Uvicorn
