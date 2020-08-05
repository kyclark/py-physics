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

    parser.add_argument('-f',
                        '--file',
                        metavar='FILE',
                        help='Input video file',
                        type=str)

    parser.add_argument('-t',
                        '--thresh1',
                        metavar='threshold1',
                        help='Threshold 1 value',
                        type=int,
                        default=0)

    parser.add_argument('-T',
                        '--thresh2',
                        metavar='threshold2',
                        help='Threshold 2 value',
                        type=int,
                        default=10)

    parser.add_argument('-d',
                        '--dist',
                        metavar='distance',
                        help='Distance',
                        type=int,
                        default=5)

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f'Invalid file "{args.file}"')

    return args


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    x_cm, y_cm, time = track_motion(args.file, args.thresh1, args.thresh2,
                                    args.dist)

    print(f'X = "{x_cm}", Y = "{y_cm}", time = "{time}"')


# --------------------------------------------------
def read_frame(video, frame_num):
    """Read a frame from the video"""

    video.set(1, frame_num)
    _, frame = video.read()
    return frame


# --------------------------------------------------
def track_motion(filename, thresh, thresh2, dist):
    """Track the motion"""

    vid = cv2.VideoCapture(filename)

    # determine the size of the video images and the number of frames
    # width = vid.get(3)
    # height = vid.get(4)
    fps = vid.get(5)

    # determines number of frames in video
    num_frames = int(vid.get(7))

    # setup arrays to store the coordinates
    # of the center of mass at each time point
    x_cm = np.zeros((num_frames, 1))
    y_cm = np.zeros((num_frames, 1))

    time = np.array([i for i in range(num_frames)], dtype='float') / fps

    # read in first frame and convert to float
    frame = read_frame(vid, 0)
    frame = frame.astype('float')

    # compute the grayscale and red images
    gray = np.mean(frame, axis=2, dtype=float)
    red = frame[:, :, 2]

    # find values of the image created by subtracting gray from red
    # that are less than Thresh or greater than Thresh2
    mask = (red - gray < thresh)
    mask2 = (red - gray > thresh2)

    # have user measure the distance between lines in image
    # fig = plt.figure()
    plt.spy(mask2)

    print('Click on two marker points in the image that are Dist apart')

    points = np.array(plt.ginput(2))

    # define the pixel to cm conversion scale
    pix2cm = dist / (points[1, 0] - points[0, 0])

    # find the connected regions in the Mask
    regions = cv2.connectedComponentsWithStats(mask.astype('uint8'))

    # determine which region has the largest area
    stats = regions[2]
    stats[0, 4] = 0
    can_label = np.argmax(stats[:, 4])

    # remove unwanted regions from the mask
    can_mask = mask
    can_mask[regions[1] != can_label] = 0

    # find the center of mass of the object
    x_cm[0] = regions[3][can_label, 0]
    y_cm[0] = regions[3][can_label, 1]

    # plot the mask and its center of mass
    plt.clf()
    plt.spy(can_mask)
    plt.plot(x_cm[0], y_cm[0], 'or')
    plt.pause(0.1)

    # loop through the remaining frames of the video
    for i in range(1, num_frames):
        # read in first frame and convert to float
        frame = read_frame(vid, i)
        frame = frame.astype('float')

        # compute the grayscale image
        gray = np.mean(frame, axis=2, dtype=float)
        red = frame[:, :, 2]

        # find values of the grayscale image greater than Thresh
        mask = (red - gray > thresh)

        # find the connected regions in the Mask
        regions = cv2.connectedComponentsWithStats(mask.astype('uint8'))

        # determine which region has the largest area
        stats = regions[2]
        stats[0, 4] = 0
        can_label = np.argmax(stats[:, 4])

        # remove unwanted regions from the Mask
        can_mask = mask
        can_mask[regions[1] != can_label] = 0

        # find the Center of Mass of the object
        x_cm[i] = regions[3][can_label, 0]
        y_cm[i] = regions[3][can_label, 1]

        # plot the mask and its center of mass
        plt.clf()
        plt.spy(can_mask)
        plt.plot(x_cm[i], y_cm[i], 'or')
        plt.pause(0.1)

        # convert Xcm and Ycm to centimeters
        x_cm = pix2cm * x_cm
        y_cm = pix2cm * y_cm

        # plot Xcm as a function of time
        plt.figure()
        plt.plot(time, x_cm)
        plt.xlabel('Time (s)', fontname='Arial', fontsize=16)
        plt.ylabel('Distance (cm)', fontname='Arial', fontsize=16)
        vid.release()

    return x_cm, y_cm, time


# --------------------------------------------------
if __name__ == '__main__':
    main()
