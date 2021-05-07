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

continuous = {'아파트':["apartment1","apartment2"], '아니':["no1","no2"], '불':["fire1","fire2"],
              '쓰러지다':["fall1","fall2"], '마비':["paralyze1","paralyze2"], '지하':["basement1", "basement2"]}
one = {'yes':'응', 'house':'집'}

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
    parser.add_argument("--weights", default="yolov4.weights",
                        help="yolo weights path")
    parser.add_argument("--dont_show", action='store_true',
                        help="windown inference display. For headless systems")
    parser.add_argument("--ext_output", action='store_true',
                        help="display bbox coordinates of detected objects")
    parser.add_argument("--config_file", default="./cfg/yolov4.cfg",
                        help="path to config file")
    parser.add_argument("--data_file", default="./cfg/coco.data",
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


def video_capture(frame_queue, darknet_image_queue):
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


def inference(darknet_image_queue, detections_queue, fps_queue):
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


def drawing(frame_queue, detections_queue, fps_queue):
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
            if word != "" and print_count < 15:
                print("word")
                draw.text((x1, y1), word, font=ImageFont.truetype('malgun.ttf', 36), fill=(255, 255, 255))
                image = np.array(pill_image)
                print_count += 1
                video.write(image)
                cv2.imshow('Inference', image)
                if cv2.waitKey(fps) == 27:
                    break
                continue
            
            print_count = 0
            word = ""

            if label in list(one.keys()):
                draw.text((x1, y1), one.get(label), font=ImageFont.truetype('malgun.ttf', 36), fill=(255, 255, 255))
                image = np.array(pill_image)

            for i in range(len(list_of_key)):
                if before_result==list_of_value[i][0]:
                    if label==list_of_value[i][1]:
                        word = list_of_key[i]
                        draw.text((x1, y1), word, font=ImageFont.truetype('malgun.ttf', 36), fill=(255, 255, 255))
                        image = np.array(pill_image)
                        break
                        #cv2.putText(frame, list_of_key[0], (x, y - 40), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1)

            if args.out_filename is not None:
                video.write(image)
            if not args.dont_show:
                cv2.imshow('Inference', image)
            if cv2.waitKey(fps) == 27:
                break
    cap.release()
    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    frame_queue = Queue()
    darknet_image_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    fps_queue = Queue(maxsize=1)

    args = parser()
    check_arguments_errors(args)
    network, class_names, class_colors = darknet.load_network(
            args.config_file,
            args.data_file,
            args.weights,
            batch_size=1
        )
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    input_path = str2int(args.input)
    cap = cv2.VideoCapture(input_path)
    Thread(target=video_capture, args=(frame_queue, darknet_image_queue)).start()
    Thread(target=inference, args=(darknet_image_queue, detections_queue, fps_queue)).start()
    Thread(target=drawing, args=(frame_queue, detections_queue, fps_queue)).start()
