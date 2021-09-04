# sonmari
수어 번역 프로그램입니다.

# 프로젝트 소개
수어를 한국어로 번역해주는 병원용 수어 번역 프로그램을 개발한다. 컴퓨터 카메라에 수어 동작을 비추면 해당되는 한국어를 출력해주는 것이다. 
예를 들면 ‘설사’, ‘감기’, ‘콧물’ 등의 수어 동작을 카메라에 비추면, 이 모션을 인식하여 해당 의미의 한국어로 화면에 출력해준다. 또한 이 프로그램에서는 '리셋' 동작을 별도로 지정해두었다. 사용자가 '리셋' 동작을 취할 때까지 출력된 단어들을 화면 위에 모두 보여주어, 문장 수준의 이해가 가능하도록 했다.
이로써 의사가 청각장애인의 수어 동작을 이해할 수 있게 되고, 진료에 도움을 줄 수 있을 것이다.

# 필요 하드웨어
<img src="https://user-images.githubusercontent.com/74365895/132035599-0b286730-bd4e-4b04-8e50-c774215b6876.jpg"  width="800" height="400">

GPU가 내장된 노트북 한대와 수어 동작을 촬영하는 웹캠이 필요하다.

# 사용 방법
손마리의 사용자는 의사와 환자이며 진료를 시작한 의사가 환자에게 질문을 한다. 가령 '어디가 아프세요'와 같은 질문이다.
다음으로 이 질문을 들은 농인 환자가 카메라에 대고 수어로 말한다. 그러면 손마리 프로그램이 해당 수어 동작을 인식하여 한국어로 번역한 뒤 의사 화면에 출력한다.
이 때 '리셋'동작을 미리 지정해두었고, 환자가 '리셋'동작을 취할 때까지 출력된 단어들을 화면 위에 모두 보여준다.

<img src="https://user-images.githubusercontent.com/74365895/132082420-573b5459-bdbd-4ee7-b9ad-afab2ce75651.gif"  width="800" height="450">


# 시연 영상

<유튜브 URL>

# 필요 기술
RNN과 CNN의 결합으로 동적인 영상에 대한 번역을 구현한 경우 속도가 느리거나 실시간이 아니라는 한계가 있다. '빠른 속도를 내면서도 영상을 번역할 수는 없을까?'라는 고민을 하게 되었고 그 과정에서 빠른 속도로 실시간 객체 탐지를 제공하는 YOLO를 찾게 되었다.
YOLO는 실시간으로 매우 빠른 속도의 이미지에 대한 번역을 제공하는 오픈소스 툴이다. 기존의 R-CNN과 달리 합성곱 신경망을 단 한번 통과 시키고, 이로 인해 속도가 매우 빠르고 실시간에 용이하다는 장점이 있다.

<img src="https://user-images.githubusercontent.com/74365895/120753068-977e8a80-c545-11eb-8ac1-7914844aac8c.png"  width="800" height="400">

우선 수어 동작 별로 핵심 이미지를 지정해두었고, YOLO를 이용해 모든 단어들의 핵심 이미지들을 트레이닝 시켰다.
이후 파이썬을 이용해 핵심 이미지들이 모두 인식되면 해당 단어를 출력하도록 했다.
예를 들면 쓰러지다 1과 쓰러지다 2가 순차적으로 인식이 되면 쓰러지다가 출력되도록 했다.

<img src="https://user-images.githubusercontent.com/74365895/120752859-4a9ab400-c545-11eb-9f7b-ce19e137ae6f.png"  width="800" height="400">


# 번역 단어
이틀,삼일,감기,콧물,쓰러지다,설사,예,아니,머리,배,아프다,입원,퇴원 등 총 20개 단어에 대한 번역을 제공하고, 리셋 동작을 인식해 문장을 초기화한다.

<img src="https://user-images.githubusercontent.com/74365895/132034383-fb3dbb94-402a-4e70-977f-89c9e2f481f0.jpg"  width="800" height="400">

# 데이터 구성

위 이미지를 보면 총 34개의 클래스가 있고 각 클래스 별로 최소 200 - 300장의 데이터가 필요하다. 약 10000장의 데이터를 모았고 7:1:1의 비율로 트레이닝셋, 검증셋, 테스트셋으로 나누었다.
트레이닝셋은 대부분 어두운 옷을 입고 트레이닝을 진행했고, 검증셋은 대부분 밝고 다양한 옷을 입어 YOLO의 성능을 정확히 측정하도록 했다.

<img src="https://user-images.githubusercontent.com/74365895/132083392-9f49d4c6-9ed6-4065-8f7d-f873a818c5dd.jpg"  width="400" height="400">

<img src="https://user-images.githubusercontent.com/74365895/132083394-cdf2f022-4623-4a78-befc-50c00c3341a8.jpg"  width="400" height="400">

차례대로 트레이닝셋과 검증셋이다.
라벨링은 labelImg 툴을 이용해 스탠다드하게 직사각형 모양으로 라벨링한 뒤 박스의 좌표값들에 대한 txt 파일을 저장해주었다.

<img src="https://user-images.githubusercontent.com/74365895/132083397-e37a0a14-046a-43a0-88c8-d834a1406ca7.png"  width="800" height="400">



# 트레이닝 방법
YOLO를 이용해 트레이닝하면 중간중간에 검증셋을 이용해 정확도를 측정해준다. 이에 따라 가장 성능이 좋은 가중치 파일을 선택한다.

<img src="https://user-images.githubusercontent.com/74365895/132083511-cda04b4b-128b-4daa-add1-5dd76490599d.png"  width="600" height="600">


# 최종 정확도
테스트셋에 대한 최종 정확도를 출력한 결과다.
다른 사람의 손동작을 이용해 테스트셋을 만들고 그에 따른 정확도를 클래스별로 출력했다.

<img src="https://user-images.githubusercontent.com/74365895/132083595-f0396d20-a029-46be-9089-38191b5f26cd.png"  width="640" height="692">


# reference
https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects

https://www.youtube.com/watch?v=7XLu7p8Vatg&t=16s

https://github.com/Cartucho/mAP


