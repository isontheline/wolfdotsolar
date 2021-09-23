#!/usr/bin/env python3

import ephem
import math
import datetime
import argparse

def parallactic_angle(latitude, longitude, datetime):
    observer = ephem.Observer()
    observer.date = datetime
    observer.lat = math.radians(latitude)
    observer.lon = math.radians(longitude)

    sun = ephem.Sun(observer)
    parallactic_angle = sun.parallactic_angle()

    return math.degrees(parallactic_angle)

def solar_coordinates(datetime):
    print("TODO")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", help="Year of observation", type=int, required=True)
    parser.add_argument("-m", "--month", help="Month of observation", type=int, required=True)
    parser.add_argument("-d", "--day", help="Day of observation", type=int, required=True)
    parser.add_argument("-H", "--hour", help="Hour of observation", type=int, required=True)
    parser.add_argument("-M", "--minute", help="Minute of observation", type=int, required=True)
    parser.add_argument("-l", "--latitude", help="Latitude of observation", type=float, required=True)
    parser.add_argument("-L", "--longitude", help="Longitude of observation", type=float, required=True)
    args = parser.parse_args()
    dt = datetime.datetime(args.year, args.month, args.day, args.hour, args.minute)
    print("Parallactic angle : ", parallactic_angle(args.latitude, args.longitude, dt))