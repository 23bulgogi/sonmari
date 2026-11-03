"""
두 weights 파일을 테스트 데이터로 채점해서 비교한다.

사용법 (web 폴더에서, venv 켠 상태):
  python compare_models.py <테스트 폴더> <weights A> <weights B> [--limit 300]

  <테스트 폴더>: 이미지(.jpg)와 같은 이름의 라벨(.txt)이 들어 있는 폴더 (예: 테스트jpg + 테스트txt를 한 폴더에 푼 것)

채점 방식:
  이미지마다 모델이 가장 확신하는 동작 하나를 고르고, 그게 정답 라벨에 있으면 정답.
  (웹 앱도 프레임마다 가장 확신하는 동작 하나만 쓰기 때문에 같은 기준)
"""
import argparse
import os
import random
import struct
import time
from collections import Counter

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(HERE, "model", "yolov4-obj.cfg")
NAMES = os.path.join(HERE, "model", "obj.names")


def header_info(path):
    with open(path, "rb") as f:
        major, minor, _ = struct.unpack("3i", f.read(12))
        seen = struct.unpack("Q" if major * 10 + minor >= 2 else "I", f.read(8 if major * 10 + minor >= 2 else 4))[0]
    return seen


def load(path):
    net = cv2.dnn.readNetFromDarknet(CFG, path)
    m = cv2.dnn_DetectionModel(net)
    m.setInputParams(size=(416, 416), scale=1 / 255.0, swapRB=True)
    return m


def top_class(model, img, conf):
    ids, scores, _ = model.detect(img, conf, 0.45)
    ids, scores = np.array(ids).flatten(), np.array(scores).flatten()
    if len(ids) == 0:
        return None
    return int(ids[int(np.argmax(scores))])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("test_dir"); ap.add_argument("weights_a"); ap.add_argument("weights_b")
    ap.add_argument("--limit", type=int, default=0, help="이미지 수 제한 (0 = 전부)")
    ap.add_argument("--conf", type=float, default=0.25)
    a = ap.parse_args()

    names = [l.strip() for l in open(NAMES, encoding="utf-8") if l.strip()]
    samples = []
    for d, _, files in os.walk(a.test_dir):
        for f in files:
            stem, ext = os.path.splitext(f)
            txt = os.path.join(d, stem + ".txt")
            if ext.lower() in (".jpg", ".jpeg", ".png") and os.path.exists(txt):
                gt = {int(l.split()[0]) for l in open(txt, encoding="utf-8", errors="ignore") if l.split()}
                if gt:
                    samples.append((os.path.join(d, f), gt))
    if not samples:
        raise SystemExit("라벨이 있는 이미지를 찾지 못했습니다. jpg와 txt가 같은 폴더에 있는지 확인하세요.")
    random.seed(0)
    random.shuffle(samples)
    if a.limit:
        samples = samples[:a.limit]

    models = {}
    for key, path in (("A", a.weights_a), ("B", a.weights_b)):
        print(f"[{key}] {os.path.basename(path)}  학습량: 이미지 {header_info(path):,}장 분량")
        models[key] = load(path)

    correct = {k: 0 for k in models}
    miss = {k: 0 for k in models}
    per_total, per_ok = Counter(), {k: Counter() for k in models}
    wrong = {k: {} for k in models}  # 정답 클래스 -> Counter(모델이 대신 고른 것)
    t0 = time.time()
    for i, (path, gt) in enumerate(samples, 1):
        img = cv2.imread(path)
        if img is None:
            continue
        for c in gt:
            per_total[c] += 1
        for k, m in models.items():
            p = top_class(m, img, a.conf)
            if p is None:
                miss[k] += 1
            elif p in gt:
                correct[k] += 1
                per_ok[k][p] += 1
            for c in gt:
                if p not in gt:
                    wrong[k].setdefault(c, Counter())[names[p] if p is not None else '(검출 없음)'] += 1
        if i % 50 == 0:
            print(f"  {i}/{len(samples)} ({time.time() - t0:.0f}초)")

    n = len(samples)
    print(f"\n테스트 이미지 {n}장")
    for k in models:
        print(f"[{k}] 정답률 {correct[k] / n:.1%}  (검출 못함 {miss[k]}장)")

    def top_wrong(k, c):
        w = wrong[k].get(c)
        return ", ".join(f"{l}×{n}" for l, n in w.most_common(2)) if w else ""

    print("\n| 클래스 | 이미지 수 | A 정답률 | B 정답률 | B가 대신 고른 것 |")
    print("|---|---|---|---|---|")
    for c in range(len(names)):
        t = per_total[c]
        if t == 0:
            print(f"| {names[c]} | 0 | - | - | (테스트 이미지 없음) |")
            continue
        ra, rb = per_ok["A"][c] / t, per_ok["B"][c] / t
        mark = " ←" if abs(ra - rb) >= 0.15 else ""
        print(f"| {names[c]} | {t} | {ra:.0%} | {rb:.0%}{mark} | {top_wrong('B', c)} |")
    extra = sorted(c for c in per_total if c >= len(names))
    if extra:
        print(f"\n[주의] obj.names에 없는 클래스 번호가 라벨에 있음: {extra}")


if __name__ == "__main__":
    main()
