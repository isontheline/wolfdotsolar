###########################################################################
# This script is forked from the original work of LandingEllipse          #
# Author profile : https://stackoverflow.com/users/5613422/landingellipse #
# Code : https://stackoverflow.com/a/43530769/8102448                     #
# Date : April 20, 2017                                                   #
# License : CC BY-SA 3.0 https://creativecommons.org/licenses/by-sa/3.0/  #
###########################################################################
import cv2

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
    image = cv2.imread("/imgs/_pss_sharp.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    center, radius = find_disk(img=gray, threshold=100)

    print("circle x,y: {},{}".format(center[0], center[1]))
    print("circle radius: {}".format(radius))

    # Output the original image with the detected disk superimposed
    cv2.circle(image, center, radius, (0, 0, 255), 1)
    cv2.rectangle(image, (center[0] - 2, center[1] - 2), (center[0] + 2, center[1] + 2), (0, 0, 255), -1)
    cv2.imwrite("/imgs/_pss_sharp_super.png", image)