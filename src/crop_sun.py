import glob
import argparse
import modules.FindSunCoordinates as FSC
import cv2
import os
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("job_pathPattern", help="The directory pattern where your Sun pictures will be cropped from")
parser.add_argument("-t", "--threshold", help="Threshold of min pixel value to consider as part of the solar disk", type=int, default=50)
parser.add_argument("-m", "--margin", help="Margin around the Solar Limb", type=int, default=50)
args = parser.parse_args()

filenames_list = glob.glob(args.job_pathPattern)

if len(filenames_list) == 0:
    raise RuntimeError("Directory pattern '%s' doesn't return any files" %args.job_pathPattern)

job_root_path=os.path.abspath(os.path.join(filenames_list[0], os.pardir))
wds_path=os.path.join(job_root_path, "wolfdotsolar")
job_path=os.path.join(wds_path, "crop")

if os.path.isdir(job_path) == False:
    os.makedirs(job_path)

steps_labels = [ "Finding Sun Coordinates", "Cropping Sun Images" ]
max_label_length = max(len(step_label) for step_label in steps_labels)

progress_bar_find = tqdm(total=len(filenames_list), desc=steps_labels[0].rjust(max_label_length, " "), unit="image", ascii=False, colour="blue")
progress_bar_find.update(0)

progress_bar_crop = tqdm(total=len(filenames_list), position=1, desc=steps_labels[1].rjust(max_label_length, " "), ascii=False, colour="blue")
progress_bar_crop.update(0)

max_radius = 0
sun_coordinates = []

for image_file in filenames_list:
    center, radius = FSC.find_disk_in_image_file(image_file=image_file, threshold=args.threshold)
    sun_coordinates.append({ "file": image_file, "center": center })
    progress_bar_find.set_postfix(file=image_file, x=center[0], y=center[1], r=radius)
    progress_bar_find.update(1)
    if radius > max_radius:
        max_radius = radius

progress_bar_find.colour = "green"
progress_bar_find.set_postfix(None)

for sun_coordinate in sun_coordinates:
    file_path = sun_coordinate["file"]
    img = cv2.imread(file_path)
    radius = max_radius + args.margin
    x_center = sun_coordinate["center"][0]
    y_center = sun_coordinate["center"][1]
    x = round(x_center - radius)
    y = round(y_center - radius)
    crop_img = img[y:y+radius*2, x:x+radius*2]
    crop_img_path=os.path.join(job_path, os.path.basename(file_path))
    cv2.imwrite(crop_img_path, crop_img)
    progress_bar_crop.update(1)
progress_bar_crop.colour = "green"

progress_bar_find.close()
progress_bar_crop.close()