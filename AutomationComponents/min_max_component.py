import os, sys
import shutil
import pandas as pd
import glob

input_src = '/home/bcma/AutomationDump/script_template/CNT_n_m_d.in'
bash_src = '/home/bcma/AutomationDump/script_template/CNT_n_m_d.bash'

## Checks if the data file has already been modified
check_for_mod = '# Data File for '
mod_flag = False

## Only accounts files with file extension .dump
all_the_dump_files = [f for f in os.listdir() if f.endswith('.dump')]

for data_file in all_the_dump_files:
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

    ## Get the text from the data file and modify certain lines/rows
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

    ## Set up array
    all_dfs = []

    ## Glob is for returning all file paths with specific patterns
    glob.glob('CNT_*.csv')

    ## Go through the csv and grab columns xu and yu
    for csv_file in glob.glob('CNT_*.csv'):
        print(f'Loading {csv_file}\n')
        new_df = pd.read_csv(csv_file)

        all_dfs.append(new_df)
        finaldf = pd.concat(all_dfs, axis=0, join='inner', ignore_index=True).sort_index()

        finaldf.head

        ## Parse columns of xu and yu from dump file
        column_xu = finaldf["xu"]
        max_xu = float(column_xu.max())
        min_xu = float(column_xu.min())

        column_yu = finaldf["yu"]
        max_yu = float(column_yu.max())
        min_yu = float(column_yu.min())

        ## Debug print of min and max
        # print(max_xu)
        # print(min_xu)
        # print(max_yu)
        # print(min_yu)
        # print('\n')

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
                x_box = f'{xu_maxbound} {xu_minbound}			xlo xhi\n'
            if row in [6]:
                rm_newline = line.strip('\n')
                y_box = f'{yu_maxbound} {yu_minbound}			ylo yhi\n'
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
        with open(data_name, 'w') as fw:
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
