#!/usr/bin/env python3

import argparse
import os
from wand.image import Image


def unsharp(source_file, destination_file, radius=100, sigma=2, amount=3, threshold=0):
    if os.path.isfile(source_file) == False:
        raise RuntimeError("File '%s' doesn't exists" % source_file)

    with Image(filename=source_file) as img:
        img.unsharp_mask(radius=radius, sigma=sigma,
                         amount=amount, threshold=threshold)
        img.save(filename=destination_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file", help="The image to unsharp")
    parser.add_argument("destination_file", help="The output image")
    parser.add_argument(
        "-r", "--radius", help="Unsharp radius", type=int, default=100)
    parser.add_argument(
        "-s", "--sigma", help="Unsharp sigma", type=int, default=2)
    parser.add_argument(
        "-a", "--amount", help="Unsharp amount", type=int, default=3)
    parser.add_argument("-t", "--threshold",
                        help="Unsharp threshold", type=int, default=0)
    args = parser.parse_args()
    unsharp(args.source_file, args.destination_file, args.radius,
            args.sigma, args.amount, args.threshold)
