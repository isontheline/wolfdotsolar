#!/usr/bin/env python3

import argparse
import os
import cv2


def sharp(source_file, destination_file):
    if os.path.isfile(source_file) == False:
        raise RuntimeError("File '%s' doesn't exists" % source_file)
    
    img = cv2.imread(source_file)
    if img is None:
        raise RuntimeError(f"Failed to read the image from '{source_file}'")
    
    gaussian_3 = cv2.GaussianBlur(img, (0, 0), 2.0)
    unsharp_image = cv2.addWeighted(img, 2.0, gaussian_3, -1.0, 0)
    cv2.imwrite(destination_file, unsharp_image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file", help="The image to sharp")
    parser.add_argument("destination_file", help="The output image file")
    
    args = parser.parse_args()
    sharp(args.source_file, args.destination_file)
