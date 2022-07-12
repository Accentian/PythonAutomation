"""
Brandon Ma
Credit: Megan McCarthy, Ember Sikorski, Naasir Smalls, & GeeksforGeeks website
Created using Jupyter Notebook & Atom Editor

This program goes through the directory that it is listed on and selects files with with .dump extensions, then create a copy of .dump files and modifies it to .dat files while creating bash and input script for those respective .dat files.

In between the process, a csv file of the dump will be generated to caclulate the max and min of the x & y coordinates of the atoms where the script will record those min max values and use it to create the box boundaries in the input script.

Once the csv has been read. The script will remove the csv.

Note that this code is fragile as any changes to any of the LAMMPS files can
cause incorrect modifications.The origin of this fragility can be found in the likes of the for loops.

Please be careful when modifying or inputting the file for this code.

NOTE:

Please ensure that the proper packages and imports are in the Python environment such as pandas and glob. Failure to do so will result in several errors.
"""

import os, sys
import shutil
import pandas as pd
import glob

## Location of script templates.
## Change the directories to where you have your templates/scripts located
input_src = '/home/bcma/AutomationDump/script_template/CNT_n_m_d.in'
bash_src = '/home/bcma/AutomationDump/script_template/CNT_n_m_d.bash'

## Checks if the data file has already been modified
check_for_mod = '# Data File for '
mod_flag = False

## Only accounts files with file extension .dat
all_the_dump_files = [f for f in os.listdir() if f.endswith('.dat')]

for data_file in all_the_dump_files:
    file_stem = data_file.replace('.dat','')

    try:
        shutil.copy(data_src, data_dst)
        print('Dump file successfully copied. Converting to data file.')
    except Exception as e:
        print('Dump file was not copied successfully.')

    ## Open and read the data file
    with open(data_file, 'r') as f:
            lines = f.readlines()

    ## Check for a particular row of string
    col_check_str = 'id type xu yu zu'
    columns = None
    start_idx, end_idx = 0, len(lines)

    for row, line in enumerate(lines):
        ## If the file has already been altered, flag and break from FOR loop
        if check_for_mod in line:
            print(f'{file_stem}.dat has already been modified.\n')
            mod_flag = True
            break
        if col_check_str in line:
            columns = line.strip().split()[2:]
            start_idx = row + 1

    data0 = lines[start_idx:end_idx]
    data = [row for row in data0]
    columns_entry = None

    ## write the CSV file
    csv_name = f'{file_stem}.csv'
    with open(csv_name, 'w') as f:
        f.write(",".join(columns) + "\n")
        for start_idx in data:
            columns_entry = start_idx.strip().split()
            f.write(",".join(columns_entry) + "\n")

    f.close()

    ## Glob is for returning all file paths with specific patterns
    glob.glob('CNT_*.csv')

    ## Go through the csv and grab columns xu and yu
    for csv_file in glob.glob('CNT_*.csv'):
        print(f'Loading {csv_file}')
        new_df = pd.read_csv(csv_file)

        ## Parse columns of xu and yu from data file
        column_xu = new_df["xu"]
        max_xu = float(column_xu.max())
        min_xu = float(column_xu.min())

        column_yu = new_df["yu"]
        max_yu = float(column_yu.max())
        min_yu = float(column_yu.min())

        column_zu = new_df["zu"]
        max_zu = column_zu.max()
        min_zu = column_zu.min()

        distance_xu = math.sqrt((max_xu - min_xu) ** 2)     ## Diameter x direction
        distance_yu = math.sqrt((max_yu - min_yu) ** 2)     ## Diameter y direction
        distance_zu = math.sqrt((max_zu - min_zu) ** 2)     ## Length
        str_distance_xu = str(distance_xu)
        str_distance_yu = str(distance_yu)
        str_distance_zu = str(distance_zu)
        str_nm_distance_xu = str(distance_xu / 10)
        str_nm_distance_yu = str(distance_yu / 10)
        str_nm_distance_zu = str(distance_zu / 10)


        # ##DEBUG PRINT
        # print('Max/Min of x:')
        # print(max_xu)
        # print(min_xu)
        # print('\n')
        #
        # print('Max/Min of y:')
        # print(max_yu)
        # print(min_yu)
        # print('\n')
        #
        # print('Max/Min of z:')
        # print(max_zu)
        # print(min_zu)
        # print('\n')

        print('CNT Diameter in x direction:')
        print(str_distance_xu)
        print('To nanometers:')
        print(str_nm_distance_xu)
        print('\n')

        print('CNT Diameter in y direction:')
        print(str_distance_yu)
        print('To nanometers:')
        print(str_nm_distance_yu)
        print('\n')

        print('CNT Length:')
        print(str_distance_zu)
        print('To nanometers:')
        print(str_nm_distance_zu)
        print('---------------------')

        ## Write direct measurements to a text file
        with open(measure_name, 'w') as f:
            f.write(f'{file_stem} Measurements')
            f.write('\n \n')

            f.write('CNT Diameter in x direction: \n\n')
            f.write('%s nm \n' %str_nm_distance_xu)
            f.write('%s angstrom' %str_distance_xu)
            f.write('\n \n')

            f.write('CNT Diameter in y direction: \n\n')
            f.write('%s nm \n' %str_nm_distance_yu)
            f.write('%s angstrom' %str_distance_yu)
            f.write('\n \n')

            f.write('CNT Length: \n\n')
            f.write('%s nm \n' %str_nm_distance_zu)
            f.write('%s angstrom' %str_distance_zu)

        ## Removes dump csv after obtaining min/max of xu and yu
        if os.path.exists(f'{csv_file}'):
          os.remove(f'{csv_file}')
        else:
          print(f'{csv_file} does not exist\n')

    ## Find min and max of xu and yu, then add 2 Angstroms to get box boundary
    xu_maxbound = max_xu + 2
    xu_minbound = min_xu - 2
    yu_maxbound = max_yu + 2
    yu_minbound = min_yu - 2

    ## Get the text from the data file and modify certain lines/rows
    with open(data_file, 'r') as f:
        lines = f.readlines()
        for row, line in enumerate(lines):
            if row in [3]:
                rm_newline = line.strip('\n')
                float_value = float(rm_newline)    ## FOR BASH NODES CALCULATIONS
                num_atoms = f'{rm_newline} atoms\n\n'
            if row in [5]:
                rm_newline = line.strip('\n')
                x_box = f'{xu_minbound} {xu_maxbound} 			xlo xhi\n'
            if row in [6]:
                rm_newline = line.strip('\n')
                y_box = f'{yu_minbound} {yu_maxbound}			ylo yhi\n'
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
            print('---------------------')
        except Exception as e:
            print('Bash script was not copied successfully.')
            print('---------------------')

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
        relocate_text = f'/home/bcma/AutomationDump/{file_stem}_measurements.txt'
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
        if os.path.exists(relocate_text):
            shutil.move(relocate_text, relocate_dst)
