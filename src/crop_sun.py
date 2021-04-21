import glob
import argparse
import modules.FindSunCoordinates as FSC

parser = argparse.ArgumentParser()
parser.add_argument("jobPathPattern", help="The directory pattern where your Sun pictures will be cropped from")
args = parser.parse_args()

filenamesList = glob.glob(args.jobPathPattern)

if len(filenamesList) == 0:
    raise RuntimeError("Directory pattern '%s' doesn't return any files" %args.jobPathPattern)

for imageFile in filenamesList:
    print(imageFile, flush= True)
    center, radius = FSC.find_disk_in_image_file(image_file=imageFile)
    print("Sun circle center x, y : {}, {}".format(center[0], center[1]), flush= True)
    print("Sun circle radius : {}".format(radius), flush= True)