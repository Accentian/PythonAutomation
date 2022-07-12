import os, sys
import shutil

src = '/home/bcma/AutomationDump/script_template/CNT_n_m_d.in'

## Testing components that parse the file names
all_the_data_files = [f for f in os.listdir() if f.endswith('.dat')]

for data_file in all_the_data_files:
    file_stem = data_file.replace('.dat','')

    ## Test Component for .dat files
    # with open(data_file, 'r') as f:
    #     lines = f.readlines()
    #     for row, line in enumerate(lines):
    #         if row in [3]:
    #             rm_newline = line.strip('\n')
    #             num_atoms = f'{rm_newline} atoms\n\n'
    #         if row in [5]:
    #             rm_newline = line.strip('\n')
    #             x_box = f'{rm_newline}			xlo xhi\n'
    #         if row in [6]:
    #             rm_newline = line.strip('\n')
    #             y_box = f'{rm_newline}			ylo yhi\n'
    #         if row in [7]:
    #             rm_newline = line.strip('\n')
    #             z_box = f'{rm_newline}	zlo zhi \n\n'
    #
    # unneeded_lines = range(0,9)
    # start_idx, end_idx = 0, len(lines)
    # str_check = 'ITEM:'
    #
    # data_header = f'# Data File for {file_stem}\n\n'
    # atom_types = '1 atom types\n\n'
    # info_type = 'Masses\n\n1 12.01\n\nAtoms\n\n'
    # combined_str = f'{data_header}{num_atoms}{atom_types}{x_box}{y_box}{z_box}{info_type}'
    #
    # with open(data_file, 'w') as fw:
    #     for row, line in enumerate(lines):
    #         if row in [0]:
    #             fw.write(combined_str)
    #         elif row not in unneeded_lines:
    #             fw.write(line)

    ## Create Input script
    input_name = f'{file_stem}.in'
    dst = f'/home/bcma/AutomationDump/{input_name}'

    try:
        shutil.copy(src, dst)
        print('Input script successfully copied.')
    except Exception as e:
        print('Input script was not copied successfully.')

    with open(input_name, 'r') as f:
        lines2 = f.readlines()

    comment_header = f'#uniaxial tensile test of {file_stem}\n'
    log_command = f'log /ascldap/users/bcma/{file_stem}/{file_stem}.log.lammps\n'
    read_command = f'read_data 	{file_stem}.dat\n'
    dump_command = f'dump           1 all atom 5000 /ascldap/users/bcma/{file_stem}/{file_stem}.lammpstrj\n'

    with open(input_name, 'w') as fw:
        for row2, line2 in enumerate(lines2):
            if row2 in [0]:
                fw.write(comment_header)
            if row2 in [2]:
                fw.write(log_command)
            if row2 in [16]:
                fw.write(read_command)
            if row2 in [86]:
                fw.write(dump_command)
            elif row2 not in [0,2,16,86]:
                fw.write(line2)
