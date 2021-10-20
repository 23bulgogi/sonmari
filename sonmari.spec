# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['sonmari.py'],
             pathex=['D:\\Yolo_v4\\darknet\\build\\darknet\\x64'],
             binaries=[],
             datas=[('yolo_cpp_dll_no_gpu.dll', '.'), ('backup/yolov4-obj_96_best.weights', 'backup'), ('yolo_cpp_dll_no_gpu.exp', '.'), ('yolo_cpp_dll_no_gpu.lib', '.'), ('yolo_cpp_dll_no_gpu.pdb', '.'), ('darknet.py', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='sonmari',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='logo.ico')
