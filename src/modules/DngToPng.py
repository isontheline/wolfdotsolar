#!/usr/bin/env python3

import argparse
import os
import glob
from wand.image import Image


def convert(image_file):
    if os.path.isfile(image_file) == False:
        raise RuntimeError("File '%s' doesn't exists" % image_file)

    with Image(filename=image_file) as img:
        source_parent_path = os.path.abspath(
            os.path.join(image_file, os.pardir))
        source_file_name_split = os.path.splitext(os.path.basename(image_file))
        destination_file_name = source_file_name_split[0] + ".png"
        destination_file_path = os.path.join(
            source_parent_path, destination_file_name)
        img.format = 'png'
        img.save(filename=destination_file_path)
        # Setting creation / modification date on converted image :
        image_timestamp = os.path.getmtime(image_file)
        os.utime(destination_file_path, (image_timestamp, image_timestamp))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "images_search_pattern", help="The search images pattern to convert from DNG to PNG")
    args = parser.parse_args()

    filenames_list = glob.glob(args.images_search_pattern)

    if len(filenames_list) == 0:
        raise RuntimeError("Search images pattern '%s' doesn't return any files" %args.images_search_pattern)

    for image_file in filenames_list:
        convert(image_file)
