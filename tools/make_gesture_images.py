"""
README용 동작 예시 이미지 만들기.
공개용 데이터셋(얼굴 가린 버전)에서 동작마다 사진 한 장을 골라, 손 부분을 중심으로 정사각형으로 잘라 저장한다.

사용법 (sonmari 레포 폴더에서):
  python3 make_gesture_images.py ~/Downloads/sonmari-dataset-public/train docs/gestures

  마음에 안 드는 사진은 다른 사진으로 바꿀 수 있음:
  python3 make_gesture_images.py ... --pick head=head_0042 --pick yes=yes_0100

결과:
  docs/gestures/<라벨>.jpg   (34장, 각 240x240)
  미리보기 이미지 (전체 한눈에 보기, 임시 폴더에 저장 - 실행하면 경로가 출력됨)
"""
import argparse
import os
import tempfile

import cv2
import numpy as np

SIZE = 240        # 저장 크기 (정사각형)
MARGIN = 1.5      # 손 박스보다 이만큼 넓게 자름


def load_names(root):
    for p in (os.path.join(root, "classes.txt"), os.path.join(os.path.dirname(root.rstrip("/")), "classes.txt")):
        if os.path.exists(p):
            return [l.strip() for l in open(p, encoding="utf-8") if l.strip()]
    raise SystemExit("classes.txt 를 찾지 못했습니다.")


def crop_hand(img, label_line):
    h, w = img.shape[:2]
    _, x, y, bw, bh = label_line.split()[:5]
    cx, cy = float(x) * w, float(y) * h
    side = max(float(bw) * w, float(bh) * h) * MARGIN
    side = int(min(side, w, h))
    x1 = int(min(max(0, cx - side / 2), w - side))
    y1 = int(min(max(0, cy - side / 2), h - side))
    return cv2.resize(img[y1:y1 + side, x1:x1 + side], (SIZE, SIZE), interpolation=cv2.INTER_AREA)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("train_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--pick", action="append", default=[], help="라벨=파일이름 (예: head=head_0042)")
    ap.add_argument("--index", type=int, default=10, help="기본으로 고를 사진 순번 (기본 10번째)")
    a = ap.parse_args()

    names = load_names(a.train_dir)
    picks = dict(p.split("=", 1) for p in a.pick)
    img_dir, lbl_dir = os.path.join(a.train_dir, "images"), os.path.join(a.train_dir, "labels")
    files = sorted(os.listdir(img_dir))
    os.makedirs(a.out_dir, exist_ok=True)

    tiles = []
    for name in names:
        cands = [f for f in files if f.startswith(name + "_")]
        if not cands:
            print(f"[건너뜀] {name}: 사진 없음"); continue
        if name in picks:
            chosen = next((f for f in cands if os.path.splitext(f)[0] == picks[name]), None)
            if chosen is None:
                raise SystemExit(f"{picks[name]} 를 찾지 못했습니다.")
        else:
            chosen = cands[min(a.index - 1, len(cands) - 1)]
        stem = os.path.splitext(chosen)[0]
        img = cv2.imread(os.path.join(img_dir, chosen))
        line = open(os.path.join(lbl_dir, stem + ".txt"), encoding="utf-8").readline()
        tile = crop_hand(img, line)
        cv2.imwrite(os.path.join(a.out_dir, name + ".jpg"), tile, [cv2.IMWRITE_JPEG_QUALITY, 85])
        print(f"{name:18s} <- {chosen}")
        labeled = tile.copy()
        cv2.rectangle(labeled, (0, SIZE - 28), (SIZE, SIZE), (0, 0, 0), -1)
        cv2.putText(labeled, f"{name} ({stem})", (6, SIZE - 9), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        tiles.append(labeled)

    cols = 6
    while len(tiles) % cols:
        tiles.append(np.full((SIZE, SIZE, 3), 255, np.uint8))
    sheet = np.vstack([np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)])
    preview = os.path.join(tempfile.gettempdir(), "sonmari_gesture_preview.jpg")  # 레포에 안 섞이게 임시 폴더에
    cv2.imwrite(preview, sheet)
    print(f"\n확인용 미리보기: {preview}")


if __name__ == "__main__":
    main()
