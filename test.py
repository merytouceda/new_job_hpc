
""" Test suite for new_job.py"""


import os
import re
import random
import string
from subprocess import getstatusoutput
from shutil import rmtree
# from new import get_defaults  # what is happening here?

PRG = './new_job.py'

# GOOD1 = './expected/inputs1.slurm'  # only need it if I use other types of tests
# GOOD2 = './expected/inputs1.pbs'
# GOOD3 = './expected/inputs2.slurm'
# GOOD4 = './expected/inputs2.pbs'


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
    """test if code crashes weh bad system"""

    for flag in ['-s', '--system']:
        rv, out = getstatusoutput(f'{PRG} {flag} foo')
        assert rv != 0  # test that code breaks
        assert out.lower().startswith(
            'usage:')  # test that error message is correct


# --------------------------------------------------


def test_filenotok():
    """ test that code breaks when file is not given """

    # given only the program with no positional job name argument
    rv, out = getstatusoutput(f'{PRG}')
    assert rv != 0  # test that code breaks
    assert out.lower().startswith(
        'usage:')  # test that error message is correct


# --------------------------------------------------
def run(system: str) -> None:
    """ Runs ok
    This test will run things and tidy up after """

    cwd = os.path.abspath(os.getcwd())  # get current wd absolute path
    dirname = os.path.join(cwd, random_string())  # create a random dirname
    abs_new = os.path.abspath(PRG)  # get absolute path of program

    if os.path.isdir(dirname):  # if dir exists remove -r
        rmtree(dirname)

    os.makedirs(dirname)  # create the dir and cd
    os.chdir(dirname)

    try:
        # create random py script
        ext = '.pbs' if system == 'pbs' else '.slurm'
        filename = random_string() + ext
        system_opt = f'-s {system}' if system else ''
        cmd = f'{abs_new} {system_opt} -d {dirname} {filename}'
        retval, out = getstatusoutput(cmd)

        # check that file is created ok
        assert retval == 0
        system_name = system.upper() if system else 'SLURM'
        assert out == f'{system_name} job has been created!'

        assert os.path.isdir(dirname)
        outfile = os.path.join(dirname, filename)
        assert os.path.isfile(outfile)

        with open(outfile) as fh:
            pragma_name = 'PBS' if system == 'pbs' else 'SBATCH'
            lines = list(filter(lambda s: s.startswith(f'#{pragma_name}'), fh))
            assert len(lines) > 1

    finally:  # clean up
        if os.path.isdir(dirname):
            rmtree(dirname)
        os.chdir(cwd)


# --------------------------------------------------
def test_system_default() -> None:
    """ Runs with default (SLURM) """

    run('')


# --------------------------------------------------
def test_system_slurm() -> None:
    """ Runs with SLURM """

    run('slurm')


# --------------------------------------------------
def test_system_pbs() -> None:
    """ Runs with SLURM """

    run('pbs')


# --------------------------------------------------

# def test_get_defaults():
#     """ Test get_defaults() """

#     expected = {
#         random_string(): random_string()
#         for _ in range(random.randint(3, 7))
#     }
#     text = io.StringIO('\n'.join(f'{k}={v}' for k, v in expected.items()))
#     assert get_defaults(text) == expected
#     assert get_defaults(None) == {}


# --------------------------------------------------
def random_string():
    """ generate a random string """

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))

