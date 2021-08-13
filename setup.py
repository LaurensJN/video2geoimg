import runpy

import logging
from setuptools import setup, find_packages

# Retrieve __version__ from the package.

PACKAGE_NAME = "video2geoimg"
VERSION = runpy.run_path("video2geoimg/version.py")["__version__"]
DESCRIPTION = "video2geoimg: Convert your geotagged videos to georeferenced still frames using python"
URL = "https://github.com/LaurensJN/video2geoimg"
AUTHOR = "L.J.N. Oostwegel"
LICENSE = "GNU General Public License v3.0 or later"
DOWNLOAD_URL = ""
LONG_DESCRIPTION = """
A longer description of what the library does. This will appear on pypi, and also influence
search keywords etc. (Maybe 1-2 paragraphs long)
"""
CLASSIFIERS = [
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: Science/Research",
    "Operating System :: Windows",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Software Development :: Libraries",
]


logger = logging.getLogger()
logging.basicConfig(format="%(levelname)s - %(message)s")


def get_requirements():
    packages = None
    with open("requirements.txt") as f:
        packages = f.read().splitlines()
    return packages


if __name__ == "__main__":

    setup(
        # Metadata
        name=PACKAGE_NAME,
        version=VERSION,
        author=AUTHOR,
        description=DESCRIPTION,
        url=URL,
        long_description=LONG_DESCRIPTION,
        licence=LICENSE,
        python_requires=">3.6",
        # Package info
        packages=find_packages(exclude=("docs", "test", "examples", "fmt_file")),
        install_requires=get_requirements(),
        zip_safe=True,
        include_dirs=[],
        classifiers=CLASSIFIERS,
    )