#!/usr/bin/env python3

####################################################################
# This script was forked from the original work of maitek          #
# Original Author profile : https://github.com/maitek              #
# Original Code : https://github.com/maitek/image_stacking         #
# Original Date : October 5, 2017                                  #
# License : MIT                                                    #
####################################################################
import os
import cv2
import numpy as np
from time import time
from tqdm import tqdm
import argparse

# Align and stack images with ECC method
# Slower but more accurate


def stack_images_ecc(file_list):
    progress_bar_stack = tqdm(total=len(file_list), desc="Stacking Cropped Images (ECC Method)".ljust(
        40, " "), unit="image", ascii=False, colour="blue")
    progress_bar_stack.update(0)

    M = np.eye(3, 3, dtype=np.float32)

    first_image = None
    stacked_image = None

    for file in file_list:
        progress_bar_stack.set_postfix(file=file)
        progress_bar_stack.update(1)

        image = cv2.imread(file, 1).astype(np.float32) / 255
        if first_image is None:
            # convert to gray scale floating point image
            first_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            stacked_image = image
        else:
            # Specify the number of iterations.
            number_of_iterations = 10

            # Specify the threshold of the increment
            # in the correlation coefficient between two iterations
            termination_eps = 1e-10

            # Define termination criteria
            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                        number_of_iterations,  termination_eps)

            # Estimate perspective transform
            s, M = cv2.findTransformECC(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), first_image,
                                        M, cv2.MOTION_HOMOGRAPHY, criteria, inputMask=None, gaussFiltSize=1)
            w, h, _ = image.shape
            # Align image to first image
            image = cv2.warpPerspective(image, M, (h, w))
            stacked_image += image

    progress_bar_stack.colour = "green"
    progress_bar_stack.set_postfix(None)
    progress_bar_stack.close()

    stacked_image /= len(file_list)
    stacked_image = (stacked_image*255).astype(np.uint8)
    return stacked_image


# Align and stack images by matching ORB keypoints
# Faster but less accurate
def stack_images_keypoint_matching(file_list):
    progress_bar_stack = tqdm(total=len(file_list), desc="Stacking Cropped Images (ORB Method)".ljust(
        40, " "), unit="image", ascii=False, colour="blue")
    progress_bar_stack.update(0)

    orb = cv2.ORB_create()

    # disable OpenCL to because of bug in ORB in OpenCV 3.1
    cv2.ocl.setUseOpenCL(False)

    stacked_image = None
    first_image = None
    first_kp = None
    first_des = None
    for file in file_list:
        progress_bar_stack.set_postfix(file=file)
        progress_bar_stack.update(1)

        image = cv2.imread(file, 1)
        image_f = image.astype(np.float32) / 255

        # compute the descriptors with ORB
        kp = orb.detect(image, None)
        kp, des = orb.compute(image, kp)

        # create BFMatcher object
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        if first_image is None:
            # Save keypoints for first image
            stacked_image = image_f
            first_image = image
            first_kp = kp
            first_des = des
        else:
            # Find matches and sort them in the order of their distance
            matches = matcher.match(first_des, des)
            matches = sorted(matches, key=lambda x: x.distance)

            src_pts = np.float32(
                [first_kp[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32(
                [kp[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

            # Estimate perspective transformation
            M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
            w, h, _ = image_f.shape
            image_f = cv2.warpPerspective(image_f, M, (h, w))
            stacked_image += image_f

    progress_bar_stack.colour = "green"
    progress_bar_stack.set_postfix(None)
    progress_bar_stack.close()

    stacked_image /= len(file_list)
    stacked_image = (stacked_image*255).astype(np.uint8)
    return stacked_image


def stack_pictures(input_dir, output_image, method="ECC"):
    image_folder = input_dir
    if not os.path.exists(image_folder):
        print("ERROR {} not found!".format(image_folder))
        exit()

    file_list = os.listdir(image_folder)
    file_list = [os.path.join(image_folder, x)
                 for x in file_list if x.endswith((".jpg", ".png"))]

    if method is not None:
        method = str(method)
    else:
        method = "KP"

    if method == "ECC":
        # Stack images using ECC method :
        stacked_image = stack_images_ecc(file_list)
    elif method == "ORB":
        # Stack images using ORB keypoint method :
        stacked_image = stack_images_keypoint_matching(file_list)
    else:
        print("ERROR: method {} not found!".format(method))
        exit()

    # Checking that parent directory exists :
    parent_dir = os.path.abspath(os.path.join(output_image, os.pardir))
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir)

    # Saving image :
    cv2.imwrite(str(output_image), stacked_image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Input directory of images ()")
    parser.add_argument("output_image", help="Output image name")
    parser.add_argument(
        "--method", help="Stacking method ORB (faster) or ECC (more precise)", default="ECC")
    args = parser.parse_args()
    stack_pictures(args.input_dir, args.output_image, args.method)
