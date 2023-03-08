# OneManChallenge_Crawler
프로젝트용 IT 뉴스 기사 수집 크롤러

## 1. 기술스택
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> Beautifulsoup4 

## 2. 크롤링 참고사항
- (처벌)상대방 서비스 지장 없도록 진행
- (처벌)크롤링한 data 상업적 사용 금지 ⇒ 영리성 목적이 없으면 괜찮음(항해99 매니저님 말씀)
- 출처 표기(readme 등)
- robots.txt Allow 체크
- 크롤링 항목 없는 경우 Default값 처리

## 3. 크롤링 목적 및 대상
- 크롤링 목적 : 항해99 챌린지팀 실전 프로젝트 학습용
- 크롤링 대상 : IT 관련 뉴스기사
- 수집항목 : (뉴스) 제목, 내용 미리보기, 등록날짜 섬네일URL, 메인기사URL

## 4. 크롤링 전략
- 크롤링 과정 : Local data 수집 → csv 추출 → 클라우드 DB서버로 저장
- 크롤링 차단 대응 : sleep() 와 같은 일시정지 기능 활용하여 방화벽 차단 대응
- 크롤링 수집 노드 : 개인 PC 활용

## 5. 현재 수집된 총 데이터 개수 : 30만건, 사이트 3곳
- 1일 약 10만건 ⇒ 100만건 예상 일수 : 10일
