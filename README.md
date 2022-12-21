# This repo is a file dump for my Python automation code.

Contains Python scripts that automates the LAMMPS script process and another script for post-process output from LAMMPS after a successful run.

  1. `v4automate_lammps_files.py` - This script will take `.dump` file and create several other files according to it. The script will then create a folder with the CNT's parameters, move all associated files into it, then relocate the entire file to Desktop.
  
  2. `automate_data_analysis.py` - This script will take `.log.lammps` files (TENSILE TESTS ONLY) and generate a `.csv` file and PNG graphs based on the content. After the files have been generated, it will create a folder, move all associated files into it, and relocate it.

