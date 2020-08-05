#!/usr/bin/env python3
"""
Authors: Charles Wolgemuth <wolg@arizona.edu>,
         Ken Youens-Clark <kyclark@gmail.com>
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
                        '--threshold1',
                        metavar='threshold1',
                        help='Threshold 1 value',
                        type=int,
                        default=0)

    parser.add_argument('-T',
                        '--threshold2',
                        metavar='threshold2',
                        help='Threshold 2 value',
                        type=int,
                        default=10)

    parser.add_argument('-d',
                        '--dist',
                        metavar='distance',
                        help='Distance in centimeters',
                        type=float,
                        default=5.)

    parser.add_argument('-s',
                        '--speed',
                        metavar='speed',
                        help='Speed of animation',
                        type=float,
                        default=.1)

    parser.add_argument('-o',
                        '--outfile',
                        metavar='FILE',
                        help='Name of output file',
                        type=str,
                        default='out.png')

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        parser.error(f'Invalid file "{args.file}"')

    return args


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    thresh1 = args.threshold1
    thresh2 = args.threshold2
    dist = args.dist
    speed = args.speed

    # determine the size of the video images and the number of frames
    vid = cv2.VideoCapture(args.file)
    fps = vid.get(5)

    # determines number of frames in video
    num_frames = int(vid.get(7))

    # setup arrays to store the coordinates
    # of the center of mass at each time point
    x_cm = np.zeros((num_frames, 1))
    y_cm = np.zeros((num_frames, 1))
    time = np.array(list(range(num_frames)), dtype='float') / fps
    mask1, mask2 = frame_masks(vid, 0, thresh1, thresh2)

    plt.spy(mask2)

    # have user measure the distance between lines in image
    print(f'Click on two marker points in the image that are {dist} cm apart')

    points = np.array(plt.ginput(2))

    # define the pixel to cm conversion scale
    pix2cm = dist / (points[1, 0] - points[0, 0])
    can_mask, x_cm[0], y_cm[0] = get_stats(mask1)

    # plot the mask and its center of mass
    plt.clf()
    plt.spy(can_mask)
    plt.plot(x_cm[0], y_cm[0], 'or')
    plt.pause(speed)

    # loop through the remaining frames of the video
    for i in range(1, num_frames):
        # read in first frame and convert to float
        mask1, mask2 = frame_masks(vid, i, thresh1, thresh2)
        can_mask, x_cm[i], y_cm[i] = get_stats(mask1)

        # plot the mask and its center of mass
        plt.clf()
        plt.spy(can_mask)
        plt.plot(x_cm[i], y_cm[i], 'or')
        plt.pause(speed)

    # convert Xcm and Ycm to centimeters
    x_cm, y_cm = pix2cm * x_cm, pix2cm * y_cm

    # plot Xcm as a function of time
    plt.figure()
    plt.plot(time, x_cm)
    plt.xlabel('Time (s)', fontname='Arial', fontsize=16)
    plt.ylabel('Distance (cm)', fontname='Arial', fontsize=16)
    plt.savefig(args.outfile, fmt='png')
    plt.show()
    vid.release()

    print(f'Done, see "{args.outfile}".')


# --------------------------------------------------
def frame_masks(video, frame_num, thresh1, thresh2):
    """Show a frame"""

    video.set(1, frame_num)
    _, frame_raw = video.read()
    frame = frame_raw.astype('float')

    # compute the grayscale and red images
    gray = np.mean(frame, axis=2, dtype=float)
    red = frame[:, :, 2]

    # find values of the image created by subtracting gray from red
    # that are less than Thresh1 or greater than Thresh2
    return (red - gray < thresh1), (red - gray > thresh2)


# --------------------------------------------------
def test_frame_masks():
    """Test frame_masks"""

    # assert frame_masks(???) == ???

    # placeholder until real test
    assert True


# --------------------------------------------------
def get_stats(mask):
    """Determine which region has the largest area"""

    # find the connected regions in the Mask
    regions = cv2.connectedComponentsWithStats(mask.astype('uint8'))
    stats = regions[2]
    stats[0, 4] = 0
    can_label = np.argmax(stats[:, 4])

    # remove unwanted regions from the mask
    can_mask = mask
    can_mask[regions[1] != can_label] = 0

    # find the center of mass of the object
    return can_mask, regions[3][can_label, 0], regions[3][can_label, 1]


# --------------------------------------------------
def test_get_stats():
    """Test get_stats"""

    # assert get_stats(???) == ???

    # placeholder until real test
    assert True


# --------------------------------------------------
if __name__ == '__main__':
    main()
