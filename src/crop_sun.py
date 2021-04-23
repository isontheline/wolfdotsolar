import glob
import argparse
import modules.FindSunCoordinates as FSC

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("jobPathPattern", help="The directory pattern where your Sun pictures will be cropped from")
parser.add_argument("-t", "--threshold", help="Threshold of min pixel value to consider as part of the solar disk", type=int, default=50)
args = parser.parse_args()

filenamesList = glob.glob(args.jobPathPattern)

if len(filenamesList) == 0:
    raise RuntimeError("Directory pattern '%s' doesn't return any files" %args.jobPathPattern)

with tqdm(total=len(filenamesList), desc="Cropping sun", unit="image", ascii=False, colour="blue") as pbar:
    for imageFile in filenamesList:
        #print(imageFile)
        center, radius = FSC.find_disk_in_image_file(image_file=imageFile, threshold=args.threshold)
        #print("Sun circle center x, y : {}, {}".format(center[0], center[1]))
        #print("Sun circle radius : {}".format(radius))
        pbar.update(1)