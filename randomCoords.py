#! /usr/bin/env python

"""
Program to generate random coordinates in the contiguous UNited States.


This program will generate a user-specified number of random geographic
coordinates in the contiguous United States, reverse geocode them, then
write them to the specified file.

Example:
    $ python randomCoords.py number_of_points output_file

The following conventions were used to ensure the coordinates were in the
contiguous U.S.

US Geographic Information

Northernmost - (49.384472, -95.153389)
Southernmost - (24.433333, -81.918333)
Easternmost - (44.815278. -65.949722)
Westernmost - (48.164167. -124.733056)
Geographic Center - (39.833333. -98.583333)
"""
import argparse
import os
import random

import geocoder


def coordinate_generator(number_of_points):
    """
    Generate and geocode a number of random geographical points.

    :param number_of_points: number of points to generate
    :type number_of_points: int
    :return: list of geographic point tuples

    """
    NORTHERNMOST = 49.
    SOUTHERNMOST = 25.
    EASTERNMOST = -66.
    WESTERNMOST = -124.

    coordinate_list = []
    counter = 0

    while counter < number_of_points:
        latlng = round(random.uniform(SOUTHERNMOST, NORTHERNMOST), 6), round(random.uniform(EASTERNMOST, WESTERNMOST), 6)
        g = geocoder.reverse(latlng)
        if g.country != 'US':
            continue
        else:
            counter += 1
            coordinate_list.append((g.x, g.y, g.address))
            # output_file.write(fullstring.format(g.x, g.y, g.address))
    print 'Finished generating %d coordinate points' % counter
    return coordinate_list



def main(points, fname):
    """
    write list of coordinates to file

    :param points: number of points to generate
    :param fname: name of output file

    """
    fullstring = '{0}, {1}, "{2}", \n'
    coordinates = []
    if os.path.isfile(fname):
        proceed_prompt = raw_input("File exists, proceed(y or n)? ")
        if proceed_prompt.lower() == 'y':
            fout = open(fname, 'a')
            number_of_points = points
            coordinates = coordinate_generator(number_of_points)
            # fout.close()
            for loc in coordinates:
                fout.write(fullstring.format(loc[0], loc[1], loc[2]))
        else:
            print 'Aborting . . .'
            exit()
    else:
        fout = open(fname, 'a')
        number_of_points = points
        coordinates = coordinate_generator(number_of_points)
        for loc in coordinates:
            fout.write(fullstring.format(loc[0], loc[1], loc[2]))
        fout.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("points", type=int, help="number of points to generate")
    parser.add_argument("fname", help="name of output file")
    args = parser.parse_args()
    main(args.points, args.fname)
