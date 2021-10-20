# Sonmari

Open-source Sign language translator using deep learning model

[![GitHub version](https://badge.fury.io/gh/23bulgogi%2Fsonmari.svg)](https://badge.fury.io/gh/23bulgogi%2Fsonmari)

## 수어번역기 손마리

<img src="https://user-images.githubusercontent.com/74365895/132082420-573b5459-bdbd-4ee7-b9ad-afab2ce75651.gif"  width="800" height="450">

### Demo on [YouTube](https://youtu.be/WgXRq9RozLM) 

## Info

수어를 한국어로 번역해주는 병원용 수어 번역 프로그램으로 의료 통역사가 부족한 상황에서 청각장애인이 진료를 받을 때 통역사의 도움 없이 독립적으로 진료를 받을 수 있도록 하는 것이 목적이다. 프로그램을 사용하여 의사가 청각장애인의 수어를 이해할 수 있도록 디자인했다.

## Role

카메라를 통해 수어 영상이 입력으로 들어오면 그 영상을 한국어 문자언어로 실시간 번역하여 화면에 출력한다.    
예를 들어 ‘설사’, ‘감기’, ‘콧물’ 등의 수어 동작을 카메라에 비추면, 이 모션을 인식하여 해당 의미의 한국어로 화면에 출력해준다. 또한 이 프로그램에서는 '리셋' 동작을 별도로 지정해두었다. 사용자가 '리셋' 동작을 취할 때까지 출력된 단어들을 화면 위에 모두 보여주어, 문장 수준의 이해가 가능하도록 했다.

## Contribution Guide

Contributing to sonmari : [HOW TO CONTRIBUTE](https://github.com/23bulgogi/sonmari/blob/main/CONTRIBUTING.md) 

## Setup Guide

### Prerequistics
 * WebCam
 * GPU (for training)
    * For testing, GPU is not needed.

### Software requirements
 - Python 3.6
 - OpenCV 3.x
 - CMAKE 3.18
 - CUDA 10.2
 - cuDNN 8.0.2
 - PYQT5


## Development Guide

### Code of conduct
View [Code of conduct](https://github.com/23bulgogi/sonmari/blob/main/CODE_OF_CONDUCT.md) for community guidelines.

### Setting-up dev. environment
Refer [BUILD](https://github.com/23bulgogi/sonmari/blob/main/BUILD.md).

### Training custom YOLO model

1. 이미지 데이터를 수집한다. 다운받아서 사용할 수 있도록 웹에 오픈되어 있는 수어 이미지 데이터가 거의 없기 때문에, 이미지를 직접 촬영하여 수집하였다. 직접 수집한 약 10000장의 데이터를 7:1:1의 비율로 트레이닝셋, 검증셋, 테스트셋으로 나누었다.
  
2. 이미지를 라벨링한다. 이미지를 모델에 학습시키기 위해서 라벨링 툴을 이용해 필요한 이미지를 라벨링 해야한다. 라벨링 툴으로는 laeblImg 를 이용하였다.  labelImg를 이용할 때 모드를 YOLO로 설정하여 결과물이 txt파일로 저장되도록 해야한다.   
 - labelImg 설치 및 사용 : https://github.com/tzutalin/labelImg 참고.
  
3. custom data를 훈련시키기 위해서는 아래의 파일들이 필요하다.
  ```
  obj.data     
  obj.cfg    
  obj.names    
  train.txt   
  valid.txt    
  ```
4. darknet에서 제공하는 Yolov4의 pretrain 모델([yolov4.conv.137](https://drive.google.com/file/d/1JKF-bdIklxOOVy-2Cr5qdvjgGpmGfcbp/view))을 다운 받은 후 훈련을 시작한다. 
5. train YOLOv4 

```
./darknet detector train custom/obj.data custom/obj.cfg yolov4.conv.137 -map
```

<img src="https://user-images.githubusercontent.com/74365895/132083511-cda04b4b-128b-4daa-add1-5dd76490599d.png"  width="600" height="600">

6. Accuracy

<img src="https://user-images.githubusercontent.com/74365895/132083595-f0396d20-a029-46be-9089-38191b5f26cd.png"  width="640" height="692">

### Testing 

darknet.py 와 sonmari_video.py를 다운받은 후 sonmari_video.py를 실행한다. weights 파일은 training 결과로 얻은 것을 이용한다.
```
sonmari_video.py
```

## Using sonmari

logo.png, sonmari.py, sonmariui.ui 를 sonmari_video.py 와 같은 경로에 다운받은 후 sonmari.py를 실행한다.
```
sonmari.py
```

## Dataset

<img src="https://user-images.githubusercontent.com/74365895/132034383-fb3dbb94-402a-4e70-977f-89c9e2f481f0.jpg"  width="800" height="400">

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/23bulgogi/sonmari/blob/main/LICENSE) file for details

## References

 * YOLO를 이용한 커스텀 데이터 트레이닝
    * https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects
 * YOLO 설치
    * https://wiserloner.tistory.com/m/1247
 * 참고했던 이전의 수어번역 프로그램
    * https://www.youtube.com/watch?v=7XLu7p8Vatg&t=16s
 * 정확도 확인
    * https://github.com/Cartucho/mAP
 * 라벨링 툴
    * https://github.com/tzutalin/labelImg
