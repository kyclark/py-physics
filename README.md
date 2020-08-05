# Example physics problems in Python

## Starting a new program

I suggest students use a program called "new.py" (included) to start writing a new Python program like so:

```
$ ./new.py videocapture.py
Done, see new script "videocapture.py."
```

The new "videocapture.py" program will include examples of how to accept command-line parameters and will produce help documentation:

```
$ ./videocapture.py --help
usage: videocapture.py [-h] [-a str] [-i int] [-f FILE] [-o] str

Rock the Casbah

positional arguments:
  str                   A positional argument

optional arguments:
  -h, --help            show this help message and exit
  -a str, --arg str     A named string argument (default: )
  -i int, --int int     A named integer argument (default: 0)
  -f FILE, --file FILE  A readable file (default: None)
  -o, --on              A boolean flag (default: False)
```

These are not the correct parameters for our program, so change the "get_args()" function like so:

```
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Recording and Analyzing Moving Objects',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('video',
                        metavar='FILE',
                        help='Input video file')

    args = parser.parse_args()

    if not os.path.isfile(args.video):
        parser.error(f'Invalid file "{args.video}"')

    return args
```

Now the program will produce the following "usage":

```
$ ./videocapture.py -h
usage: videocapture.py [-h] FILE

Recording and Analyzing Moving Objects

positional arguments:
  FILE        Input video file

optional arguments:
  -h, --help  show this help message and exit
```

## Installing requirments

Our program will need these imports:

```
import numpy as np
import cv2
import matplotlib.pyplot as plt
```

In the event you do not have these modules installed, you can use the following command:

```
$ python3 -m pip install numpy opencv-python matplotlib
```

Alternately these have been listed in the file "requirements.txt," so this command would work as well:

```
$ python3 -m pip install -r requirements.txt
```

## Author

Ken Youens-Clark <kyclark@gmail.com>
