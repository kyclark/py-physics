#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-08-05
Purpose: Recording and Analyzing Moving Objects
"""

import argparse
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Recording and Analyzing Moving Objects',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('video', metavar='FILE', help='Input video file')

    args = parser.parse_args()

    if not os.path.isfile(args.video):
        parser.error(f'Invalid file "{args.video}"')

    return args


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    print(args.video)
    # vid = cv2.VideoCapture(args.video)


# --------------------------------------------------
if __name__ == '__main__':
    main()
