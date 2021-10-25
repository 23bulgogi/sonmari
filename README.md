# Sonmari

Open-source Sign language translator using deep learning model

[![GitHub version](https://badge.fury.io/gh/23bulgogi%2Fsonmari.svg)](https://badge.fury.io/gh/23bulgogi%2Fsonmari)

## Sonmari Demo

<img src="https://user-images.githubusercontent.com/74365895/132082420-573b5459-bdbd-4ee7-b9ad-afab2ce75651.gif"  width="800" height="450">

### Full demo on [YouTube](https://youtu.be/vU0wX_ToSsw) 

## Info

This is a hospital sign language translation program that translates sign language into Korean, and the purpose is to allow deaf people to be independent of translators for there treatment in a situation where medical interpreters are insufficient. We designed this program so that doctors can understand the sign language of the deaf by using this program.


## Role

When a sign language image is input through the camera, the meaning is translated into Korean text language in real time and displayed on the program screen.
For example, if you show the camera the sign language movements such as diarrhea, cold, and runny nose, this motion is recognized and the meaning is displayed on the screen in Korean words. In addition, we added the 'reset' action separately in this program for initializing all outputs. Until the program recognizing the 'reset' action, all the translated words are displayed on the screen to be understood in the form of a simple sentence.


## Build Guide


### Requirements
Download all following requirements.
 - Python 3.7 and pip https://www.python.org/downloads/
 - openCV 4.1.0 download https://opencv.org/releases/
 - Visual Studio 2019 https://visualstudio.microsoft.com/ko/downloads/
 - CMAKE https://cmake.org/download/
 - git
 - PyQt5
 - numpy
 ```
 pip install PyQt5
 ```
 ```
 pip install numpy
 ```

### Install OpenCV
Download openCV 4.1.0 'sources' at https://opencv.org/releases/ and unzip the file.

unzip downloaded file and rename 'opencv-4.*.*' folder into 'opencv'

```
cd opencv
```

### Install opencv-contrib
```
git clone https://github.com/opencv/opencv_contrib
```
Install 'opencv-contrib' in 'opencv' directory.


### Make OpenCV
Make a directory in 'opencv'.
```
mkdir build
```
Then open CMAKE-gui, and Click Browse-source and Choose 'opencv' directory.
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

Go back to darknet\build\darknet and Open 'yolo_cpp_dll_no_gpu.vcxproj' in Visual studio and Change Compile mode to 'Release x64'
Then build dll file.

### Compile Darknet

Open darknet_no_gpu.sln with Visual studio.
compile mode-> release x64

Right click 'darknet_no_gpu.sln' and click the 'property'

Then click C/C++ ->general->Additional include directories
Add 'opencv\build\install\include' (Find opencv path).

Click Linker->general->Additional library directories
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

 * Custom Data training using YOLOv4
    * https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects
 * YOLOv4 installation
    * https://wiserloner.tistory.com/m/1247
 * The previous sign language translation program
    * https://www.youtube.com/watch?v=7XLu7p8Vatg&t=16s
 * Test Accuracy
    * https://github.com/Cartucho/mAP
 * Labelling tool [labelImg]
    * https://github.com/tzutalin/labelImg
