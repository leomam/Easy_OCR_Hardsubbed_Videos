# Easy_OCR_Hardsubbed_Videos
An easy way to retrieve subs or text in a video (currently in early stage)

## Install Linux Manjaro
```shell
sudo pacman -Syu --noconfirm && sudo pacman -S \
    tesseract \
    tesseract-data-eng \
    tesseract-data-fra \
    tesseract-data-spa \
    tesseract-data-ita \
    tesseract-data-jpn --noconfirm
```

## Install Linux Kali
```shell
$ sudo apt update -y && sudo apt upgrade -y
$ sudo apt install \
    tesseract-ocr \
    python3-pil \
    tesseract-data-eng \
    tesseract-data-fra \
    tesseract-data-spa \
    tesseract-data-ita \
    tesseract-data-jpn
```

## In your Terminal
```shell
$ pip install opencv-python pytesseract srt
```

## Usage
In headers.py, change the first line `VIDEO_PATH = ""` with the path/of/file.mp4

You can put other video format `VIDEO_EXTENSION_ARRAY = ['mp4','mkv','avi']`

```shell
$ python3 run.py
```
It can take a lot of time and storage (it currently extract 1 frame every 24 frames so usually 1 frame every second).

When it's done, please check all the subbtitle, OCR is not accurate as a human.

Note that this project is in early access, a lot of issue can appear.