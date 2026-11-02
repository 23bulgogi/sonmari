"""
모델 점검 도구.
  python check_model.py                 -> cfg와 weights 크기가 맞는지 확인
  python check_model.py 이미지.jpg ...   -> 학습 이미지로 실제 인식 결과 확인
"""
import os
import sys

MODEL_DIR = os.environ.get("SONMARI_MODEL_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "model"))
CFG = os.path.join(MODEL_DIR, "yolov4-obj.cfg")
WEIGHTS = os.path.join(MODEL_DIR, "yolov4-obj_best.weights")


def parse_cfg(path):
    blocks, cur = [], None
    for line in open(path, encoding="utf-8", errors="ignore"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        if line.startswith("["):
            cur = {"type": line.strip("[]")}
            blocks.append(cur)
        elif "=" in line and cur is not None:
            k, v = line.split("=", 1)
            cur[k.strip()] = v.strip()
    return blocks


def expected_weight_count(path):
    """cfg 구조로 weights 파일에 들어 있어야 할 float 개수 계산"""
    blocks = parse_cfg(path)
    net = blocks[0]
    c = int(net.get("channels", 3))
    out_ch, total = [], 0
    for b in blocks[1:]:
        t = b["type"]
        if t == "convolutional":
            f, k = int(b["filters"]), int(b["size"])
            g = int(b.get("groups", 1))
            bn = int(b.get("batch_normalize", 0))
            total += f * (c // g) * k * k + (4 * f if bn else f)
            c = f
        elif t == "route":
            idx = [int(x) for x in b["layers"].split(",")]
            idx = [i if i >= 0 else len(out_ch) + i for i in idx]
            c = sum(out_ch[i] for i in idx) // int(b.get("groups", 1))
        elif t in ("shortcut", "maxpool", "upsample", "yolo", "dropout"):
            pass
        else:
            print(f"[주의] 계산에 반영하지 않은 층: {t}")
        out_ch.append(c)
    return total


def check_size():
    n = expected_weight_count(CFG)
    with open(WEIGHTS, "rb") as f:
        import struct
        major, minor, _ = struct.unpack("3i", f.read(12))
    header = 20 if (major * 10 + minor) >= 2 else 16
    expected = header + n * 4
    actual = os.path.getsize(WEIGHTS)
    print(f"cfg 기준 예상 크기 : {expected:,} bytes")
    print(f"weights 실제 크기  : {actual:,} bytes")
    if actual == expected:
        print("=> 크기 일치. cfg와 weights 구조가 맞습니다.")
    else:
        print("=> 크기 불일치! 이 cfg로 학습한 weights가 아니거나, 파일이 덜 받아졌습니다.")


def check_images(paths):
    import cv2
    from detector import Detector
    d = Detector(conf=0.05)
    for p in paths:
        img = cv2.imread(p)
        if img is None:
            print(p, "-> 이미지를 못 읽음")
            continue
        top = d.detect(img)[:3]
        print(os.path.basename(p), "->", ", ".join(f"{l} {c:.0%}" for l, c, _ in top) or "검출 없음")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_images(sys.argv[1:])
    else:
        check_size()
