#!/usr/bin/env python3
"""
Author : mtoucedasuarez <mtoucedasuarez@localhost>
Date   : 2021-11-02
Purpose: Create a new (empty) job script for the Uofa HPC system(s)
"""

import argparse
import os
import sys
import re
from pathlib import Path
from typing import NamedTuple, Optional, TextIO


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Create a HPC job template',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    rc_file = os.path.join(str(Path.home()), '.new_job.py')
    defaults = get_defaults(open(rc_file) if os.path.isfile(rc_file) else None)
    username = os.getenv('USER') or 'Anonymous'
    hostname = os.getenv('HOSTNAME') or 'localhost'

    parser.add_argument('job', help='Job name', type=str)

    parser.add_argument('-s',
                        '--system',
                        help='The system you would like to create the job for',
                        metavar='str',
                        type=str,
                        default='slurm',
                        choices = ['slurm', 'pbs'])

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
                        choices=['ALL'])

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

    parser.add_argument('-t', #not sure how to add this!! # NOTE: this is not the final code!!!
                        '--time',
                        help='The time required for this job (hhh:mm:ss)',
                        metavar='str',
                        type=str,)

    parser.add_argument('-d',
                        '--outdir',
                        help='Directory where you would like the job to be created',
                        metavar='str',
                        type=str,
                        default = 'jobs') #maybe if a new directory is created i should print where!


    return parser.parse_args()


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()
    job = args.job


    # create output directory if not provided
    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)
        print(f'Output directory has been created: {args.outdir}')

    # create job calling the function with different arguments depending on system
    if args.system == "slurm": 
        print(create_job('SBATCH', args.name, args.group, args.request_email,
        args.email, args.partition, args.ntasks, args.nodes, args.memory, args.time), 
        file=open(job, 'wt'), end='')
        print(f'Slurm job has been created!')
    elif args.system == "pbs":
        print(create_job('PBS', args.name, args.group, args.request_email,
        args.email, args.partition, args.ntasks, args.nodes, args.memory, args.time),
        file=open(job, 'wt'), end='')
        print(f'Pbs job has been created!')


# --------------------------------------------------
def create_job(s, n, g, re, e, p, nt, nn, m, t):
    """ Create a slurm file
    takes: 
    n (name of job)
    g (group for allocation)
    re (request email?)
    e (email address)
    p (partition)
    nt (number of tasks)
    nn (number of nodes)
    m (memory)
    t (time)
    returns: a job template text"""

    return f"""#!/usr/bin/bash
# --------------------------------------------------
# Request resources here
# --------------------------------------------------
#{s} --job-name={n}
#{s} --output={n}.out
#{s} --account={g}
#{s} --mail-type={re}
#{s} --mail-user={e}
#{s} --partition={p}
#{s} --ntasks={nt}
#{s} --nodes={nn}
#{s} --mem={m}
#{s} --time={t}

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
