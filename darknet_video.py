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
import sonmari
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore




three = {'입원':["hospitalization1","hospitalization2", "hospitalization3"],'퇴원':["hospitalization3","hospitalization2","hospitalization1"],
              '완쾌':["recovery1","recovery2","recovery3"], '소화불량':["digestion1","digestion2","poor"], '변비':["constipation1","constipation2","constipation3"]}

two = {'감기':["cold1","cold2"], '아니오':["no1","no2"], '콧물':["runnynose1","runnynose2"], '쓰러지다':["fall1","fall2"], '설사':["diarrhea1","diarrhea2"],
       '낫다':["recovery1","recovery2"], '대변':["constipation1","constipation2"],'소변':["urine1","urine2"], '수술':["surgery1","surgery2"]}

one = {'2day':'2일', '3day':'3일', 'yes':'네', 'head':'머리', 'stomach':'배', 'sick':'아프다','reset':'','medicine':'약'}

key_of_2 = list(two.keys())
value_of_2 = list(two.values())

key_of_3 = list(three.keys())
value_of_3 = list(three.values())


b,g,r,a = 255,255,255,0
fontpath = "fonts/gulim.ttc"
font = ImageFont.truetype(fontpath, 20)


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
    label = "" #detect 결과
    word = "" #출력할 단어
    
    twice_before_result="" #이전 이전의 결과
    before_result="" #이전 결과
    result = "" #현재 결과
    print_count = 0
    
    while cap.isOpened():
            
        
        frame_resized = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()
        if frame_resized is not None:

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

            
            if before_result != "" and label != "":
                #이전 결과에 저장된 값과 이전 결과가 모두 null이 아니면 한칸씩 밀려남
                twice_before_result = before_result
                before_result = label
            elif label != "":
                #이전 결과에 저장된 값은 null이지만 이전 결과는 null이 아닌 경우
                before_result = label

                    

            #디텍션 결과 받아옴
            label, image = darknet.draw_boxes(detections, frame_resized, class_colors)
            #print(label)
            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pill_image = Image.fromarray(image)
            draw = ImageDraw.Draw(pill_image)
            x1, y1 = 30, 30

            

            if label != "":
                result = label
                #디텍션 결과가 null이 아닌 경우에만 result에 저장시켜줌
                
                #핵심동작 1개인 수화 출력
                if label in list(one.keys()):
                    draw.text((x1, y1), one.get(label), font=ImageFont.truetype('malgun.ttf', 36), fill=(0, 0, 0))
                    image = np.array(pill_image)


                #이전 이전의 결과, 이전 결과, 현재 결과의 내용이 같지 않도록 조정해줌
                    
                if twice_before_result == before_result:
                    if before_result == result:
                        twice_before_result = ""
                        before_result = ""
                    else:
                        twice_before_result = ""
                elif before_result == result:
                    before_result = twice_before_result
                    twice_before_result = ""
                    


                #핵심동작 2개,3개인 수화 출력

                for i in range(len(key_of_2)):
                    if before_result == value_of_2[i][0]:
                        if result == value_of_2[i][1]:
                            word = key_of_2[i]
                            draw.text((x1, y1), word, font=ImageFont.truetype('malgun.ttf', 36), fill=(0, 0, 0))
                            image = np.array(pill_image)
                            break
                    
                for i in range(len(key_of_3)):
                    if twice_before_result == value_of_3[i][0]:
                        if before_result == value_of_3[i][1]:
                            if result == value_of_3[i][2]:
                                word = key_of_3[i]
                                draw.text((x1, y1), word, font=ImageFont.truetype('malgun.ttf', 36), fill=(0, 0, 0))
                                image = np.array(pill_image)
                                break
                    
                        
            

            
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h,w,c = image.shape
            qImg = QtGui.QImage(image.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            window.image.setPixmap(pixmap)
                
            if cv2.waitKey(fps) == 27:
                break
            #esc누르면 종료
            
    cap.release()
    video.release()
    cv2.destroyAllWindows()
