import argparse
import sys
from video2geoimg.converter import Converter


def cmdline(args=None):
    # Example:
    # mp4togeoimg -i GH011021.MP4
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=str, help="input mp4", required=True)
    parser.add_argument("-o", "--output", type=str, help="output directory for images")
    parser.add_argument("-iv", "--interval", type=int, default=5,
                        help="interval at which the photos need to be filtered (default is 5)")
    parser.add_argument("-m", "--method", type=str, choices=["METERS", "SECONDS"], default="SECONDS",
                        help="unit that is used to calculate where to take the frames (default is SECONDS)")
    # parser.add_argument("-f", "--format", type=str, help="output format (jpg/png/tif)")
    args = parser.parse_args()

    data = {}
    data["input_file"] = args.input
    if args.output:
        data["output_dir"] = args.output
    if args.interval:
        data["interval"] = args.interval
    if args.method:
        data["method"] = args.method
    # if args.format:
    #     data["output_format"] = args.format

    c = Converter(**data)
    c.write_gpx()
    c.import_gpx()
    c.convert_to_photos()


if __name__ == '__main__':
    sys.exit(cmdline())
