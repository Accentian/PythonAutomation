import os, sys
import shutil
from os.path import exists

all_the_data_files = [f for f in os.listdir() if f.endswith('.dat')]

for data_file in all_the_data_files:
    file_stem = data_file.replace('.dat','')

    ## Get the text from the data file
    with open(data_file, 'r') as f:
        lines = f.readlines()
        for row, line in enumerate(lines):
            if row in [3]:
                rm_newline = line.strip('\n')
                float_value = float(rm_newline)    # FOR BASH NODES
                num_atoms = f'{rm_newline} atoms\n\n'
            if row in [5]:
                rm_newline = line.strip('\n')
                x_box = f'{rm_newline}			xlo xhi\n'
            if row in [6]:
                rm_newline = line.strip('\n')
                y_box = f'{rm_newline}			ylo yhi\n'
            if row in [7]:
                rm_newline = line.strip('\n')
                z_box = f'{rm_newline}	zlo zhi \n\n'

    unneeded_lines = range(0,9)
    start_idx, end_idx = 0, len(lines)
    str_check = 'ITEM:'

    data_header = f'# Data File for {file_stem}\n\n'
    atom_types = '1 atom types\n\n'
    info_type = 'Masses\n\n1 12.01\n\nAtoms\n\n'
    combined_str = f'{data_header}{num_atoms}{atom_types}{x_box}{y_box}{z_box}{info_type}'

    # Write changes to the file
    with open(data_file, 'w') as fw:
        for row, line in enumerate(lines):
            if row in [0]:
                fw.write(combined_str)
            elif row not in unneeded_lines:
                fw.write(line)

    # # Initalize CNT directory name
    # # Credit to GeeksforGeeks
    # cnt_dir = file_stem
    # parent_dir = '/home/bcma/Desktop/'
    # dir_path = os.path.join(parent_dir, cnt_dir)
    #
    # # Create directory for the CNT
    # os.mkdir(dir_path)
    # print("Directory '%s' created " %cnt_dir)

    ## Initalize CNT directory name
    ## Credit to GeeksforGeeks: https://www.geeksforgeeks.org/create-a-directory-in-python/

    #cnt_dir = file_stem
    dir_dst = f'/home/bcma/Desktop/{file_stem}'
    os.mkdir(dir_dst)
    print("Directory '%s' created " %file_stem)

    ## Move data file, bash and input script to their respective CNT folders
    relocate_bash = f'/home/bcma/AutomationDump/{file_stem}.bash'
    relocate_input = f'/home/bcma/AutomationDump/{file_stem}.in'
    relocate_dat = f'/home/bcma/AutomationDump/{file_stem}.dat'
    relocate_pdb = f'/home/bcma/AutomationDump/{file_stem}.pdb'
    relocate_xyz = f'/home/bcma/AutomationDump/{file_stem}.xyz'
    relocate_dst = f'/home/bcma/Desktop/{file_stem}'

    if os.path.exists(relocate_pdb):
        shutil.move(relocate_pdb, relocate_dst)
    if os.path.exists(relocate_xyz):
        shutil.move(relocate_xyz, relocate_dst)

    shutil.move(relocate_bash, relocate_dst)
    shutil.move(relocate_input, relocate_dst)
    shutil.move(relocate_dat, relocate_dst)
