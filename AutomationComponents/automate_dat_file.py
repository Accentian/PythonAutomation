### Brandon Ma
### Credit: Megan McCarthy, os & sys methods used as templates
## This code modifies ONLY the raw .dat files from VMD to a format that's acceptable to LAMMPS
## This code is fragile. Any changes to the raw .dat file can result in incorrect modifications
## The fragiliy is from LINE 15 where we get the text from the data file

import os, sys

all_the_data_files = [f for f in os.listdir() if f.endswith('.dat')]

for data_file in all_the_data_files:
    file_stem = data_file.replace('.dat','')

    ## get the text from the data file
    with open(data_file, 'r') as f:
        lines = f.readlines()
        for row, line in enumerate(lines):
            if row in [3]:
                rm_newline = line.strip('\n')
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

    with open(data_file, 'w') as fw:
        for row, line in enumerate(lines):
            if row in [0]:
                fw.write(combined_str)
            elif row not in unneeded_lines:
                fw.write(line)

    ## DEBUG PRINT: KEEP IT IN THIS ORDER
    # print(data_header)
    # print(num_atoms)
    # print(atom_types)
    # print(x_box)
    # print(y_box)
    # print(z_box)
    # print(info_type)
    # print(combined_str)
