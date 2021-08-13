import argparse
from converter import Converter

mkdir = 'mkdir test2'
videofile = "GH011020.MP4"
output_dir = "output"
interval = 5 # interval in seconds

if __name__ == '__main__':
    # Example:
    # mp4togeoimg -i GH011021.MP4

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--input", type=str, help="input mp4", required=True)
    parser.add_argument("-o", "--output", type=str, help="output directory for images")
    parser.add_argument("-iv", "--interval", type=int, help="interval in seconds at which the photos need to be filtered")
    # parser.add_argument("-f", "--format", type=str, help="output format (jpg/png/tif)")
    args = parser.parse_args()

    data = {}
    data["input_file"] = args.input
    if args.output:
        data["output_dir"] = args.output
    if args.interval:
        data["interval"] = args.interval
    # if args.format:
    #     data["output_format"] = args.format

    c = Converter(**data)
    c.write_gpx()
    c.import_gpx()
    c.convert_to_photos()
    c.add_metadata()



