# video2geoimg
Convert your geotagged videos to georeferenced still frames using python! This project is largely based on FFmpeg and ExifTool.

## Installation
### Requirements
- [Python](https://www.python)
- [FFmpeg](https://www.ffmpeg.org/) 
- [ExifTool](https://exiftool.org/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)

### Installation instructions 
This is currently only tested on windows.

- Download FFmpeg at: https://www.ffmpeg.org/download.html and follow installation instructions. 
I used the [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) build.
- Download Exiftool at: https://exiftool.org/ and follow installation instructions.
- Add the folder with ExifTool.exe and the folder with FFmpeg.exe to your PATH environment variables. 
- Type in command prompt:

`python -m pip install ffmpeg-python, beautifulsoup4`

## Usage
```
usage: video2geoimg.py [-h] -i INPUT [-o OUTPUT] [-iv INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        geotagged input video
  -o OUTPUT, --output OUTPUT
                        output directory for images
  -iv INTERVAL, --interval INTERVAL
                        interval in seconds at which the photos need to be filtered
```
Example takes my_video as input and puts photos at a 2 sec interval in the geo-photos directory:

`video2geoimg.py -i my_video.mp4 -o "geo-photos" -iv 2`

The output format is currently always JPG, because PNG does not work well with georeferenced photos and for some reason ExifTool does not like TIF images.

## License
Licensed under [GPL-3.0-or-later](LICENSE)
