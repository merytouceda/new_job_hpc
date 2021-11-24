#!/usr/bin/env python3
"""
Test suite for new_job.py
"""

import argparse
import os
from subprocess import getstatusoutput, getoutput

prg = './new_job.py'

# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{prg} {flag}')
        assert rv == 0
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_empty():
    ''' template with no command line arguments'''
    pass


# --------------------------------------------------
def test_commandargs():
    ''' template with command line arguments'''
    pass

# --------------------------------------------------
if __name__ == '__main__':
    main()
