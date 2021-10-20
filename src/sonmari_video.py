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
from collections import OrderedDict

continuous = {'감기 ':["cold1","cold2"], '아니오 ':["no1","no2"], '콧물 ':["runnynose1","runnynose2"],
              '쓰러지다 ':["fall1","fall2"], '설사 ':["diarrhea1","diarrhea2"], '입원 ':["hospitalization1","hospitalization2","hospitalization3"],
              '퇴원 ':["hospitalization3","hospitalization2","hospitalization1"],
              '완쾌 ':["recovery1","recovery2","recovery3"], '소화불량 ' :["digestion1","digestion2","poor"], '변비 ':["constipation1","constipation2","constipation3"],
              '소변 ':["urine1","urine2"], '수술 ':["surgery1","surgery2"],  '낫다 ':["","recovery3"]}
#핵심 이미지가 여러개인 수화 동작 저장

one = {'3day':'3일 ', 'yes':'네 ', 'head':'머리 ', 'stomach':'배 ', 'sick':'아프다 ','reset':'','medicine':'약 '}
#핵심 이미지가 하나인 수화 동작 저장

list_of_key = list(continuous.keys())
list_of_value = list(continuous.values())
#핵심 이미지가 여러개인 단어인 경우,
#단어 별 핵심 이미지들은 value에 저장, 한국어 단어는 key에 저장

b,g,r,a = 255,255,255,0
fontpath = "fonts/gulim.ttc"
font = ImageFont.truetype(fontpath, 20)
#한글을 출력할 폰트 설정



def video_capture(cap, width, height, frame_queue, darknet_image_queue):
    #웹캠으로 이미지를 캡처
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
    #캡처한 이미지를 토대로 detect
    while cap.isOpened():
        darknet_image = darknet_image_queue.get()
        prev_time = time.time()
        #캡처한 이미지에 대한 detect 결과 가져옴
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=args.thresh)
        #큐에 detect 결과 추가
        detections_queue.put(detections)
        fps = int(1/(time.time() - prev_time))
        fps_queue.put(fps)
        #FPS 출력
        print("FPS: {}".format(fps))
        darknet.print_detections(detections, args.ext_output)
        darknet.free_image(darknet_image)
    cap.release()


def drawing(cap, window, args, width, height, class_colors, frame_queue, detections_queue, fps_queue):
    #detect 결과 출력
    
    random.seed(3)   
    label = ""       #detect 결과(실시간으로 detect된 이미지)
    word = ""        #최종으로 출력할 단어
    sentence=[]      #출력할 문장
    
    result = ""          #현재 결과
    before_result = ""  #이전 결과
    result_que = Queue(3) #result들을 저장하는 큐 생성. 현재 결과까지 최대 3개 저장
    
    
    while cap.isOpened():         
        
        frame_resized = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()

        if frame_resized is not None:

                                
            label, image = darknet.draw_boxes(detections, frame_resized, class_colors)         
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            #한글을 이미지 위에 출력하기 위해 hand_image로 변환
            hand_image = Image.fromarray(image)
            draw = ImageDraw.Draw(hand_image)
            x, y = 30, 30

            #문장 출력
            sentence=list(OrderedDict.fromkeys(list(sentence)))
            window.sentence.setText(''.join(sentence))

            #result가 null이 아닌 경우에만 before_result에 저장
            if result != "":
                before_result = result
            
            #디텍션 결과가 null이 아닌 경우에만 result에 저장
            if label != "":
                result = label

                #이전 결과와 현재 결과가 다른 경우에만 결과 큐에 저장
                if(before_result != result and result not in list(one.keys())):
                    if(not result_que.full()):
                        result_que.put(result)
                    else:
                        #큐가 가득 차있으면 원소 제거 후 삽입
                        result_que.get()
                        result_que.put(result)
                

                              
                #핵심동작 1개인 수화 출력
                if label in list(one.keys()):
                    if label == 'reset':
                        #인식한 이미지가 리셋일 경우 문장 초기화
                        sentence=[]
                    else:
                        #리셋이 아닐경우 문장에 추가
                        sentence.append(one.get(label))                    
                    draw.text((x, y), one.get(label), font=ImageFont.truetype('malgun.ttf', 36), fill=(0, 0, 0))
                    result_que = Queue(3)

                list_of_result = list(result_que.queue)
                #큐를 리스트로 변환

                print(list_of_result)


                
                #'완쾌'와 독립적으로 '낫다' 출력
                if 'recovery1' not in list_of_result and 'recovery2' not in list_of_result and label=='recovery3':
                    sentence.append('낫다 ')    
                    draw.text((x, y), "낫다", font=ImageFont.truetype('malgun.ttf', 36), fill=(0, 0, 0))
                    
                    
                #핵심동작 2개,3개인 수화 출력
                for i in range(len(list_of_key)):
                    if list_of_result == list_of_value[i] or list_of_result[1:] == list_of_value[i]:
                        #현재까지 저장된 result들을 토대로 단어 생성
                        word = list_of_key[i]
                        sentence.append(word)
                        #출력할 문장에 최종 단어 추가
                        draw.text((x, y), word, font=ImageFont.truetype('malgun.ttf', 36), fill=(0, 0, 0))
                        break                                         


            #detect한 최종 이미지를 UI로 전달
            image = np.array(hand_image)
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
