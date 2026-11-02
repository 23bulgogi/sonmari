"""
수어 인식 결과(프레임별 라벨) -> 한국어 문장 변환.
기존 src/sonmari_video.py의 drawing() 로직을 UI/darknet과 분리해서 그대로 옮긴 것.
"""
from collections import OrderedDict

# 핵심 이미지가 여러 개인 수어 동작
CONTINUOUS = {
    '감기 ': ["cold1", "cold2"], '아니오 ': ["no1", "no2"], '콧물 ': ["runnynose1", "runnynose2"],
    '쓰러지다 ': ["fall1", "fall2"], '설사 ': ["diarrhea1", "diarrhea2"],
    '입원 ': ["hospitalization1", "hospitalization2", "hospitalization3"],
    '퇴원 ': ["hospitalization3", "hospitalization2", "hospitalization1"],
    '완쾌 ': ["recovery1", "recovery2", "recovery3"],
    '소화불량 ': ["digestion1", "digestion2", "poor"],
    '변비 ': ["constipation1", "constipation2", "constipation3"],
    '소변 ': ["urine1", "urine2"], '수술 ': ["surgery1", "surgery2"], '낫다 ': ["", "recovery3"],
}
# 핵심 이미지가 하나인 수어 동작
ONE = {'2day': '2일 ', '3day': '3일 ', 'yes': '네 ', 'head': '머리 ', 'stomach': '배 ',
       'sick': '아프다 ', 'reset': '', 'medicine': '약 '}


class Translator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.sentence = []
        self.result = ""
        self.before_result = ""
        self.queue = []  # 최근 결과 최대 3개

    def step(self, label):
        """한 프레임의 최고 신뢰도 라벨("" = 검출 없음)을 넣으면 (이번에 인식된 단어, 현재 문장)을 돌려준다."""
        word = None
        self.sentence = list(OrderedDict.fromkeys(self.sentence))

        if self.result != "":
            self.before_result = self.result

        if label != "":
            self.result = label
            if self.before_result != self.result and self.result not in ONE:
                self.queue.append(self.result)
                self.queue = self.queue[-3:]

            if label in ONE:
                if label == 'reset':
                    self.sentence = []
                else:
                    self.sentence.append(ONE[label])
                word = ONE[label]
                self.queue = []

            q = self.queue
            if 'recovery1' not in q and 'recovery2' not in q and label == 'recovery3':
                self.sentence.append('낫다 ')
                word = '낫다 '

            for key, seq in CONTINUOUS.items():
                if q == seq or q[1:] == seq:
                    self.sentence.append(key)
                    word = key
                    break

        self.sentence = list(OrderedDict.fromkeys(self.sentence))
        return word, ''.join(self.sentence).strip()
