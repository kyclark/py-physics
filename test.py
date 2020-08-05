#!/usr/bin/env python3
"""tests for videocapture.py"""

import os
from subprocess import getstatusoutput

PRG = './videocapture.py'
VIDEO = './can.mp4'


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{PRG} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_ok():
    """ok"""

    rv, out = getstatusoutput(f'{PRG} {VIDEO}')
    assert rv == 0
    assert out == VIDEO
