import os
import subprocess
import ffmpeg
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import math

EXIFTOOL = "exiftool"


# FFMPEG = "./ffmpeg/bin/ffmpeg.exe"

class Converter:
    def __init__(self, input_file, output_dir=None, interval=10, output_format="jpg", method="SECONDS"):
        self.input_file = input_file
        self.stripped_input, self.extension = os.path.splitext(input_file)
        self.gps_file = None
        self.gps_data = None
        self.photos = []
        self.interval = interval
        self.output_format = output_format
        self.timestamp = None
        self.method = method

        if output_dir is not None:
            self.output_dir = output_dir + "/"
        else:
            self.output_dir = self.stripped_input + "/"
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def write_gpx(self):
        cline = f"{EXIFTOOL} -p fmt_file/gpx.fmt -ee {self.input_file} > {self.output_dir}out.gpx"
        os.system(cline)
        self.gps_file = f"{self.output_dir}out.gpx"

    def import_gpx(self):
        with open(self.gps_file) as f:
            gps_data_raw = BeautifulSoup(f, 'html.parser')
        gps_data_unsorted = [{'lat': float(coord['lat']),
                              'lon': float(coord['lon']),
                              'time': self.extract_gpx_timestamp(coord.time.text)}
                             for coord in gps_data_raw.find_all('trkpt')
                             if coord.time is not None]

        self.gps_data = sorted(gps_data_unsorted, key=lambda item: item["time"])
        self.timestamp = self.gps_data[0]["time"]

    def convert_to_photos(self):
        if self.method == "SECONDS":
            self.convert_to_photos_seconds()
            self.add_metadata()
        elif self.method == "METERS":
            self.convert_to_photos_meters()
        else:
            print("The method is not valid. Please select METERS or SECONDS.")
            return

        self.add_photo_georeferencing()

    def convert_to_photos_seconds(self):
        stream = (ffmpeg
                  .input(self.input_file)
                  .filter("fps", fps=1 / self.interval)
                  .output(f"{self.output_dir}{self.stripped_input}-%d.{self.output_format}")
                  )
        stream.run()
        return

    def convert_to_photos_meters(self):
        try:
            from geopy.distance import geodesic
            using_geopy = True
        except ImportError as err:
            print(f"{err}. Using the manual method (less accurate)...")
            using_geopy = False

        prev_tp = self.gps_data[0]
        i = 0
        photos = []
        for tp in self.gps_data:
            # first photo will always be converted.
            if using_geopy:
                distance = geodesic((tp["lat"], tp["lon"]), (prev_tp["lat"], prev_tp["lon"])).meters
            else:
                distance = self.latlon_distance((tp["lat"], tp["lon"]), (prev_tp["lat"], prev_tp["lon"]))

            if distance > self.interval:
                i += 1
                photo = self.convert_to_photo(tp["time"], i)
                prev_tp = tp
                self.add_photo_metadata(photo, tp["time"])
                photos.append(photo)
        return photos

    def convert_to_photo(self, timestamp, idx):
        timestamp_in_seconds = timestamp - self.timestamp
        output_file = f"{self.output_dir}{self.stripped_input}-{idx}.{self.output_format}"

        stream = ffmpeg.input(self.input_file)
        # TODO following code is not clean. Should find a better solution.
        ffmpeg.nodes.get_stream_spec_nodes(stream)[0].kwargs['ss'] = str(timestamp_in_seconds)

        stream = stream.output(output_file, frames=1)
        stream.run(overwrite_output=True)

        return output_file

    def add_metadata(self):
        photo_idx = 1
        photos = []
        while True:
            photo = f"{self.output_dir}{self.stripped_input}-{photo_idx}.{self.output_format}"
            if not os.path.isfile(photo):
                return photos

            td = timedelta(seconds=(photo_idx - 1) * self.interval)
            timestamp = self.timestamp + td
            # geolocation = self.retrieve_geolocation(timestamp)
            self.add_photo_metadata(photo, timestamp)
            photo_idx += 1
            photos.append(photo)

    def add_photo_metadata(self, photo, timestamp):
        timestamp_string = self.datetime_to_exiftool(timestamp)
        cline = f'{EXIFTOOL} {photo} "-CreateDate={timestamp_string}" "-FileCreateDate={timestamp_string}" {photo}'
        print(cline)
        os.system(cline)

    def add_photo_georeferencing(self):
        cline = f'{EXIFTOOL} -v2 -geotag "{self.output_dir}out.gpx" "-geotime<${{createdate}}+00:00" {self.output_dir}'
        # cline = f'exiftool -v2 -geotag "{self.input_file}" "-xmp:geotime<createdate" {self.output_dir}'
        print(cline)
        os.system(cline)

    @staticmethod
    def datetime_to_exiftool(timestamp):
        return timestamp.strftime("%Y:%m:%d %H:%M:%S")  # TODO: should fix the UTC issue

    @staticmethod
    def extract_metadata_timestamp(input_file):
        cline = f"{EXIFTOOL} -s -time:CreateDate {input_file}"
        (out, err) = subprocess.Popen(cline, stdout=subprocess.PIPE, shell=True).communicate()
        if err:
            print(err)

        dt_string = str(out).split(" : ")[-1][:-5]
        return datetime.strptime(dt_string, "%Y:%m:%d %H:%M:%S")

    @staticmethod
    def extract_gpx_timestamp(timestamp):
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

    @staticmethod
    def latlon_distance(origin, destination):
        """
        Calculate the Haversine distance. From https://stackoverflow.com/a/38187562/12479748.

        Parameters
        ----------
        origin : tuple of float
            (lat, long)
        destination : tuple of float
            (lat, long)

        Returns
        -------
        distance_in_m : float
        """
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371000  # in meter

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c

        return d
