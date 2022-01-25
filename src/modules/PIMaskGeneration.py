#!/usr/bin/env python3

import argparse
import os
from PIL import Image, ImageDraw

try:
    import modules.FindSunCoordinates as FSC
except ModuleNotFoundError:
    import FindSunCoordinates as FSC


def createPIMask(image_file, threshold=50):
    if os.path.isfile(image_file) == False:
        raise RuntimeError("File '%s' doesn't exists" % image_file)

    imSource = Image.open(image_file)

    source_parent_path = os.path.abspath(
        os.path.join(image_file, os.pardir))
    source_file_name_split = os.path.splitext(os.path.basename(image_file))
    destination_file_name = source_file_name_split[0] + "-mask.png"
    destination_file_path = os.path.join(
        source_parent_path, destination_file_name)

    center, radius = FSC.find_disk_in_image_file(
        image_file=image_file, threshold=threshold)
    im = Image.new('L', imSource.size, "black")
    draw = ImageDraw.Draw(im)
    print(center)
    print(radius)
    shape = [(center[0] - radius, center[1] - radius),
             (center[0] + radius, center[1] + radius)]
    draw.ellipse(shape, fill="white", outline="black", width=8)
    im.save(destination_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "image_file", help="The image to create a Pixinsight related mask")
    args = parser.parse_args()
    createPIMask(args.image_file)
