"""
YOLOv4(darknet 형식) 모델을 OpenCV DNN으로 실행. darknet DLL/CUDA 불필요.
주의: OpenCV 5.x에는 readNetFromDarknet이 없으므로 4.x를 써야 한다 (requirements.txt 참고).
"""
import os
import cv2
import numpy as np

MODEL_DIR = os.environ.get("SONMARI_MODEL_DIR", os.path.join(os.path.dirname(__file__), "model"))


class Detector:
    def __init__(self, cfg="yolov4-obj.cfg", weights="yolov4-obj_best.weights",
                 names="obj.names", size=416, conf=0.70, nms=0.45):
        cfg_path = os.path.join(MODEL_DIR, cfg)
        weights_path = os.path.join(MODEL_DIR, weights)
        for p in (cfg_path, weights_path):
            if not os.path.exists(p):
                raise FileNotFoundError(f"모델 파일이 없습니다: {p}")
        with open(os.path.join(MODEL_DIR, names), encoding="utf-8") as f:
            self.names = [l.strip() for l in f if l.strip()]

        net = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)
        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(size, size), scale=1 / 255.0, swapRB=True)
        self.conf, self.nms = conf, nms

    def detect(self, frame_bgr, conf=None):
        """[(label, confidence, [x, y, w, h]), ...] 신뢰도 내림차순"""
        conf = self.conf if conf is None else conf
        class_ids, scores, boxes = self.model.detect(frame_bgr, conf, self.nms)
        out = [(self.names[int(c)], float(s), [int(v) for v in b])
               for c, s, b in zip(np.array(class_ids).flatten(), np.array(scores).flatten(), boxes)]
        return sorted(out, key=lambda d: -d[1])
