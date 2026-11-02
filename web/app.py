"""
손마리 웹 서버.  실행:  uvicorn app:app --host 0.0.0.0 --port 8000
브라우저가 웹캠 프레임(JPEG)을 WebSocket으로 보내면, 검출 결과와 번역 문장을 돌려준다.
"""
import asyncio
import os

import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from detector import Detector
from translator import Translator

app = FastAPI(title="Sonmari")
THRESH = float(os.environ.get("SONMARI_THRESH", 0.70))
DEBUG_THRESH = 0.05  # 디버그용: 임계값 아래 후보도 화면에 표시
detector = Detector(conf=THRESH)
lock = asyncio.Lock()  # OpenCV DNN 네트워크는 동시에 한 프레임씩만 처리
STATIC = os.path.join(os.path.dirname(__file__), "static")


@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC, "index.html"))


@app.get("/health")
def health():
    return {"ok": True, "classes": len(detector.names)}


@app.websocket("/ws")
async def ws(socket: WebSocket):
    await socket.accept()
    tr = Translator()  # 접속(사용자)마다 문장 상태를 따로 둔다
    loop = asyncio.get_running_loop()
    try:
        while True:
            msg = await socket.receive()
            if msg.get("text") == "reset":
                tr.reset()
                await socket.send_json({"detections": [], "word": None, "sentence": ""})
                continue
            data = msg.get("bytes")
            if not data:
                continue
            frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
            if frame is None:
                continue
            async with lock:
                raw = await loop.run_in_executor(None, detector.detect, frame, DEBUG_THRESH)
            dets = [d for d in raw if d[1] >= THRESH]
            word, sentence = tr.step(dets[0][0] if dets else "")
            await socket.send_json({
                "detections": [{"label": l, "conf": round(c, 3), "box": b} for l, c, b in dets],
                "word": word.strip() if word else None,
                "sentence": sentence,
                "candidates": [{"label": l, "conf": round(c, 3)} for l, c, _ in raw[:3]],
                "thresh": THRESH,
                "width": frame.shape[1], "height": frame.shape[0],
            })
    except (WebSocketDisconnect, RuntimeError):
        pass
