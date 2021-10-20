#!/usr/bin/env python3

import argparse
from PIL import Image
import piexif


def copy_exif(src_copy, dst_paste):
    # Extract EXIF from source image file :
    im = Image.open(src_copy)
    exif_dict = piexif.load(im.info["exif"])
    exif_bytes = piexif.dump(exif_dict)

    # Apply EXIF to the destination image :
    im_dst = Image.open(dst_paste)
    im_dst.save(dst_paste, im.format, exif=exif_bytes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src_copy", help="The image to copy EXIF from")
    parser.add_argument("dst_paste", help="The image to paste EXIF to")
    args = parser.parse_args()
    copy_exif(args.src_copy, args.dst_paste)
