import glob
import argparse
import modules.FindSunCoordinates as FSC
import cv2
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("jobPathPattern", help="The directory pattern where your Sun pictures will be cropped from")
parser.add_argument("-t", "--threshold", help="Threshold of min pixel value to consider as part of the solar disk", type=int, default=50)
parser.add_argument("-m", "--margin", help="Margin around the Solar Limb", type=int, default=50)
args = parser.parse_args()

filenames_list = glob.glob(args.jobPathPattern)

if len(filenames_list) == 0:
    raise RuntimeError("Directory pattern '%s' doesn't return any files" %args.jobPathPattern)

steps_labels = [ "Finding Sun Coordinates", "Cropping Sun Images" ]
max_label_length = max(len(step_label) for step_label in steps_labels)

pbar_find = tqdm(total=len(filenames_list), desc=steps_labels[0].rjust(max_label_length, " "), unit="image", ascii=False, colour="blue")
pbar_find.update(0)

pbar_crop = tqdm(total=len(filenames_list), position=1, desc=steps_labels[1].rjust(max_label_length, " "), ascii=False, colour="blue")
pbar_crop.update(0)

max_radius = 0
sun_coordinates = []

for image_file in filenames_list:
    center, radius = FSC.find_disk_in_image_file(image_file=image_file, threshold=args.threshold)
    sun_coordinates.append({ "file": image_file, "center": center })
    pbar_find.set_postfix(file=image_file, x=center[0], y=center[1], r=radius)
    pbar_find.update(1)
    if radius > max_radius:
        max_radius = radius

pbar_find.colour = "green"
pbar_find.set_postfix(None)

for sun_coordinate in sun_coordinates:
    img = cv2.imread(sun_coordinate["file"])
    radius = max_radius + args.margin
    x_center = sun_coordinate["center"][0]
    y_center = sun_coordinate["center"][1]
    x = round(x_center - radius)
    y = round(y_center - radius)
    crop_img = img[y:y+radius*2, x:x+radius*2]
    cv2.imwrite("/imgs/test.jpg", crop_img)
    pbar_crop.update(1)
pbar_crop.colour = "green"

pbar_find.close()
pbar_crop.close()