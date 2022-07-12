"""
Brandon Ma
Credit: Megan McCarthy, Ember Sikorski, & GeeksforGeeks website

This program goes through the directory that it is listed on and selects files with with .dat extensions,
then modifies the .dat files while creating bash and input script for those respective .dat files.
Note that this code is fragile as any changes to the .dat files can cause incorrect modifications.
The origin of this fragility can be found in the likes of for loops through certain lines as seen
in LINE 26.

Please be careful when modifying or inputting the file for this code.
"""

import os, sys
import shutil

## Location of script templates.
## Change the directories to where you have your templates/scripts located
input_src = '/home/bcma/AutomationDump/script_template/CNT_n_m_d.in'
bash_src = '/home/bcma/AutomationDump/script_template/CNT_n_m_d.bash'

## Checks if the data file has already been modified
check_for_mod = '# Data File for '
mod_flag = False

## Only accounts files with file extension .dat
all_the_data_files = [f for f in os.listdir() if f.endswith('.dat')]

for data_file in all_the_data_files:
    file_stem = data_file.replace('.dat','')

    ## Find Min and Max of xu and yu and add/subtract two for box boundaries
    # ripup_file_stem = file_stem.split("_")
    # float_diameter = float(ripup_file_stem[3])
    # cnt_boundary = (float_diameter / 2) + 3
    # opp_cnt_boundary = -abs(cnt_boundary)

    ## PRINT DEBUG
    # print(f'Loading {file_stem}')
    # print(cnt_boundary)
    # print(opp_cnt_boundary)

    ## Get the text from the data file and modify certain lines/rows
    with open(data_file, 'r') as f:
        lines = f.readlines()
        for row, line in enumerate(lines):
            ## If the file has already been altered, flag and break from FOR loop
            if check_for_mod in line:
                print(f'{file_stem}.dat has already been modified.\n')
                mod_flag = True
                break
            if row in [3]:
                rm_newline = line.strip('\n')
                float_value = float(rm_newline)    ## FOR BASH NODES CALCULATIONS
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

    if mod_flag:
        print('Continuing automation.\n')
        mod_flag = False
    else:
        ## This set up the upper most of the data file to be rewritten
        ## Checks certain string in a line. It will be removed/rewritten
        unneeded_lines = range(0,9)
        start_idx, end_idx = 0, len(lines)
        # str_check = 'ITEM:'

        data_header = f'# Data File for {file_stem}\n\n'
        atom_types = '1 atom types\n\n'
        info_type = 'Masses\n\n1 12.01\n\nAtoms\n\n'
        combined_str = f'{data_header}{num_atoms}{atom_types}{x_box}{y_box}{z_box}{info_type}'

        ## Write changes to the file
        with open(data_file, 'w') as fw:
            for row, line in enumerate(lines):
                if row in [0]:
                    fw.write(combined_str)
                elif row not in unneeded_lines:
                    fw.write(line)

        ## Initalize CNT directory name, will give a FileExistsError if directory
        ## already exists at the destination
        dir_dst = f'/home/bcma/Desktop/{file_stem}'
        os.mkdir(dir_dst)
        print("Directory '%s' created " %file_stem)

        ## Create Input script (Tensile test)
        ## Input script can vary, review what sort of Input script you have
        input_name = f'{file_stem}.in'
        input_dst = f'/home/bcma/AutomationDump/{input_name}'

        ## Copy input script from source to destination
        try:
            shutil.copy(input_src, input_dst)
            print('Input script successfully copied.')
        except Exception as e:
            print('Input script was not copied successfully.')

        with open(input_name, 'r') as f:
            lines2 = f.readlines()

        ## IMPORTANT:
        ## Modify directories
        ## Modify log_command
        ## Modify dump_command
        comment_header = f'#uniaxial tensile test of {file_stem}\n'
        log_command = f'log /ascldap/users/bcma/5thCNTRun/{file_stem}/{file_stem}.log.lammps\n'     ## Modify
        read_command = f'read_data 	{file_stem}.dat\n'
        dump_command = f'dump           1 all atom 5000 /ascldap/users/bcma/5thCNTRun/{file_stem}/{file_stem}.lammpstrj\n'      ## Modify

        ## Write changes to the script
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


        ## Create bash script
        ## Bash script can vary, so review what sort of Bash script you have
        bash_name = f'{file_stem}.bash'
        bash_dst = f'/home/bcma/AutomationDump/{bash_name}'

        ## Fit number of atoms to number of nodes
        ## Set conditions to limit the amount of nodes we can use
        float_value = round((float_value / 45) / 16)

        if float_value >= 256:
            float_value = 256
        elif float_value <= 1:
            float_value = 1

        str_value = str(float_value)

        ## Copy bash script from source to destination
        try:
            shutil.copy(bash_src, bash_dst)
            print('Bash script successfully copied.')
        except Exception as e:
            print('Bash script was not copied successfully.')

        with open(bash_name, 'r') as f:
            lines3 = f.readlines()

        ## Set changes to the bash script
        ## Modify directories if needed
        bash_job_name = f'#SBATCH --job-name {file_stem}\n'
        bash_num_nodes = f'#SBATCH --nodes={str_value}\n'
        bash_input = f'mpiexec --n $(($cores*$nodes)) /ascldap/users/bcma/lammps-develop/build/lmp -in {file_stem}.in'

        ## Write changes to the script
        with open(bash_name, 'w') as fw:
            for row3, line3 in enumerate(lines3):
                if row3 in [2]:
                    fw.write(bash_job_name)
                if row3 in [5]:
                    fw.write(bash_num_nodes)
                if row3 in [18]:
                    fw.write(bash_input)
                elif row3 not in [2, 5, 18]:
                    fw.write(line3)


        ## If the conditons are met, move data file, bash and input script to their respective CNT folders
        ## Adjust directory path to fit what you have structured
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
        if os.path.exists(relocate_bash):
            shutil.move(relocate_bash, relocate_dst)
        if os.path.exists(relocate_input):
            shutil.move(relocate_input, relocate_dst)
        if os.path.exists(relocate_dat):
            shutil.move(relocate_dat, relocate_dst)
