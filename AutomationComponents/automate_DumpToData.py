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
all_the_data_files = [f for f in os.listdir() if f.endswith('.dump')]

for data_file in all_the_data_files:
    file_stem = data_file.replace('.dump','')

    ## Create data file
    data_name = f'{file_stem}.dat'
    data_src = f'/home/bcma/AutomationDump/{data_file}'
    data_dst = f'/home/bcma/AutomationDump/{data_name}'

    try:
        shutil.copy(data_src, data_dst)
        print('Dump file successfully copied. Converting to data file.')
    except Exception as e:
        print('Dump file was not copied successfully.')

    ## Parse the diameter into a variable for calculations in order to
    ## modify the x and y size of the box boundary of the CNTs
    # ripup_file_stem = file_stem.split("_")
    # float_diameter = float(ripup_file_stem[3])
    # cnt_boundary = (float_diameter / 2) + 4
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
                print(f'{file_stem}.dump has already been modified.\n')
                mod_flag = True
                break
            if row in [3]:
                rm_newline = line.strip('\n')
                float_value = float(rm_newline)    ## FOR BASH NODES CALCULATIONS
                num_atoms = f'{rm_newline} atoms\n\n'
            if row in [5]:
                rm_newline = line.strip('\n')
                x_box = f'{rm_newline}          xlo xhi\n'
            if row in [6]:
                rm_newline = line.strip('\n')
                y_box = f'{rm_newline}          ylo yhi\n'
            if row in [7]:
                rm_newline = line.strip('\n')
                z_box = f'{rm_newline}          zlo zhi \n\n'

    ## If the file has been flagged, continue to next file if possible and reset flag
    if mod_flag:
        print('Continuing automation.\n')
        mod_flag = False
    else:
        ## The set up the upper most of the data file to be rewritten
        ## Checks certain string in a line. It will be removed/rewritten
        unneeded_lines = range(0,9)
        start_idx, end_idx = 0, len(lines)

        data_header = f'# Data File for {file_stem}\n\n'
        atom_types = '1 atom types\n\n'
        info_type = 'Masses\n\n1 12.01\n\nAtoms\n\n'
        combined_str = f'{data_header}{num_atoms}{atom_types}{x_box}{y_box}{z_box}{info_type}'

        ## Write changes to the file
        with open(data_name, 'w') as fw:
            for row, line in enumerate(lines):
                if row in [0]:
                    fw.write(combined_str)
                elif row not in unneeded_lines:
                    fw.write(line)

        dir_dst = f'/home/bcma/Desktop/{file_stem}'
        os.mkdir(dir_dst)
        print("Directory '%s' created " %file_stem)

        ## If the conditons are met, move data file, bash and input script to their respective CNT folders
        ## Adjust directory path to fit what you have structured
        relocate_bash = f'/home/bcma/AutomationDump/{file_stem}.bash'
        relocate_input = f'/home/bcma/AutomationDump/{file_stem}.in'
        relocate_dat = f'/home/bcma/AutomationDump/{file_stem}.dat'
        relocate_dump = f'/home/bcma/AutomationDump/{file_stem}.dump'
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
        if os.path.exists(relocate_dump):
            shutil.move(relocate_dump, relocate_dst)
