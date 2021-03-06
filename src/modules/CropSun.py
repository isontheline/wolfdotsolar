#!/usr/bin/env python3

import glob
import argparse
import cv2
import os
from tqdm import tqdm
from PIL import Image

try:
    import modules.FindSunCoordinates as FSC
except ModuleNotFoundError:
    import FindSunCoordinates as FSC

def crop_sun_pictures(job_path_pattern, destination="wolfdotsolar", threshold=50, margin=50):
    filenames_list = glob.glob(job_path_pattern)

    if len(filenames_list) == 0:
        raise RuntimeError("Directory pattern '%s' doesn't return any files" %job_path_pattern)

    job_root_path = os.path.abspath(os.path.join(filenames_list[0], os.pardir))
    job_path = destination

    if not job_path.startswith("/"):
        job_path = os.path.join(job_root_path, destination)

    if not os.path.isdir(job_path):
        os.makedirs(job_path)

    max_radius = 0
    sun_coordinates = []

    # Finding Sun Coordinates :
    progress_bar_find = tqdm(total=len(filenames_list), desc="Finding Sun Coordinates".ljust(40, " "), unit="image", ascii=False, colour="blue")
    progress_bar_find.update(0)
    for image_file in filenames_list:
        center, radius = FSC.find_disk_in_image_file(image_file=image_file, threshold=threshold)
        sun_coordinates.append({ "file": image_file, "center": center })
        progress_bar_find.set_postfix(file=image_file)
        progress_bar_find.update(1)
        if radius > max_radius:
            max_radius = radius
    progress_bar_find.colour = "green"
    progress_bar_find.set_postfix(None)
    progress_bar_find.close()

    # Cropping Sun Images :
    progress_bar_crop = tqdm(total=len(filenames_list), position=1, desc="Cropping Sun Images".ljust(40, " "), unit="image", ascii=False, colour="blue")
    progress_bar_crop.update(0)
    images_timestamps = []
    for sun_coordinate in sun_coordinates:
        file_path = sun_coordinate["file"]
        img = cv2.imread(file_path)
        radius = max_radius + margin
        x_center = sun_coordinate["center"][0]
        y_center = sun_coordinate["center"][1]
        x = round(x_center - radius)
        y = round(y_center - radius)
        # Cropping image :
        crop_img = img[y:y+radius*2, x:x+radius*2]
        crop_img_filename = os.path.splitext(os.path.basename(file_path))[0] + ".png"
        crop_img_path = os.path.join(job_path, crop_img_filename)
        # Writing cropped image :
        cv2.imwrite(crop_img_path, crop_img)
        # Setting creation / modification date on cropped image :
        image_timestamp = os.path.getmtime(file_path)
        os.utime(crop_img_path, (image_timestamp, image_timestamp))
        images_timestamps.append(image_timestamp)
        # Updating progress bar :
        progress_bar_crop.set_postfix(file=file_path)
        progress_bar_crop.update(1)
    progress_bar_crop.colour = "green"
    progress_bar_crop.set_postfix(None)
    progress_bar_crop.close()

    average_timestamp = int(sum(images_timestamps) / len(images_timestamps))
    return { "AverageTimestamp": average_timestamp }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("job_pathPattern", help="The directory pattern where your Sun pictures will be cropped from")
    parser.add_argument("-t", "--threshold", help="Threshold of min pixel value to consider as part of the solar disk", type=int, default=50)
    parser.add_argument("-m", "--margin", help="Margin around the Solar Limb", type=int, default=50)
    parser.add_argument("-d", "--destination", help="Destination subfolder", default="wolfdotsolar")
    args = parser.parse_args()
    crop_sun_pictures(args.job_pathPattern, args.destination, args.threshold, args.margin)