smart-resizer
=============
Intellectual resizing and croping script. Smart-resizer allows to resize image from one aspect ratio to another (with crop) while leaving important information on it. Script uses saliency map to detect important features.

Help:
```
python iresizer.py -h
usage: iresizer.py [-h] [-o OUTPUT_PATH] [-W WIDTH] [-H HEIGHT] [-c]
                   image_path

Smart resizer

positional arguments:
  image_path      input image path

optional arguments:
  -h, --help      show this help message and exit
  -o OUTPUT_PATH  output file path. By default: result.jpg
  -W WIDTH        new width
  -H HEIGHT       new height
  -c              use crop
```

How to run:
```
python iresizer.py kino.jpg -W 400 -H 500 -c
```

Example
------- 
Input image (680x170):

![alt text](https://github.com/madcat1991/smart-resizer/blob/master/hockey.jpg "Original")

Script call:
```
python iresizer.py hockey.jpg -W 200 -H 300 -c
```

Output image (200x300):

![alt text](https://github.com/madcat1991/smart-resizer/blob/master/hockey_resized.jpg "Resized")