# 손마리 웹 버전

darknet DLL·CUDA·Visual Studio 없이, OpenCV DNN으로 기존 YOLOv4 모델을 그대로 돌리는 웹 버전입니다.
Mac / Windows / Linux 어디서나 CPU로 동작하고, 브라우저에서 웹캠으로 사용합니다.

## 1. 모델 파일 넣기

`model/` 폴더에 아래 세 파일이 있어야 합니다.

| 파일 | 출처 |
|---|---|
| `yolov4-obj.cfg` | 레포에 포함 (학습에 쓴 cfg와 다르면 학습용 cfg로 교체) |
| `obj.names` | 레포에 포함 |
| `yolov4-obj_best.weights` | 구글 드라이브에서 받아서 직접 넣기 (git에는 올리지 않음) |

> cfg의 `classes=34`, 마지막 층들의 `filters=117`이 weights를 학습할 때 쓴 값과 같아야 합니다.
> 다르면 로드 단계에서 에러가 나거나 결과가 엉망이 됩니다.

## 2. Mac에서 실행

```bash
cd web
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --port 8000
```

브라우저에서 http://localhost:8000 → "카메라 시작" → 카메라 권한 허용.

## 3. Docker로 실행 / 배포

```bash
docker build -t sonmari .
docker run -p 8000:8000 -v "$(pwd)/model:/app/model" sonmari
```

서버에 올릴 때 주의:
- 브라우저는 **HTTPS에서만** 카메라를 허용합니다 (localhost는 예외). ALB+ACM, Caddy, nginx 등으로 HTTPS를 붙여야 합니다.
- WebSocket(`/ws`)을 프록시가 통과시키도록 설정해야 합니다.
- 영상 프레임이 서버로 전송되므로, 병원 환경에서는 개인정보 처리 방침을 안내해야 합니다.

## 환경 변수

| 이름 | 기본값 | 설명 |
|---|---|---|
| `SONMARI_MODEL_DIR` | `./model` | 모델 파일 폴더 |
| `SONMARI_THRESH` | `0.70` | 검출 신뢰도 임계값 (기존 `--thresh`와 동일) |

## 구조

- `detector.py` — OpenCV DNN으로 YOLOv4 실행
- `translator.py` — 프레임별 라벨 → 문장 변환 (기존 `sonmari_video.py` 로직 이식)
- `app.py` — FastAPI 서버, `/ws` WebSocket
- `static/index.html` — 웹캠 화면
- `test_translator.py` — 번역 로직 테스트 (`python test_translator.py`)
