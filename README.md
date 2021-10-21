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


## Build Guide


### Requirements
Download all following requirements.
 - 파이썬 3.* 및 pip
 - openCV
 - 비주얼스튜디오 2019
 - pyinstaller
 - pyqt5
 ```
pip install pyinstaller
```
```
pip install PyQt5
```

### Clone main branch and unzip the file

```
git clone https://github.com/23bulgogi/sonmari.git
```
### Move to src directory
```
cd src
```

### Make sonmari.py file into exe file using pyinstaller
```
pyinstaller --onefile --icon=logo.ico sonmari.py
```
Then you can see sonmari.exe in dist directory. 

### Move "sonmari.exe" file out of the dist directory.

### Install yolo and darknet
내용 보충할것
visual studio를 이용해 yolo_cpp_dll_no_gpu.vcxproj를 release 모드로 빌드, 생성된 dll 파일을 모두 sonmari.exe가 위치한 폴더로 이동시킴

### Run sonmari.exe 
```
sonmari.exe
```


## Contribution Guide

Contributing to sonmari : [HOW TO CONTRIBUTE](https://github.com/23bulgogi/sonmari/blob/main/CONTRIBUTING.md) 


## Quickly Start

Clone releases branch and unzip the file. 
Then you can see "sonmari.exe" file. 
Click the file then you can run the program easily.

```
sonmari.exe
```


## Development Guide

### Prerequistics
 * WebCam
 * GPU (for training)
    * For testing, GPU is not needed.

### Development Environment
 - Python 3.6
 - OpenCV 3.x
 - CMAKE 3.18
 - CUDA 10.2
 - cuDNN 8.0.2
 - PYQT5

cpu를 이용해 해당 프로그램을 실행시킬 때는 CUDA와 cuDNN이 필수적이지 않으나,
본 프로그램을 이용해 직접 트레이닝하고 확장시키려면 gpu와 CUDA, CuDNN이 필수적임.

### Code of conduct
View [Code of conduct](https://github.com/23bulgogi/sonmari/blob/main/CODE_OF_CONDUCT.md) for community guidelines.

### How to training
Refer https://github.com/23bulgogi/sonmari/wiki/How-to-Training


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
