# new_job.py
Python program to create [UofA HPC](https://public.confluence.arizona.edu/display/UAHPC/HPC+Documentation) jobs. 

## Description
The script "new_job.py" has been created with the goal to automate the creation of HPC job submission files. 

Job submission files for the UofA HPC system can be created for the SLURM or the PBS systems. 
See more in the [HPC wiki](https://public.confluence.arizona.edu/display/UAHPC/HPC+Documentation)

If run with -h|--help new_job.py produces the following:

```
$ ./new_job.py -h
usage: new_job.py [-h] [-s str] [-n str] [-g str] [-re str] [-e EMAIL] [-p str] [-nt str] [-nn str]
                  [-m str] [-t str] [-d str] [-f]
                  job

Create a HPC job template

positional arguments:
  job                   Job name

optional arguments:
  -h, --help            show this help message and exit
  -s str, --system str  The system you would like to create the job for (default: slurm)
  -n str, --name str    Name you want to give the file and the job (default: new_job)
  -g str, --group str   The group to assign the job to (default: barberan)
  -re str, --request_email str
                        Mail intensity you want to request (default: ALL)
  -e EMAIL, --email EMAIL
                        Email for docstring (default: mtoucedasuarez@email.arizona.edu)
  -p str, --partition str
                        The system you would like to create the job for (default: standard)
  -nt str, --ntasks str
                        The number of cores used for this job (default: 1)
  -nn str, --nodes str  Number of nodes used for this job (default: 1)
  -m str, --memory str  Memory required for this job (default: 1gb)
  -t str, --time str    The time required for this job (hhh:mm:ss) (default: 1:00:00)
  -d str, --outdir str  Directory where you would like the job to be created (default: jobs)
  -f, --force           Overwrite existing (default: False)
```


The only required argument is the positional `job`, which takes the name you want to give the job file. 

If run with default settings new_job.py will produce the following SLURM template: 

```
$ ./new_job.py foo.slurm
SLURM job has been created!
$ less ./jobs/foo.slurm
#!/usr/bin/bash
# --------------------------------------------------
# Request resources here
# --------------------------------------------------
#SBATCH --job-name=new_job
#SBATCH --output=new_job.out
#SBATCH --account=barberan
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mtoucedasuarez@email.arizona.edu
#SBATCH --partition=standard
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --mem=1gb
#SBATCH --time=None

# --------------------------------------------------
# Load modules here
# --------------------------------------------------

# --------------------------------------------------
# Execute commands here
# --------------------------------------------------
```

This template will be created as a file, which can be stored in a personalized directory specified using the `-d` flag (default: jobs).


## Defaults: 
This script has been made to make my life easier, some default values (e.g. group = barberan and email) are convenient for me but might not be convenient for other users. 

**You can change the default values** of arguments in the `get_args()` and `get_defaults()` functions to those that best suit you.  

## Overwrite: 
The script will check if the file name you give it exists. If you don't give it initial instructions on wether it should overwrite a pre-existing file using the flag `-f` `--force`, then the script will ask you if you would like to overwrite: 

```
$ ./new_job.py foo.slurm
"jobs/foo.slurm" exists.  Overwrite? [yN] y
SLURM job has been created!
```

## Author
Mery Touceda-Suárez: maria.touceda.suarez@gmail.com
