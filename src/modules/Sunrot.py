#!/usr/bin/env python3

import os
import ephem
import math
import datetime
import argparse
from PIL import Image


def parallactic_angle(latitude, longitude, datetime):
    observer = ephem.Observer()
    observer.date = datetime
    observer.lat = math.radians(latitude)
    observer.lon = math.radians(longitude)

    sun = ephem.Sun(observer)
    parallactic_angle = sun.parallactic_angle()

    return -math.degrees(parallactic_angle)


def get_julian_datetime(date):
    """
    https://stackoverflow.com/questions/31142181/calculating-julian-date-in-python
    Convert a datetime object into julian float.
    Args:
        date: datetime-object of date in question

    Returns: float - Julian calculated datetime.
    Raises: 
        TypeError : Incorrect parameter type
        ValueError: Date out of range of equation
    """

    # Ensure correct format
    if not isinstance(date, datetime.datetime):
        raise TypeError(
            'Invalid type for parameter "date" - expecting datetime')
    elif date.year < 1801 or date.year > 2099:
        raise ValueError('Datetime must be between year 1801 and 2099')

    # Perform the calculation
    julian_datetime = 367 * date.year - int((7 * (date.year + int((date.month + 9) / 12.0))) / 4.0) + int(
        (275 * date.month) / 9.0) + date.day + 1721013.5 + (
        date.hour + date.minute / 60.0 + date.second / math.pow(60,
                                                                2)) / 24.0 - 0.5 * math.copysign(
        1, 100 * date.year + date.month - 190002.5) + 0.5

    return julian_datetime


def truncate_angle(angle):
    n = math.floor(angle / 360.0)
    return angle - (n * 360)


def solar_coordinates(datetime):
    jd = get_julian_datetime(datetime)
    radian = 57.29577951308232
    theta = (jd - 2398220.0) * 360.0 / 25.38
    inc = 0.1265363707695889
    k = 73.6667 + 1.3958333 * (jd - 2396758.0) / 36525.0
    t = (jd - 2451545.0) / 36525.0
    t2 = t * t
    t3 = t * t2
    l0 = 280.46645 + 36000.76983 * t + 3.032E-4 * t2
    m = 357.5291 + 35999.0503 * t - 1.559E-4 * t2 - 4.8E-7 * t3
    mr = m / radian
    c = (1.9146 - 0.004817 * t - 1.4E-5 * t2) * math.sin(mr) + (0.019993 -
                                                                1.01E-4 * t) * math.sin(2.0 * mr) + 2.9E-4 * math.sin(3.0 * mr)
    sun_l = l0 + c
    omega = 125.04 - 1934.136 * t
    lngtd = sun_l - 0.00569 - 0.00478 * math.sin(omega / radian)
    diffk = (lngtd - k) / radian
    oblr = (23.4392911 - 0.0130042 * t - 1.64E-5 * t2 + 5.04E-5 * t3) / radian
    tx = -math.cos(lngtd / radian) * math.tan(oblr)
    ty = -math.cos(diffk) * math.tan(inc)
    p = radian * (math.atan(tx) + math.atan(ty))
    b0 = radian * math.asin(math.sin(diffk) * math.sin(inc))
    etay = -math.sin(diffk) * math.cos(inc)
    etax = -math.cos(diffk)
    eta = math.atan2(etay, etax) * radian
    l0 = eta - theta
    l0 = truncate_angle(l0)
    carr_no = math.floor((jd - 2398140.2271) / 27.2752316)

    return {
        "L0": l0,
        "B0": b0,
        "Carrington_Number": carr_no,
        "P": p,
        "JD": jd
    }


def normalize_solar_picture_angles(image_file, year, month, day, hour, minute, latitude, longitude, mount_type="altazimuth"):
    dt = datetime.datetime(year, month, day, hour, minute)
    sc = solar_coordinates(dt)
    if os.path.isfile(image_file) == False:
        raise RuntimeError("File '%s' doesn't exists" % image_file)

    image = Image.open(image_file)

    # P = The position angle between the geocentric north pole and the solar rotational north pole measured eastward from geocentric north.
    # The range in P is +/- 26.3°.
    # http://www.jgiesen.de/sunrot/index.html
    rotation_angle = sc["P"]

    if "altazimuth" == mount_type:
        # One disadvantage of using an altazimuth telescope mounting is that the cardinal points of the Sun (north, east, south and west) are more difficult to determine than if an equatorial type of mounting were used.
        # https://www.petermeadows.com/html/parallactic.html
        pa = parallactic_angle(latitude, longitude, dt)
        rotation_angle += pa

    rotated_image = image.rotate(-rotation_angle)
    source_parent_path = os.path.abspath(os.path.join(image_file, os.pardir))
    source_file_name_split = os.path.splitext(os.path.basename(image_file))
    destination_file_name = source_file_name_split[0] + "-rotated.png"
    destination_file_path = os.path.join(
        source_parent_path, destination_file_name)
    rotated_image.save(destination_file_path, "png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_file", help="The image to rotate")
    parser.add_argument(
        "-y", "--year", help="Year of observation", type=int, required=True)
    parser.add_argument(
        "-m", "--month", help="Month of observation", type=int, required=True)
    parser.add_argument(
        "-d", "--day", help="Day of observation", type=int, required=True)
    parser.add_argument(
        "-H", "--hour", help="Hour of observation", type=int, required=True)
    parser.add_argument(
        "-M", "--minute", help="Minute of observation", type=int, required=True)
    parser.add_argument(
        "-l", "--latitude", help="Latitude of observation", type=float, required=True)
    parser.add_argument(
        "-L", "--longitude", help="Longitude of observation", type=float, required=True)
    parser.add_argument(
        "-t", "--mount", help="Mount type (altazimuth, equatorial)", default="altazimuth")
    args = parser.parse_args()
    normalize_solar_picture_angles(args.image_file, args.year, args.month, args.day,
                                   args.hour, args.minute, args.latitude, args.longitude, args.mount)
