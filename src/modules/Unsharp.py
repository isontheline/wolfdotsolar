#!/usr/bin/env python3

import argparse
import os
from wand.image import Image

def unsharp(image_file, radius=100, sigma=2, amount=3, threshold=0):
    if os.path.isfile(image_file) == False:
        raise RuntimeError("File '%s' doesn't exists" %image_file)

    with Image(filename=image_file) as img:
        img.unsharp_mask(radius=radius, sigma=sigma, amount=amount, threshold=threshold)
        source_parent_path=os.path.abspath(os.path.join(image_file, os.pardir))
        source_file_name_split = os.path.splitext(os.path.basename(image_file))
        destination_file_name = source_file_name_split[0] + "-unsharp.png"
        destination_file_path = os.path.join(source_parent_path, destination_file_name)
        img.save(filename=destination_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_file", help="The image to unsharp")
    parser.add_argument("-r", "--radius", help="Unsharp radius", type=int, default=100)
    parser.add_argument("-s", "--sigma", help="Unsharp sigma", type=int, default=2)
    parser.add_argument("-a", "--amount", help="Unsharp amount", type=int, default=3)
    parser.add_argument("-t", "--threshold", help="Unsharp threshold", type=int, default=0)
    args = parser.parse_args()
    unsharp(args.image_file, args.radius, args.sigma, args.amount, args.threshold)