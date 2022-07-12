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

    ## Parse the diameter into a variable for calculations in order to
    ## modify the x and y size of the box boundary of the CNTs
    ripup_file_stem = file_stem.split("_")
    float_diameter = float(ripup_file_stem[3])
    cnt_boundary = (float_diameter / 2) + 4
    opp_cnt_boundary = -abs(cnt_boundary)

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
                x_box = f'{cnt_boundary} {opp_cnt_boundary}         xlo xhi\n'
            if row in [6]:
                rm_newline = line.strip('\n')
                y_box = f'{cnt_boundary} {opp_cnt_boundary}         ylo yhi\n'
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
        with open(data_file, 'w') as fw:
            for row, line in enumerate(lines):
                if row in [0]:
                    fw.write(combined_str)
                elif row not in unneeded_lines:
                    fw.write(line)
