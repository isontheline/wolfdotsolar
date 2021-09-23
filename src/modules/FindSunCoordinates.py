#!/usr/bin/env python3
#####################################################################################
# This script was forked from the original work of LandingEllipse                   #
# Original Author profile : https://stackoverflow.com/users/5613422/landingellipse  #
# Original Code : https://stackoverflow.com/a/43530769/8102448                      #
# Original Date : April 20, 2017                                                    #
# License : CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0/            #
#####################################################################################
import cv2
import argparse
import os.path

def find_disk_in_image_file(image_file, threshold=10):
    image = cv2.imread(image_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return find_disk(img=gray, threshold=threshold)

def find_disk(img, threshold=10):
    """Finds the center and radius of a single solar disk present in the supplied image.

    Uses cv2.inRange, cv2.findContours and cv2.minEnclosingCircle to determine the centre and 
    radius of the solar disk present in the supplied image.

    Args:
        img (numpy.ndarray): greyscale image containing a solar disk against a background that is below `threshold`.
        threshold (int): threshold of min pixel value to consider as part of the solar disk

    Returns:
        tuple: center coordinates in x,y form (int) 
        int: radius
    """
    if img is None:
        raise TypeError("img argument is None - check that the path of the loaded image is correct.")

    if len(img.shape) > 2:
        raise TypeError("Expected single channel (grayscale) image.")

    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    mask = cv2.inRange(blurred, threshold, 255)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find and use the biggest contour
    r = 0
    for cnt in contours:
        (c_x, c_y), c_r = cv2.minEnclosingCircle(cnt)
        if c_r > r:
            x = c_x
            y = c_y
            r = c_r

    if x is None:
        raise RuntimeError("No disks detected in the image.")

    return (round(x), round(y)), round(r)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("imageFilePath", help="The input image file path to extract the sun position")
    parser.add_argument("-s", "--superimposeFilePath", help="The output image file path where you want the detected disk superimposed on")
    parser.add_argument("-t", "--threshold", help="Threshold of min pixel value to consider as part of the solar disk", type=int, default=50)
    args = parser.parse_args()

    if os.path.isfile(args.imageFilePath) == False:
        raise RuntimeError("File '%s' doesn't exist" %args.imageFilePath)

    center, radius = find_disk_in_image_file(image_file=args.imageFilePath, threshold=args.threshold)

    print("Sun circle center x, y : {}, {}".format(center[0], center[1]))
    print("Sun circle radius : {}".format(radius))

    # Output the original image with the detected disk superimposed
    if args.superimposeFilePath:
        image = cv2.imread(args.imageFilePath)
        cv2.circle(image, center, radius, (0, 255, 0), 1)
        cv2.rectangle(image, (center[0] - 2, center[1] - 2), (center[0] + 2, center[1] + 2), (0, 255, 0), -1)
        cv2.imwrite(args.superimposeFilePath, image)