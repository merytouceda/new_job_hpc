# new_job.py
Python program to create [UofA HPC] (https://public.confluence.arizona.edu/display/UAHPC/HPC+Documentation) jobs. 

## Description
The script "new_job.py" has been created with the goal to automate the creation of HPC job submission files. 

Job submission files for the UofA HPC system can be created for the SLURM or the PBS systems. 
See more in the HPC wiki: https://public.confluence.arizona.edu/display/UAHPC/HPC+Documentation

If run with -h|--help new_job.py produces the following: 


The only required argument is --job. 

If run with default settings new_job.py will produce the following SLURM template: 


#### NOTE: 
This script has been made to make my life easier, some default values (e.g. group = barberan and email) are convenient for me but might not be convenient for other users. You can change the default values of arguments in the get_args() and get_defaults() functions. 

## Author
Mery Touceda-Suárez: maria.touceda.suarez@gmail.com
