# Easy_OCR_Hardsubbed_Videos
An easy way to retrieve subs or text in a video (currently in early stage)

## Install Linux Manjaro
```shell
$ sudo pacman -Syu
$ sudo pacman -S tesseract tesseract-data-eng tesseract-data-fra
```

## Install Linux Kali
```shell
$ sudo apt update -y && sudo apt upgrade -y
$ sudo apt install tesseract-ocr python3-pil tesseract-ocr-eng tesseract-ocr-fra
```

## In your Terminal
```shell
$ pip install opencv-python
$ pip install pytesseract
$ pip install srt
```

## Usage
```shell
$ python3 run.py
```
