# MongoDB를 활용한 기사 추천 및 컨텐츠 추천

## 소개
MongoDB를 활용한 기사 및 컨텐츠 추천 프로젝트입니다. 사용자의 관심사와 컨텐츠 특성을 기반으로 개인화된 추천을 제공합니다.

## 주요 기능
- (LLM) 텍스트 임베딩 기반 컨텐츠 유사도 분석
- 실시간 추천 시스템

## 시작하기
### 필요 조건
- Python 3.12 이상
- Conda
- MongoDB
- 필요한 Python 패키지 (requirements.txt 참조)

### 파이썬 환경 설정
```bash
# Conda 환경 생성 및 활성화
conda create -n personal-matching python=3.12
conda activate personal-matching

# 필요한 패키지 설치
pip install -r requirements.txt
```

### MongoDB 설정
1. MongoDB 서버 실행
2. 데이터베이스 및 컬렉션 생성
3. 환경 변수 설정 (.env 파일 생성)
```
MONGODB_URI=your_mongodb_connection_string
MONGODB_NAME=your_database_name
MONGODB_COLLECTION_RECOMMEND=your_database_collection_name_for_recommend
MONGODB_COLLECTION_USER=your_database_collection_name_for_user
```

### 프로그램 실행
1. 임베딩 테스트 데이터 추가
```bash
python -m scripts.execution.py
```

2. LLM 프로그램 실행
```bash
python main.py "{LLM 서치 데이터 입력}"
```

## 프로젝트 구조
```
.
├── config/
│   ├── __init__.py           #
│   ├── db.py                 # mongoDB 연결 클래스 정의
│   ├── embedding.py          # 데이터 임베딩 모델 정의 클래스
│   └── settings.py           # mongoDB 기본 연결 이름 정의
├── scripts/
│   ├── __init__.py           # 
│   ├── data_processing.py    # 임베딩 데이터 insert를 위한 함수
│   ├── execution.py          # 실행 스크립트
│   └── utils.py              # 기타 util 함수
├── services/
│   ├── __init__.py           # 
│   └── llm_recommender.py    # LLM 추천 실행 스크립트 정의
├── main.py                   # 메인 실행 파일
├── requirements.txt          # 의존성 패키지
└── README.md                 # 프로젝트 문서
```
