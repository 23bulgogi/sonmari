from ctypes import *
import random
import os
import cv2
import time
import darknet
import argparse
from threading import Thread, enumerate
from queue import Queue
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import doctorui
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


continuous = {'감기에 걸렸습니다':["cold1","cold2"], '아니오':["no1","no2"], '콧물이 나고':["runnynose1","runnynose2"],
              '쓰러졌습니다':["fall1","fall2"], '설사를 합니다':["diarrhea1","diarrhea2"]}
one = {'2day':'2일전에', '3day':'3일전에', 'yes':'네', 'head':'머리가', 'stomach':'배가', 'sick':'아픕니다','reset':''}

list_of_key = list(continuous.keys())
list_of_value = list(continuous.values())

result_class = []

b,g,r,a = 255,255,255,0
fontpath = "fonts/gulim.ttc"
font = ImageFont.truetype(fontpath, 20)

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


def str2int(video_path):
    """
    argparse returns and string althout webcam uses int (0, 1 ...)
    Cast to int if needed
    """
    try:
        return int(video_path)
    except ValueError:
        return video_path


def check_arguments_errors(args):
    assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(args.config_file):
        raise(ValueError("Invalid config path {}".format(os.path.abspath(args.config_file))))
    if not os.path.exists(args.weights):
        raise(ValueError("Invalid weight path {}".format(os.path.abspath(args.weights))))
    if not os.path.exists(args.data_file):
        raise(ValueError("Invalid data file path {}".format(os.path.abspath(args.data_file))))
    if str2int(args.input) == str and not os.path.exists(args.input):
        raise(ValueError("Invalid video path {}".format(os.path.abspath(args.input))))


def set_saved_video(input_video, output_video, size):
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    fps = int(input_video.get(cv2.CAP_PROP_FPS))
    video = cv2.VideoWriter(output_video, fourcc, fps, size)
    return video


def video_capture(cap, width, height, frame_queue, darknet_image_queue):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height),
                                   interpolation=cv2.INTER_LINEAR)
        frame_queue.put(frame_resized)
        img_for_detect = darknet.make_image(width, height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        darknet_image_queue.put(img_for_detect)
    cap.release()


def inference(cap, args, network, class_names, darknet_image_queue, detections_queue, fps_queue):
    while cap.isOpened():
        darknet_image = darknet_image_queue.get()
        prev_time = time.time()
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=args.thresh)
        detections_queue.put(detections)
        fps = int(1/(time.time() - prev_time))
        fps_queue.put(fps)
        print("FPS: {}".format(fps))
        darknet.print_detections(detections, args.ext_output)
        darknet.free_image(darknet_image)
    cap.release()


def drawing(cap, window, args, width, height, class_colors, frame_queue, detections_queue, fps_queue):
    random.seed(3)  # deterministic bbox colors
    video = set_saved_video(cap, args.out_filename, (width, height))
    label = ""
    word = ""
    before_result=""
    print_count = 0
    while cap.isOpened():
        if label != "":
            before_result = label
            
        #print(before_result)
        frame_resized = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()
        if frame_resized is not None:
            label, image = darknet.draw_boxes(detections, frame_resized, class_colors)
            print(label)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pill_image = Image.fromarray(image)
            draw = ImageDraw.Draw(pill_image)
            x1, y1 = 30, 30

            #핵심동작 1개인 수화는 15번 출력되게 함
            if word != "" and print_count < 15:
                draw.text((x1, y1), word, font=ImageFont.truetype('malgun.ttf', 36), fill=(0, 0, 0))
                image = np.array(pill_image)
                print_count += 1
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h,w,c = image.shape
                qImg = QtGui.QImage(image.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                window.image.setPixmap(pixmap)


                if cv2.waitKey(fps) == 27:
                    break
                continue
            
            print_count = 0
            word = ""

            #핵심동작 1개인 수화 출력
            if label in list(one.keys()):
                draw.text((x1, y1), one.get(label), font=ImageFont.truetype('malgun.ttf', 36), fill=(0, 0, 0))
                image = np.array(pill_image)

            #핵심동작 2개인 수화 출력

            for i in range(len(list_of_key)):
                if before_result==list_of_value[i][0]:
                    if label==list_of_value[i][1]:
                        word = list_of_key[i]
                        draw.text((x1, y1), word, font=ImageFont.truetype('malgun.ttf', 36), fill=(0, 0, 0))
                        image = np.array(pill_image)
                        break
                        
            if args.out_filename is not None:
                video.write(image)
            if not args.dont_show:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h,w,c = image.shape
                qImg = QtGui.QImage(image.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                window.image.setPixmap(pixmap)
                
            if cv2.waitKey(fps) == 27:
                break
    cap.release()
    video.release()
    cv2.destroyAllWindows()
