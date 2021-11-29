#!/usr/bin/env python3
"""
Author : mtoucedasuarez <mtoucedasuarez@email.arizona.edu>
Date   : 2021-11-02
Purpose: Create a new (empty) job script for the Uofa HPC system(s)
"""

import argparse
import os
import sys
import re
from pathlib import Path
from typing import NamedTuple, Optional, TextIO

class Args(NamedTuple):
    """ Command-line arguments """
    job: str
    system: str
    name: str
    group: str
    request_email: str
    email: str
    partition: str
    ntasks: str
    nodes: str
    memory: str
    time: str
    outdir: str
    overwrite: bool


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Create a HPC job template',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    rc_file = os.path.join(str(Path.home()), '.new_job.py')
    defaults = get_defaults(open(rc_file) if os.path.isfile(rc_file) else None)
    username = os.getenv('USER') or 'Anonymous'
    hostname = os.getenv('HOSTNAME') or 'email.arizona.edu'

    parser.add_argument('job', help='Job name', type=str)

    parser.add_argument('-s',
                        '--system',
                        help='The system you would like to create the job for',
                        metavar='str',
                        type=str,
                        default='slurm',
                        choices=['slurm', 'pbs'])

    parser.add_argument('-n',
                        '--name',
                        help='Name you want to give the file and the job',
                        metavar='str',
                        type=str,
                        default='new_job',)

    parser.add_argument('-g',
                        '--group',
                        help='The group to assign the job to',
                        metavar='str',
                        type=str,
                        default='barberan')

    parser.add_argument('-re',
                        '--request_email',
                        help='Mail intensity you want to request',
                        metavar='str',
                        type=str,
                        default='ALL',
                        choices=['BEGIN','END','FAIL','ALL'])

    parser.add_argument('-e',
                        '--email',
                        type=str,
                        default=defaults.get('email',
                                             f'{username}@{hostname}'),
                        help='Email for docstring')

    parser.add_argument('-p',
                        '--partition',
                        help='The system you would like to create the job for',
                        metavar='str',
                        type=str,
                        default='standard',
                        choices=['standard', 'windfall'])

    parser.add_argument('-nt',
                        '--ntasks',
                        help='The number of cores used for this job',
                        metavar='str',
                        type=str,
                        default='1')

    parser.add_argument('-nn',
                        '--nodes',
                        help='Number of nodes used for this job',
                        metavar='str',
                        type=str,
                        default='1')

    parser.add_argument('-m',
                        '--memory',
                        help='Memory required for this job',
                        metavar='str',
                        type=str,
                        default='1gb')

    parser.add_argument('-t',
                        '--time',
                        help='The time required for this job (hhh:mm:ss)',
                        metavar='str',
                        type=str,
                        default="1:00:00")

    parser.add_argument('-d',
                        '--outdir',
                        help='Directory where you would like the job to be created',
                        metavar='str',
                        type=str,
                        default='jobs')

    parser.add_argument('-f',
                        '--force',
                        help='Overwrite existing',
                        action='store_true')

    
    args = parser.parse_args()

    args.job = args.job.strip().replace('-', '_')

    if not args.job:
        parser.error(f'Not a usable filename "{args.job}"')

    return Args(job = args.job, 
                system = args.system, 
                name = args.name,
                group = args.group,
                request_email = args.request_email, 
                email = args.email, 
                partition = args.partition,
                ntasks = args.ntasks,
                nodes = args.nodes,
                memory = args.memory,
                time = args.time,
                outdir=args.outdir, 
                overwrite=args.force)


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    job = args.job

    # create output directory if not provided
    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)
        print(f'Output directory has been created: {args.outdir}')

    # create filename for saving the new file in the directory
    filename = os.path.join(args.outdir, job)

    # overwrite:  ## this doesn't work anymore, something with the directory
    if os.path.isfile(filename) and not args.overwrite:
        answer = input(f'"{filename}" exists.  Overwrite? [yN] ')
        if not answer.lower().startswith('y'):
            sys.exit('Will not overwrite. Bye!')


    # create job calling the function with different arguments depending on system
    # slurm
    if args.system == "slurm":
        print(create_job('SBATCH', args),
              file=open(filename, 'wt'), end='')
        print(f'SLURM job has been created!')
    # pbs
    elif args.system == "pbs":
        print(create_job('PBS', args),
              file=open(filename, 'wt'), end='')
        print(f'PBS job has been created!')


# --------------------------------------------------
def create_job(s, args:Args) -> str:
    """ Create a job file template """

    return f"""#!/usr/bin/bash
# --------------------------------------------------
# Request resources here
# --------------------------------------------------
#{s} --job-name={args.name}
#{s} --output={args.name}.out
#{s} --account={args.group}
#{s} --mail-type={args.request_email}
#{s} --mail-user={args.email}
#{s} --partition={args.partition}
#{s} --ntasks={args.ntasks}
#{s} --nodes={args.nodes}
#{s} --mem={args.memory}
#{s} --time={args.time}

# --------------------------------------------------
# Load modules here
# --------------------------------------------------

# --------------------------------------------------
# Execute commands here
# --------------------------------------------------

"""


# --------------------------------------------------
def get_defaults(file_handle: Optional[TextIO]):
    """ Get defaults from ~/.new_job.py """

    defaults = {}
    if file_handle:
        for line in file_handle:
            match = re.match('([^=]+)=([^=]+)', line)
            if match:
                key, val = map(str.strip, match.groups())
                if key and val:
                    defaults[key] = val

    return defaults


# --------------------------------------------------
if __name__ == '__main__':
    main()
