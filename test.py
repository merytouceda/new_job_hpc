#!/usr/bin/env python3
"""
Test suite for new_job.py
"""

import io
import os
import re
import random
import string
from subprocess import getstatusoutput
from shutil import rmtree
from new import get_defaults

PRG = './new_job.py'
GOOD1 = './expected/inputs1.slurm'
GOOD2 = './expected/inputs1.pbs'
GOOD3 = './expected/inputs2.slurm'
GOOD4 = './expected/inputs2.pbs'

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
        assert re.match("usage", out, re.IGNORECASE)

# --------------------------------------------------
def test_badsystem():
    """usage"""

    for flag in ['-s', '--system']:
        rv, out = getstatusoutput(f'{PRG} {flag} foo')
        assert rv != 0
        assert usage.lower().startswith('usage:')

# --------------------------------------------------
def test_filenotok():
    """ bla """
    pass

# --------------------------------------------------
def test_filenotok():
    pass

# --------------------------------------------------
def test_ok():
    """ Runs ok """

    cwd = os.path.abspath(os.getcwd())
    dirname = os.path.join(cwd, random_string())
    abs_new = os.path.abspath(PRG)

    if os.path.isdir(dirname):
        rmtree(dirname)

    os.makedirs(dirname)
    os.chdir(dirname)

    try:
        basename = random_string()
        name = basename + '.py'
        retval, out = getstatusoutput(f'{abs_new} -t {name}')
        assert retval == 0
        assert os.path.isfile(name)
        assert out == f'Done, see new script "{name}".'

    finally:
        if os.path.isdir(dirname):
            rmtree(dirname)
        os.chdir(cwd)

# --------------------------------------------------
def test_get_defaults():
    """ Test get_defaults() """

    expected = {
        random_string(): random_string()
        for _ in range(random.randint(3, 7))
    }
    text = io.StringIO('\n'.join(f'{k}={v}' for k, v in expected.items()))
    assert get_defaults(text) == expected
    assert get_defaults(None) == {}


# --------------------------------------------------
def random_string():
    """ generate a random string """

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))

# --------------------------------------------------
if __name__ == '__main__':
    main()
