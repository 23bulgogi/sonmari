# 손마리 (Sonmari)

**딥러닝 기반 의료 수어 번역기** — 카메라에 수어 동작을 보여주면 한국어 문장으로 실시간 번역합니다.

Open-source Korean Sign Language translator for hospitals, using a YOLOv4 model.

<img src="https://user-images.githubusercontent.com/74365895/132082420-573b5459-bdbd-4ee7-b9ad-afab2ce75651.gif" width="800">

- 🎬 데모 영상: [Google Drive](https://drive.google.com/file/d/1gQuCYR1dsx_L5tSe3xyAj115FsYxC_k8/view?usp=sharing)

---

## 소개

병원에서 의료 수어 통역사가 부족한 상황에서도, 농인 환자가 통역사 없이 의사와 소통할 수 있도록 만든 프로그램입니다.
의사가 이 프로그램을 통해 환자의 수어를 이해할 수 있는 것을 목표로 합니다.

웹캠으로 들어온 수어 동작을 YOLOv4 모델이 인식하고, 인식된 동작들을 조합해 한국어 단어로 바꿔 화면에 문장으로 보여줍니다.
`초기화` 동작을 인식하기 전까지 번역된 단어가 이어져 간단한 문장 형태로 표시됩니다.

## 번역 가능한 단어

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

---

## 빠른 시작 (웹 버전)

GPU, CUDA, Visual Studio 없이 **Mac / Windows / Linux** 어디서나 CPU로 실행됩니다.

### 1. 코드와 모델 받기

```bash
git clone https://github.com/23bulgogi/sonmari.git
cd sonmari/web

# 학습된 모델 (약 256MB)
curl -L -o model/yolov4-obj_best.weights \
  https://github.com/23bulgogi/sonmari/releases/download/model-v1/yolov4-obj_best.weights
```

### 2. 설치 및 실행

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app:app --port 8000
```

브라우저에서 http://localhost:8000 을 열고 **카메라 시작**을 누르세요.

### Docker로 실행

```bash
cd web
docker build -t sonmari .
docker run -p 8000:8000 -v "$(pwd)/model:/app/model" sonmari
```

자세한 설정(임계값, 서버 배포 시 주의사항)은 [web/README.md](web/README.md)를 참고하세요.

---

## 구조

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

## 모델

- YOLOv4 (darknet), 입력 416×416, 34개 클래스
- 학습 설정: [`web/model/yolov4-obj.cfg`](web/model/yolov4-obj.cfg), 클래스 목록: [`web/model/obj.names`](web/model/obj.names)
- 학습 방법: [AlexeyAB/darknet — How to train to detect your custom objects](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects)

모델이 이상하게 동작하면(아무 동작에나 같은 라벨이 나오는 등) cfg와 weights가 짝이 맞는지 먼저 확인하세요.

```bash
cd web && python check_model.py
```

## 알려진 제한사항

- CPU로 실행하면 초당 약 4프레임 정도로 처리됩니다(iMac 기준). 여러 동작으로 된 단어는 동작을 천천히, 또렷하게 해야 인식이 잘 됩니다.
- 일부 동작(예: 수술)은 인식률이 낮습니다. 화면의 **좌우 반전해서 인식** 옵션을 켜면 나아질 수 있습니다.
- 조명, 배경, 카메라와의 거리가 학습 데이터와 다르면 정확도가 떨어집니다.
- 서버에 배포할 경우 브라우저는 HTTPS에서만 카메라를 허용합니다.
- 같은 단어는 문장에 한 번만 표시됩니다.

---

## 이전 데스크톱 버전 (Windows)

`src/` 폴더에는 PyQt5 + darknet DLL 기반의 Windows 데스크톱 버전이 있습니다.
Visual Studio, CMake, OpenCV 빌드가 필요하고 GPU 사용 시 CUDA 10.2 / cuDNN 7이 필요해 설치가 까다롭습니다. 새로 시작한다면 웹 버전을 권장합니다.
당시의 빌드 가이드는 [이전 README](https://github.com/23bulgogi/sonmari/blob/0aa1ad13fa47e978a30f3b0e0ba92b02fff65a15/README.md)에서 볼 수 있습니다.

## 기여하기

[CONTRIBUTING.md](CONTRIBUTING.md)를 참고해 주세요. 이 프로젝트에 참여하는 모든 분은 [행동 강령](CODE_OF_CONDUCT.md)을 따릅니다.

## 만든 사람들

whogodemo · Minju Ko · Jeongin Bae · bjin28 · Jeongkyu Shin

## 라이선스

[MIT License](LICENSE)
