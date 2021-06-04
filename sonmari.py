import sys
from os import system
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cv2
import argparse
import darknet_video as dv
import darknet
from threading import Thread, enumerate
from queue import Queue

def parser():
    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument("--input", type=str, default=0,
                        help="video source. If empty, uses webcam 0 stream")
    parser.add_argument("--out_filename", type=str, default="",
                        help="inference video name. Not saved if empty")
    parser.add_argument("--weights", default="./backup/yolov4-obj_10000.weights",
                        help="yolo weights path")
    parser.add_argument("--dont_show", action='store_true',
                        help="windown inference display. For headless systems")
    parser.add_argument("--ext_output", action='store_true',
                        help="display bbox coordinates of detected objects")
    parser.add_argument("--config_file", default="./cfg/yolov4-obj.cfg",
                        help="path to config file")
    parser.add_argument("--data_file", default="./data/obj.data",
                        help="path to data file")
    parser.add_argument("--thresh", type=float, default=.25,
                        help="remove detections with confidence below this value")
    return parser.parse_args()

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("doctorui.ui")[0]

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

class PatientWindow(QDialog):
    def __init__(self, parent):
        super(PatientWindow, self).__init__(parent)
        patient_ui = 'patientui.ui'
        uic.loadUi(patient_ui, self)
        self.initUI()
    def function1(self, parent):
        self.movie = QMovie('의사수어/1.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.label.setMovie(self.movie)
        self.movie.start()
        self.textlabel.setText("어디가 아프세요?") #텍스트 변환

        self.show()
    def function2(self, parent):
        self.movie = QMovie('의사수어/2.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.label.setMovie(self.movie)
        self.movie.start()
        self.textlabel.setText("다른 증상은 없나요?") #텍스트 변환
        
        self.show()
    def function3(self, parent):
        self.movie = QMovie('의사수어/3.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.label.setMovie(self.movie)
        self.movie.start()
        self.textlabel.setText("밥은 잘 먹고 잘 주무셨나요?") #텍스트 변환
        self.show()
    def function4(self, parent):
        self.movie = QMovie('의사수어/4.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.label.setMovie(self.movie)
        self.movie.start()
        self.textlabel.setText("열이 났나요?") #텍스트 변환
        self.show()
    def function5(self, parent):
        self.movie = QMovie('의사수어/5.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.label.setMovie(self.movie)
        self.movie.start()
        self.textlabel.setText("언제부터 아프셨나요?") #텍스트 변환
        self.show()
    def function6(self, parent):
        self.movie = QMovie('의사수어/6.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.label.setMovie(self.movie)
        self.movie.start()
        self.textlabel.setText("약은 드셨나요?") #텍스트 변환
        self.show()
    def function7(self, parent):
        self.movie = QMovie('의사수어/7.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.label.setMovie(self.movie)
        self.movie.start()
        self.textlabel.setText("처방전 드릴게요") #텍스트 변환
        self.show()
        
    def initUI(self):
        self.move(2500,240)
        
#화면을 띄우는데 사용되는 Class 선언
class DoctorWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.pixmap = QPixmap()
        self.pixmap.load("icon.png")
        self.pixmap = self.pixmap.scaledToWidth(70)
        self.icon.setPixmap(self.pixmap)

        frame_queue = Queue()
        darknet_image_queue = Queue(maxsize=1)
        detections_queue = Queue(maxsize=1)
        fps_queue = Queue(maxsize=1)

        args = parser()

        network, class_names, class_colors = darknet.load_network(
            args.config_file,
            args.data_file,
            args.weights,
            batch_size=1
        )

        width = darknet.network_width(network)
        height = darknet.network_height(network)
        cap = cv2.VideoCapture(0)
        Thread(target=dv.video_capture, args=(cap, width, height, frame_queue, darknet_image_queue)).start()
        Thread(target=dv.inference, args=(cap, args, network, class_names, darknet_image_queue, detections_queue, fps_queue)).start()
        Thread(target=dv.drawing, args=(cap, self, args, width, height, class_colors, frame_queue, detections_queue, fps_queue)).start()

        

        self.pushButton.clicked.connect(self.button1Function)
        self.pushButton_2.clicked.connect(self.button2Function)
        self.pushButton_3.clicked.connect(self.button3Function)
        self.pushButton_4.clicked.connect(self.button4Function)
        self.pushButton_5.clicked.connect(self.button5Function)
        self.pushButton_6.clicked.connect(self.button6Function)
        self.pushButton_7.clicked.connect(self.button7Function)

    def button1Function(self):
        PatientWindow(self).function1(self)
    def button2Function(self):
        PatientWindow(self).function2(self)
    def button3Function(self):
        PatientWindow(self).function3(self)
    def button4Function(self):
        PatientWindow(self).function4(self)
    def button5Function(self):
        PatientWindow(self).function5(self)
    def button6Function(self):
        PatientWindow(self).function6(self)
    def button7Function(self):
        PatientWindow(self).function7(self)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
            cap.release()

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    doctorWindow = DoctorWindow() 

    #프로그램 화면을 보여주는 코드
    doctorWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

    sys.exit()
