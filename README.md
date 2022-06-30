# Easy_OCR_Hardsubbed_Videos
An easy way to retrieve subs or text in a video (currently in early stage)

## Install Linux Manjaro
```shell
$ sudo pacman -Syu --noconfirm && sudo pacman -S tesseract tesseract-data-eng tesseract-data-fra tesseract-data-spa tesseract-data-ita tesseract-data-jpn --noconfirm
```

## Install Linux Kali
```shell
$ sudo apt update -y && sudo apt upgrade -y
$ sudo apt install tesseract-ocr python3-pil tesseract-data-eng tesseract-data-fra tesseract-data-spa tesseract-data-ita tesseract-data-jpn
```

## In your Terminal
```shell
$ pip install opencv-python pytesseract srt
```

## Usage
```shell
$ python3 run.py
```
