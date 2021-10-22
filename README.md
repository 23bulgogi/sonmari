# Sonmari

Open-source Sign language translator using deep learning model

[![GitHub version](https://badge.fury.io/gh/23bulgogi%2Fsonmari.svg)](https://badge.fury.io/gh/23bulgogi%2Fsonmari)

## 수어번역기 손마리

<img src="https://user-images.githubusercontent.com/74365895/132082420-573b5459-bdbd-4ee7-b9ad-afab2ce75651.gif"  width="800" height="450">

### Demo on [YouTube](https://youtu.be/v-RnQI9o_Uk) 

## Info

수어를 한국어로 번역해주는 병원용 수어 번역 프로그램으로 의료 통역사가 부족한 상황에서 청각장애인이 진료를 받을 때 통역사의 도움 없이 독립적으로 진료를 받을 수 있도록 하는 것이 목적이다. 프로그램을 사용하여 의사가 청각장애인의 수어를 이해할 수 있도록 디자인했다.

## Role

카메라를 통해 수어 영상이 입력으로 들어오면 그 영상을 한국어 문자언어로 실시간 번역하여 화면에 출력한다.    
예를 들어 ‘설사’, ‘감기’, ‘콧물’ 등의 수어 동작을 카메라에 비추면, 이 모션을 인식하여 해당 의미의 한국어로 화면에 출력해준다. 또한 이 프로그램에서는 '리셋' 동작을 별도로 지정해두었다. 사용자가 '리셋' 동작을 취할 때까지 출력된 단어들을 화면 위에 모두 보여주어, 문장 수준의 이해가 가능하도록 했다.


## Build Guide


### Requirements
Download all following requirements.
 - Python 3.7 and pip https://www.python.org/downloads/
 - openCV 4.1.0 download https://opencv.org/releases/
 - Visual Studio 2019 https://visualstudio.microsoft.com/ko/downloads/
 - CMAKE https://cmake.org/download/
 - PyQt5
 ```
 pip install PyQt5
 ```

### Install OpenCV
Download openCV 4.1.0 source at https://opencv.org/releases/ and unzip the file.

 

### Install opencv-contrib
```
git clone https://github.com/opencv/opencv_contrib
```
Unzip the file and Copy 'opencv-contrib' folder into 'opencv' directory.


### Make OpenCV
Open CMAKE-gui, and Click Browse-source and Choose 'opencv/sources' directory.
Click Browse-build and Choose 'opencv/build' directory.

Configure-> visual studio 16 2019, x64

If you wait, you will see a red list. It takes a long.
Check 'BUILD_opencv_world' in the red list and Click generate.


### Build OpenCV
```
cd opencv/build
```
Open 'ALL_BUILD.vcxproj' with Visual Studio.

Build mode -> release.
If you look at 'solution explorer' then you can see ALL_BUILD in CMakeTarget. 
Right click 'ALL_BUILD' and build. 
Then right click 'install' and build also.

 

### Clone YoloV4

```
git clone https://github.com/AlexeyAB/darknet
```



### Copy dll files and paste to darknet\build\darknet\x64
```
cd opencv\build\bin\Release
```
Copy 'opencv_ffmpeg410_64.dll', 'opencv_world410.dll' into darknet\build\darknet\x64


### Compile Yolo

Open 'yolo_cpp_dll_no_gpu.vcxproj' in Visual studio and Change Compile mode to 'Release x64'
Then build dll file.

### Compile Darknet

Open darknet.sln with Visual studio.
compile mode-> release x64

Right click 'darknet.sln' and click the 'property'

Then click C/C++ ->general->Additional include directories
Add 'opencv\build\install\include' (Find opencv path).

Click Linker->general->Additional include directories
Add 'opencv\build\install\x64\vc16\lib' (Find opencv path).

Save and build the solution.


### Move into 'darknet/build/darknet/x64'
```
cd darknet/build/darknet/x64
```

### Clone Sonmari and unzip the file
```
git clone https://github.com/23bulgogi/sonmari.git
```

### Move Sonmari/src files into 'darknet/build/darknet/x64'

```
move src/* ../..
move src/cfg ../..
move src/model ../..
move src/data ../..
```

### Run sonmari.py 
```
sonmari.py
```


## Contribution Guide

Contributing to sonmari : [HOW TO CONTRIBUTE](https://github.com/23bulgogi/sonmari/blob/main/CONTRIBUTING.md) 



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
 
 CUDA and cuDnn are not essential when you executing the program using cpu,
 But gpu,CUDA,cuDnn are essential to train using this program.


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
