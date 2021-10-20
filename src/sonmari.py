import sys
from os import system
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cv2
import argparse
import sonmari_video as sv
import darknet
from threading import Thread, enumerate
from queue import Queue



def parser():
    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument("--input", type=str, default=0,
                        help="video source. If empty, uses webcam 0 stream")
    parser.add_argument("--out_filename", type=str, default="",
                        help="inference video name. Not saved if empty")
    parser.add_argument("--weights", default="./backup/yolov4-obj_96_best.weights",
                        help="yolo weights path")
    parser.add_argument("--dont_show", action='store_true',
                        help="windown inference display. For headless systems")
    parser.add_argument("--ext_output", action='store_true',
                        help="display bbox coordinates of detected objects")
    parser.add_argument("--config_file", default="./cfg/yolov4-obj.cfg",
                        help="path to config file")
    parser.add_argument("--data_file", default="./data/obj.data",
                        help="path to data file")
    parser.add_argument("--thresh", type=float, default=.70,
                        help="remove detections with confidence below this value")
    return parser.parse_args()



#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("sonmariui.ui")[0]



        
#화면을 띄우는데 사용되는 Class 선언
class SonmariWindow(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)


        self.pixmap = QPixmap()
        self.pixmap.load("logo.png")
        self.pixmap = self.pixmap.scaledToWidth(100)
        self.icon.setPixmap(self.pixmap)
        #아이콘 추가

        args = parser()


        frame_queue = Queue()
        darknet_image_queue = Queue(maxsize=1)
        detections_queue = Queue(maxsize=1)
        fps_queue = Queue(maxsize=1)


        network, class_names, class_colors = darknet.load_network(
            args.config_file,
            args.data_file,
            args.weights,
            batch_size=1
        )

        width = darknet.network_width(network)
        height = darknet.network_height(network)
        #웹캠을 이용해 캡처
        cap = cv2.VideoCapture(0)

        #캡처 쓰레드
        Thread(target=sv.video_capture, args=(cap, width, height, frame_queue, darknet_image_queue)).start()
        #detect 쓰레드
        Thread(target=sv.inference, args=(cap, args, network, class_names, darknet_image_queue, detections_queue, fps_queue)).start()
        #출력 쓰레드
        Thread(target=sv.drawing, args=(cap, self, args, width, height, class_colors, frame_queue, detections_queue, fps_queue)).start()

        


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
            cap.release()
            #esc 누르면 종료

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    sonmariWindow = SonmariWindow() 

    #프로그램 화면을 보여주는 코드
    sonmariWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

    sys.exit()


    
