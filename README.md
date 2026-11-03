# 손마리 (Sonmari)

**딥러닝 기반 의료 수어 번역기** — 카메라에 수어 동작을 보여주면 한국어 문장으로 실시간 번역합니다.

**AI-powered medical sign language translator** — translates Korean Sign Language into Korean text in real time through a webcam.

<img src="https://user-images.githubusercontent.com/74365895/132082420-573b5459-bdbd-4ee7-b9ad-afab2ce75651.gif" width="800">

- 🎬 데모 영상 / Demo video: [Google Drive](https://drive.google.com/file/d/1gQuCYR1dsx_L5tSe3xyAj115FsYxC_k8/view?usp=sharing)

**[한국어](#한국어) · [English](#english)**

---

## 한국어

### 소개

병원에서 의료 수어 통역사가 부족한 상황에서도, 농인 환자가 통역사 없이 의사와 소통할 수 있도록 만든 프로그램입니다.
의사가 이 프로그램을 통해 환자의 수어를 이해할 수 있는 것을 목표로 합니다.

웹캠으로 들어온 수어 동작을 YOLOv4 모델이 인식하고, 인식된 동작들을 조합해 한국어 단어로 바꿔 화면에 문장으로 보여줍니다.
`초기화` 동작을 인식하기 전까지 번역된 단어가 이어져 간단한 문장 형태로 표시됩니다.

### 번역 가능한 단어

| 단어 | 동작 라벨 | 단어 | 동작 라벨 |
|---|---|---|---|
| 2일 | `2day` | 입원 | `hospitalization1 → 2 → 3` |
| 3일 | `3day` | 퇴원 | `hospitalization3 → 2 → 1` |
| 네 | `yes` | 완쾌 | `recovery1 → 2 → 3` |
| 아니오 | `no1 → no2` | 낫다 | `recovery3` |
| 머리 | `head` | 소화불량 | `digestion1 → 2 → poor` |
| 배 | `stomach` | 변비 | `constipation1 → 2 → 3` |
| 아프다 | `sick` | 소변 | `urine1 → urine2` |
| 쓰러지다 | `fall1 → fall2` | 약 | `medicine` |
| 감기 | `cold1 → cold2` | 수술 | `surgery1 → surgery2` |
| 콧물 | `runnynose1 → runnynose2` | 초기화 (문장 지우기) | `reset` |
| 설사 | `diarrhea1 → diarrhea2` | | |

동작이 여러 개인 단어는 핵심 동작을 순서대로 인식했을 때 번역됩니다. (총 34개 동작 클래스)

### 빠른 시작 (웹 버전)

GPU, CUDA, Visual Studio 없이 **Mac / Windows / Linux** 어디서나 CPU로 실행됩니다.

**1. 코드와 모델 받기**

```bash
git clone https://github.com/23bulgogi/sonmari.git
cd sonmari/web

# 학습된 모델 (약 256MB)
curl -L -o model/yolov4-obj_best.weights \
  https://github.com/23bulgogi/sonmari/releases/download/model-v2/yolov4-obj_best.weights
```

**2. 설치 및 실행**

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app:app --port 8000
```

브라우저에서 http://localhost:8000 을 열고 **카메라 시작**을 누르세요.

**Docker로 실행**

```bash
cd web
docker build -t sonmari .
docker run -p 8000:8000 -v "$(pwd)/model:/app/model" sonmari
```

자세한 설정(임계값, 서버 배포 시 주의사항)은 [web/README.md](web/README.md)를 참고하세요.

### 구조

```
sonmari/
├── web/                     # 웹 버전 (권장)
│   ├── app.py               # FastAPI 서버, WebSocket(/ws)으로 프레임 수신
│   ├── detector.py          # OpenCV DNN으로 YOLOv4 실행
│   ├── translator.py        # 동작 라벨 → 한국어 문장 변환
│   ├── check_model.py       # 모델 파일 점검 도구
│   ├── static/index.html    # 웹캠 화면
│   └── model/               # cfg, obj.names (+ 직접 받은 weights)
└── src/                     # 이전 Windows 데스크톱 버전 (PyQt5 + darknet)
```

**동작 방식:** 브라우저가 웹캠 프레임을 서버로 보내면 → YOLOv4가 손 동작을 검출하고 → `translator.py`가 최근 인식된 동작들의 순서를 보고 단어를 만들어 → 문장과 함께 브라우저로 돌려줍니다.

### 모델

- YOLOv4 (darknet), 입력 416×416, 34개 클래스
- 학습 설정: [`web/model/yolov4-obj.cfg`](web/model/yolov4-obj.cfg), 클래스 목록: [`web/model/obj.names`](web/model/obj.names)
- 학습 방법: [AlexeyAB/darknet — How to train to detect your custom objects](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects)

모델이 이상하게 동작하면(아무 동작에나 같은 라벨이 나오는 등) cfg와 weights가 짝이 맞는지 먼저 확인하세요.

```bash
cd web && python check_model.py
```

### 알려진 제한사항

- CPU로 실행하면 초당 약 4프레임 정도로 처리됩니다(iMac 기준). 여러 동작으로 된 단어는 동작을 천천히, 또렷하게 해야 인식이 잘 됩니다.
- 일부 동작(예: 수술)은 인식률이 낮습니다. 화면의 **좌우 반전해서 인식** 옵션을 켜면 나아질 수 있습니다.
- 조명, 배경, 카메라와의 거리가 학습 데이터와 다르면 정확도가 떨어집니다.
- 서버에 배포할 경우 브라우저는 HTTPS에서만 카메라를 허용합니다.
- 같은 단어는 문장에 한 번만 표시됩니다.

### 이전 데스크톱 버전 (Windows)

PyQt5 + darknet DLL 기반의 Windows 데스크톱 버전은 [`desktop-version`](https://github.com/23bulgogi/sonmari/tree/desktop-version) 브랜치에 보존되어 있습니다.
Visual Studio, CMake, OpenCV 빌드가 필요하고 GPU 사용 시 CUDA 10.2 / cuDNN 7이 필요해 설치가 까다롭습니다. 새로 시작한다면 웹 버전을 권장합니다.
당시의 빌드 가이드는 해당 브랜치의 [README](https://github.com/23bulgogi/sonmari/blob/desktop-version/README.md)에 있습니다.

### 기여하기

[CONTRIBUTING.md](CONTRIBUTING.md)를 참고해 주세요. 이 프로젝트에 참여하는 모든 분은 [행동 강령](CODE_OF_CONDUCT.md)을 따릅니다.

---

## English

### About

Sonmari was built for hospitals where medical sign language interpreters are scarce. It aims to let Deaf patients communicate with doctors without an interpreter, so that doctors can understand their patients' signs through the program.

A YOLOv4 model recognizes signs captured by the webcam, combines the recognized gestures into Korean words, and displays them as a sentence.
Translated words keep accumulating into a simple sentence until the `reset` gesture is recognized.

### Supported words

| Korean | Meaning | Gesture labels | Korean | Meaning | Gesture labels |
|---|---|---|---|---|---|
| 2일 | 2 days | `2day` | 입원 | Hospitalization | `hospitalization1 → 2 → 3` |
| 3일 | 3 days | `3day` | 퇴원 | Discharge | `hospitalization3 → 2 → 1` |
| 네 | Yes | `yes` | 완쾌 | Full recovery | `recovery1 → 2 → 3` |
| 아니오 | No | `no1 → no2` | 낫다 | Get better | `recovery3` |
| 머리 | Head | `head` | 소화불량 | Indigestion | `digestion1 → 2 → poor` |
| 배 | Stomach | `stomach` | 변비 | Constipation | `constipation1 → 2 → 3` |
| 아프다 | Sick / hurts | `sick` | 소변 | Urine | `urine1 → urine2` |
| 쓰러지다 | Collapse | `fall1 → fall2` | 약 | Medicine | `medicine` |
| 감기 | Cold | `cold1 → cold2` | 수술 | Surgery | `surgery1 → surgery2` |
| 콧물 | Runny nose | `runnynose1 → runnynose2` | 초기화 | Reset (clear sentence) | `reset` |
| 설사 | Diarrhea | `diarrhea1 → diarrhea2` | | | |

Words made of multiple gestures are translated when their key gestures are recognized in order. (34 gesture classes in total)

### Quick start (web version)

Runs on the CPU on **macOS / Windows / Linux** — no GPU, CUDA, or Visual Studio required.

**1. Get the code and the model**

```bash
git clone https://github.com/23bulgogi/sonmari.git
cd sonmari/web

# Trained model (~256 MB)
curl -L -o model/yolov4-obj_best.weights \
  https://github.com/23bulgogi/sonmari/releases/download/model-v2/yolov4-obj_best.weights
```

**2. Install and run**

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app:app --port 8000
```

Open http://localhost:8000 in your browser and click **카메라 시작 (Start camera)**.

**Run with Docker**

```bash
cd web
docker build -t sonmari .
docker run -p 8000:8000 -v "$(pwd)/model:/app/model" sonmari
```

See [web/README.md](web/README.md) (Korean) for configuration options and deployment notes.

### Project structure

```
sonmari/
├── web/                     # Web version (recommended)
│   ├── app.py               # FastAPI server; receives frames over WebSocket (/ws)
│   ├── detector.py          # Runs YOLOv4 with OpenCV DNN
│   ├── translator.py        # Gesture labels → Korean sentence
│   ├── check_model.py       # Model file checker
│   ├── static/index.html    # Webcam UI
│   └── model/               # cfg, obj.names (+ weights you download)
└── src/                     # Legacy Windows desktop version (PyQt5 + darknet)
```

**How it works:** the browser sends webcam frames to the server → YOLOv4 detects the hand gesture → `translator.py` looks at the order of recently recognized gestures to form a word → the word and the sentence are sent back to the browser.

### Model

- YOLOv4 (darknet), 416×416 input, 34 classes
- Config: [`web/model/yolov4-obj.cfg`](web/model/yolov4-obj.cfg), class list: [`web/model/obj.names`](web/model/obj.names)
- Training guide: [AlexeyAB/darknet — How to train to detect your custom objects](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects)

If the model behaves strangely (e.g. the same label for every gesture), first check that the cfg and weights match:

```bash
cd web && python check_model.py
```

### Known limitations

- On the CPU it processes about 4 frames per second (measured on an iMac). Perform multi-gesture words slowly and clearly.
- Some gestures (e.g. surgery) have low recognition rates. Turning on the **좌우 반전해서 인식 (mirror input)** option may help.
- Accuracy drops when lighting, background, or distance from the camera differ from the training data.
- When deployed to a server, browsers only allow camera access over HTTPS.
- Each word appears only once in a sentence.

### Legacy desktop version (Windows)

The Windows desktop version based on PyQt5 and the darknet DLL is preserved in the [`desktop-version`](https://github.com/23bulgogi/sonmari/tree/desktop-version) branch.
It requires building Visual Studio, CMake, and OpenCV, plus CUDA 10.2 / cuDNN 7 for GPU use, so setup is difficult. The web version is recommended for new users.
The original build guide is in that branch's [README](https://github.com/23bulgogi/sonmari/blob/desktop-version/README.md).

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Everyone participating in this project is expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 만든 사람들 / Contributors

whogodemo · Minju Ko · Jeongin Bae · bjin28 · Jeongkyu Shin

## 라이선스 / License

[MIT License](LICENSE)
