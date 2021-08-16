# video2geoimg
Convert your geotagged videos to georeferenced still frames using python! This project is largely based on FFmpeg and ExifTool.

## Installation
### Requirements
- [Python](https://www.python)
- [FFmpeg](https://www.ffmpeg.org/) 
- [ExifTool](https://exiftool.org/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [geopy](https://github.com/geopy/geopy) (optional)

### Installation instructions 
This is currently only tested on windows.

- Download FFmpeg at: https://www.ffmpeg.org/download.html and follow installation instructions. 
I used the [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) build.
- Download Exiftool at: https://exiftool.org/ and follow installation instructions.
- Add the folder with ExifTool.exe and the folder with FFmpeg.exe to your PATH environment variables. 
- In git bash type:

`python -m pip install 'git+https://github.com/LaurensJN/video2geoimg.git' --user`

## Usage
```
usage: python -m video2geoimg.video2geoimg [-h] -i INPUT [-o OUTPUT] [-iv INTERVAL] [-m {METERS,SECONDS}]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input mp4
  -o OUTPUT, --output OUTPUT
                        output directory for images
  -iv INTERVAL, --interval INTERVAL
                        interval at which the photos need to be filtered (default is 5)
  -m {METERS,SECONDS}, --method {METERS,SECONDS}
                        unit that is used to calculate where to take the frames (default is SECONDS)
```
Example takes my_video as input and puts photos at a 2 sec interval in the geo-photos directory:

`python -m video2geoimg -i my_video.mp4 -o "geo-photos" -iv 2`

The output format is currently always JPG, because PNG does not work well with georeferenced photos and for some reason ExifTool does not like TIF images.

## License
This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version ([See License](LICENSE)).
