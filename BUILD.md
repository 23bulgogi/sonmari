## 1. 해당 zip 파일 클론 후 압축 해제

## 2. 다운받은 폴더 내에서 cmd 창 열고 exe파일로 변환
(pyinstaller는 미리 설치되어야 함)
pyinstaller --icon=logo.ico -F sonmari.py

## 3. yolo_cpp_dll_no_gpu.vcxproj를 비주얼스튜디오로 열고 release 모드로 빌드하면 dll파일 생성. 해당 dll을 손마리 폴더로 이동
