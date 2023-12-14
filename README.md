# 📖 프로젝트명 

### ✔️ 가족 유대감 형성을 위한 라이프로깅 SNS '우리가족섬'
(메타버스 아카데미 2기 최종 프로젝트 기획/AI/서버/유니티/3D모델링 융합 팀 프로젝트)

![image](https://github.com/WooriIsland/AI/assets/115389344/ced0ff5b-e4d2-45b0-96b0-221acab0e8a7)

# 📃 프로젝트 소개

### ✔️ GPT-4-Vision/Langchain (AI 앨범) 과 GPT-4-1106-Preview/Langchain (챗봇)을 활용한 Unity 3D 엔진 기반의 메타버스 라이프로깅 SNS '우리가족섬' 프로젝트입니다.

- 사이좋은 가족을 위한 메타버스 라이프로깅 SNS
우리가족섬은 가족 구성원의 위치와 일정을 공유하고 함께한 추억들을 기록하는 메타버스 SNS입니다. 우리의 목표는 일상을 공유하여 가족 간의 유대감 형성을 돕고 가족 간의 소통이 더욱 즐거워지도록 돕는 것입니다.

[2014년 우리나라 국민 4명중 1명 척추질환으로 진료받아, 국민건강보험공단, 2015.11.26](https://www.hira.or.kr/bbsDummy.do?pgmid=HIRAA020041000100&brdScnBltNo=4&brdBltNo=9054)<br>
[척추질환 환자 증가, 건강보험심사평가원, 2022.12.01](https://www.xn--989a170ahhpsgb.com/15/?q=YToyOntzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjtzOjQ6InBhZ2UiO2k6MTMzO30%3D&bmode=view&idx=13580562&t=board)

# 👩‍🔧 팀원 소개 및 역할

### ✔️ 팀원 및 분장
- 메타버스 아카데미 2기 기획/서버/AI 총 8명
- 팀명 : 척추적 60분
  
🔹기획<br>
황해솔 : 기획 / PM<br>
이시온 : 기획 / 디자인

🔹서버<br>
정지원 : 챗봇 통신 / 알림 / 추천<br>
남효정 : 로그인 / 커뮤니티<br>
안희찬 : 프론트 엔드

🔹AI<br>
김우정 : 대표 캐릭터 디자인 / 애니메이션 적용<br>
임정민 : 챗봇 구축 / LDA 댓글 분석<br>
오수종 : 자세 감지 / 추천 시스템 

### ✔️ AI 세부 역할 분담

- 김우정
1) VideoTo3dPoseAndBvh 라이브러리, Animated Drawings 오픈 소스 활용 캐릭터 모션 적용
2) 대표 캐릭터 '레톤이' 디자인 협업 및 검수

- 임정민
1) LangChain / ChatGPT API 활용 챗봇 구축
2) 유사 서비스 'Forest' 리뷰 LDA 분석   

- 오수종
1) MediaPipe 활용 거북목 / 비대칭 / 기대앉기 / 졸음 감지
2) ML PipeLine 활용 개인화 추천 시스템 구현 

# 📅프로젝트 진행 기록

### ✔️ 수행 기간
- 2023.09.04 ~ 2023.09.27

### ✔️ AI 세부 진행 기록

[세부 일정 GitHub Projects (Start/End)](https://github.com/orgs/SpineTracker60/projects/8/views/2)

- 23-09-04 ~ 23-09-06 : 기획/서버/AI 전공별 자기소개 및 팀빌딩
- 23-09-07 ~ 23-09-08 : 아이디어 기획 및 주제 브레인스토밍/토의
- 23-09-11 : 자세 교정 서비스 '척추의 요정' 필수 기술 요구 사항 분석 (자세 감지: 1.거북목 2.비대칭 3.기대앉기 4.졸음 , 챗봇: 1.시스템 안내 2.스트레칭 방법 3.제품 추천)
- 23-09-12 : MediaPipe 활용 자세 감지 모듈 개발(1) , LangChain 활용법 학습 및 서치 
- 23-09-13 : GPT 3.5 Turbo + LangChain 활용 챗봇 구축(1), MediaPipe 활용 자세 감지 모듈 개발(2), Animated Drawings(캐릭터 애니메이션) 오픈 소스 코드 리뷰(1)
- 23-09-14 : GPT 3.5 Turbo + LangChain 활용 챗봇 구축(2), Animated Drawings(캐릭터 애니메이션) 오픈 소스 코드 리뷰(2), 챗봇 프로토 타입 테스트
- 23-09-15 : Flask 활용 챗봇 서빙 모듈 개발 및 통신 테스트(Flask - Node.js), 1주차 기획/서버/AI 전공별 진행상황 보고 및 회의
- 23-09-16 : 중간발표 플로우 설계, Figma 활용 PPT/대본 작성
- 23-09-18 : 팀별 중간발표 및 강사/멘토 피드백, 피드백 기반 팀 회의
- 23-09-19 : Gradio 기반 챗봇 테스트 모듈 개발, 제품 추천 Mock-UP 데이터 구축, VideoTo3dPoseAndBvh 활용 모션 BVH 좌표 추출 모듈 개발(1)
- 23-09-20 : ML PipeLine (LR/RF/SVD/KNC/GBM) 기반 추천 시스템 모듈 개발, 챗봇 프롬프트 수정 및 성능 고도화(1), VideoTo3dPoseAndBvh 활용 모션 BVH 좌표 추출 모듈 개발(2)
- 23-09-21 : 제품 추천 시스템 챗봇 연동, 대표 캐릭터 초안 디자인
- 23-09-22 : 2주차 기획/서버/AI 전공별 진행상황 보고 및 회의, 대표 캐릭터 애니메이션 적용 모듈 개발(1)
- 23-09-25 : 유사 서비스 'Forest' 서비스 댓글 LDA 분석, 챗봇 프롬프트 수정 및 성능 고도화(2), 대표 캐릭터 애니메이션 적용 모듈 개발(2)
- 23-09-26 : 최종 발표 플로우 설계(서비스 중심), 서비스 시연 GIF 편집, AI 전공 PPT/대본 작성, 10분 발표 리허설 
- 23-09-27 : 최종 발표 및 팀 회식, 깃허브 리드미 작성

# 💡 주요 내용

### ✔️ 유사 서비스 'Forest' 어플 구글 플레이스토어 리뷰 LDA 분석

##### 1) 'Forest' 서비스란?

![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/f42a30d9-27ef-4169-9513-9a1312eb6449)

- 집중 시간을 측정하고 종료 알림해주는 스케줄 관리 타이머 서비스
- 집중에 성공하면 유저 자신만의 숲을 가꿀 수 있는 재미요소 가미
- 본 자세 교정 서비스와 유사한 맥락의 서비스로 벤치마킹 시도

##### 2) Forest 구글 플레이 스토어 리뷰 크롤링

- 총 1240개 리뷰 내용/평점 데이터 수집
  
![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/57b3f01d-a771-408a-bad9-e929375a2125)

##### 3) LDA 활용 토픽 모델링 / 시각화

![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/893662d3-7afd-43c4-8d00-88fbfafc89e1)

- 토픽 갯수 3종류 (n_component=3) 기준 토픽 분류
1) Topic #1 : 집중력 향상 / 성취감 / 나무,숲 재미요소
2) Topic #2 : 결제 문의 / 프리미엄 유저    
3) Topic #3 : 기능 오류 / 개선점

##### 4) LDA 인사이트 도출

- 긍정적인 반응을 보인 Topic #1 토픽 분석

  ![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/8905bc78-24ba-4558-8265-f146427b3805)

- 긍정적으로 평가한 리뷰들 중 대부분 집중력 향상과 더불어 나무를 심고 숲을 가꾸는 재미요소에 몰입 / 시너지 효과
- 이러한 실제 유저 반응들을 토대로 시각적 재미(캐릭터 애니메이션)을 적용한 자세 교정 서비스를 기획/개발에 근거

### ✔️ MediaPipe 활용 자세 감지

##### 1) 요구사항 

- '척추의 요정' 서비스의 기본이 되는 거북목 / 비대칭 자세 / 기대 앉기 / 졸음 감지 모듈 개발
  
##### 2) 자세 구분

🔹서비스 사용 시 촬영한 정자세 사진 기준을 통해 비교/구분

![KakaoTalk_20230917_123027747](https://github.com/SpineTracker60/ai-model-server/assets/115389344/206337c1-75bd-440d-a80d-d04ff302321d) ![KakaoTalk_20230917_123027747_01](https://github.com/SpineTracker60/ai-model-server/assets/115389344/f05a305f-af6f-4d1c-a36a-9fb3af762166)

- 거북목 : 정자세 기준 일정 비율 이상 얼굴 크기 확장 시 탐지
- 비대칭 자세 : 어깨 좌표 기울기 이상치 탐지
- 기대 앉기 : 정자세 기준 얼굴 크기 일정 비율 이상 감소 시 탐지
- 졸음 : 눈커플 좌표 y축(위아래 길이) 기준 축소 시 탐지

### ✔️ ChatGPT API + LangChain 활용 '레톤이' 챗봇

- GPT 3.5 Turbo 모델 활용
-  LangChain 모델 중 대화에 특화된 ChatOpenAI(LMM 모델)활용
- ChatPromptTemplate(프롬프트 템플릿) 활용
- 최소 두어절 ~ 세어절 등 적은 입력 단위에 기반하여 전체 대화 내역을 기억하는 ConversationBufferMemory 활용

##### 1) 챗봇 역할

- 시스템 안내 : 신규 유저들을 위한 서비스 안내 질의응답
- 스트레칭 정보 제공 : 장기간 업무/작업을 하는 유저들을 위한 목/허리/손목 스트레칭 정보 전달
- 제품 추천 : 성별 / 나이 / 직업 / 자세 데이터( 거북목, 비대칭, 기대앉기, 졸음 수치) 기반 개인화 제품 추천
- 기타 일상 대화

##### 2) 프롬프트 엔지니어링

- Persona Pattern : '척추의 요정'서비스의 친절한 챗봇이라는 역할/이름/성격 부여
- Task : 유저들의 입력에 친절히 답변해주는 역할, 최우선적으로 사용자의 입력이 상품 추천인지/아닌지 의도를 분류하는 역할 명시
- Examples : 사용자들이 입력할 수 있는 시스템 안내 /스트레칭 방법 /상품 추천 문답 예시 명시
- Format : 20글자 이내의 간단한 답변 형식/길이 반환 형식 정의
- Tone : 절친한 친구 말투 / 이모티콘 다수 사용 등 답변 스타일 명시

![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/190e96c8-8386-411f-b4e8-dc2dda6cbc33)

##### 3) 챗봇 테스트 모듈 개발 

- 동일한 질문에 대한 다양한 표현방식(Utterance) 테스트를 위한 Gradio 기반 모듈 개발
- 테스트 질문 답변 데이터를 저장하여 프롬프트 고도화에 활용

![ezgif com-resize](https://github.com/SpineTracker60/ai-model-server/assets/115389344/22a44e95-4e53-48b7-92b6-32a1b3d71fd8)![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/85c3a03d-942b-4ca2-aef5-675d75d57bb4)

##### 4) 챗봇 구현 예시 및 통신

- 시스템 안내와 개인화 상품 추천에 대한 예시입니다.
  
![ezgif com-resize (1)](https://github.com/SpineTracker60/ai-model-server/assets/115389344/b30e4dff-574c-4efc-853d-da24b1799ab4)![ezgif com-resize (4)](https://github.com/SpineTracker60/ai-model-server/assets/115389344/b75709b1-f208-4f82-bafe-946cd13f2033)


### ✔️ ML PipLine을 활용한 개인화 상품 추천 시스템

##### 1) 개요

- 회원가입 시 입력된 성별 / 나이 / 직업 데이터
- 서비스 사용에 따라 누적되는 거북목 / 비대칭 자세 / 기대앉기 / 졸음 데이터

![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/d783cf94-ff1d-432f-9d16-4277d075e99d)

- 위 데이터를 기반으로 자세 교정에 도움이 될 수 있는 의자, 책상, 마우스 등의 사무 상품 추천 시스템
- 본 프로젝트에서는 10000개의 Mock-Up 데이터를 직접 생성하여 적용하고 실제 서비스 사용에 따라 발생하는 새 데이터 병합하는 것으로 계획

##### 2) 활용 Machine Learning 모델

- LinearRegression(LR) / RandomForest(RF) / Singular Value Decomposition(SVD) / K-Nearest Neighbors (KNN) / XGBoostClassificier(XGBM)
- 서비스 운영에 따라 최초 구성된 10000만개 데이터에 새로운 데이터 추가
- 일주일/한달 단위 갱신된 새 데이터에 따라 적합한 ML 아키텍처가 상이
- 이에 따라 갱신된 데이터별 최적의 정확도를 가진 모델 적용을 자동화시키기 위해 ML PipeLine을 구축
  
![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/c5db3380-f838-4209-9162-274df7941a9f)

- 개인에 적합한 최적화 추천을 통해 유저 만족도를 향상시키고 비즈니스 모델 고도화를 도모
  
### ✔️ 대표 캐릭터 '레톤이' 애니메이션 적용

##### 1) 서비스 대표 캐릭터 '레톤이'

- Forest 리뷰 LDA 분석에 입각한 서비스 재미요소 대표 캐릭터 디자인

![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/61d9b3f1-e38c-4f26-9562-b4ef5b22e8da)

##### 2) 시각적 재미요소를 위한 애니메이션 적용

- VideoTo3dPoseAndBVH 활용 BVH(3D 모션 좌표) 추출
- 사람이 움직이는 영상 입력, 이후 구조와 프레임별 리깅데이터가 있는 BVH파일로 변환 

![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/e28515ff-7880-4510-a23e-1100941d5778)

![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/32d5ba10-46e8-4ac8-991d-1bddcc7d01f7)

- Animated Drawings (META 오픈 소스) 활용 
- 애니메이션 데이터 BVH파일 +  사람 형상의 캐릭터 데이터  
- 이미지에서 사람 형상 인식 및 적용
- 3D 모션에 따른 2d 이미지 변형을 진행 -> 움직이는 캐릭터 GIF 출력

![image](https://github.com/SpineTracker60/ai-model-server/assets/115389344/0f9b61ed-5e95-44f8-884e-ee361a722a23)

![KakaoTalk_20230926_232107942](https://github.com/SpineTracker60/ai-model-server/assets/115389344/c7e710be-aa05-4742-ae6c-1921027cfec1)

# 🛠 기술 스택

### 🔹 언어
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">

### 🔹 주요 라이브러리
<img src="https://img.shields.io/badge/mediapipe-23C8D2?style=for-the-badge&logo=mediapipe&logoColor=white"> <img src="https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=white">  <img src="https://img.shields.io/badge/langchain-EC1C24?style=for-the-badge&logo=langchain&logoColor=white"> <img src="https://img.shields.io/badge/konlpy-2C5BB4?style=for-the-badge&logo=konlpy&logoColor=white"> <img src="https://img.shields.io/badge/scikit learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"> <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"> <img src="https://img.shields.io/badge/VideoTo3dPoseAndBVH-A5915F?style=for-the-badge&logo=VideoTo3dPoseAndBVH&logoColor=white"> <img src="https://img.shields.io/badge/Animated Drawings-0467DF?style=for-the-badge&logo=META&logoColor=white"> <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white"> <img src="https://img.shields.io/badge/gradio-F08705?style=for-the-badge&logo=gradio&logoColor=white">

### 🔹 개발 툴
<img src="https://img.shields.io/badge/VS code-2F80ED?style=for-the-badge&logo=VS code&logoColor=white"> <img src="https://img.shields.io/badge/Google Colab-F9AB00?style=for-the-badge&logo=Google Colab&logoColor=white"> <img src="https://img.shields.io/badge/pycharm-000000?style=for-the-badge&logo=pycharm&logoColor=white">

### 🔹 협업 툴
<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"> <img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white"> <img src="https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=Figma&logoColor=white"> 

# 🔍 참고 자료

### ✔️ 시연 영상 / 블로그
- 시연 영상 : [데스크 워커를 위한 자세 교정 서비스 '척추의 요정' (3)](https://velog.io/@min0731/%EB%8D%B0%EC%8A%A4%ED%81%AC-%EC%9B%8C%EC%BB%A4%EB%A5%BC-%EC%9C%84%ED%95%9C-%EC%9E%90%EC%84%B8-%EA%B5%90%EC%A0%95-%EC%84%9C%EB%B9%84%EC%8A%A4-%EC%B2%99%EC%B6%94%EC%9D%98-%EC%9A%94%EC%A0%95-3)
- Velog : [데스크 워커를 위한 자세 교정 서비스 '척추의 요정' (1)](https://velog.io/@min0731/%EB%8D%B0%EC%8A%A4%ED%81%AC-%EC%9B%8C%EC%BB%A4%EB%A5%BC-%EC%9C%84%ED%95%9C-%EC%9E%90%EC%84%B8-%EA%B5%90%EC%A0%95-%EC%84%9C%EB%B9%84%EC%8A%A4-%EC%B2%99%EC%B6%94%EC%9D%98-%EC%9A%94%EC%A0%95-1)
  
### ✔️ 기사

- https://www.hira.or.kr/bbsDummy.do?pgmid=HIRAA020041000100&brdScnBltNo=4&brdBltNo=9054
- https://www.xn--989a170ahhpsgb.com/15/?q=YToyOntzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjtzOjQ6InBhZ2UiO2k6MTMzO30%3D&bmode=view&idx=13580562&t=board

### ✔️ 오픈소스 (GitHub)

- https://github.com/pinecone-io/examples/blob/master/learn/generation/openai/fine-tuning/gpt-3.5-agent-training/00-fine-tuning.ipynb
- https://github.com/HW140701/VideoTo3dPoseAndBvh
- https://github.com/facebookresearch/AnimatedDrawings

### ✔️ 라이브러리 공식 문서

- https://www.langchain.com/
- https://openai.com/blog/gpt-3-5-turbo-fine-tuning-and-api-updates
