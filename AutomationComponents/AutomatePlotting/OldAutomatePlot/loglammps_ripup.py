# CREDIT: Megan McCarthy
# COMPILED: Brandon Ma

## This program reads from a local directory and selects files that has log.lammps extension and
## checks if a certain column exists before generating the data after said column is confirmed to exist
## before converting it to .csv along with the file stem taken from the file's name without having to do it manually.

import os, sys

all_the_log_files = [f for f in os.listdir() if f.endswith('lammps') and not os.path.isdir(f)]

for log_file in all_the_log_files:
    file_stem = log_file.replace('.log.lammps','')

    ## get the text from the log file
    with open(log_file, 'r') as f:
        txt = f.readlines()

    col_check_str = 'Step          Temp         v_strain      v_sigmaxx      v_sigmayy'
    end_check_str = 'Loop time of '
    columns = None
    start_idx, end_idx = 0, len(txt)

    for line_idx, line in enumerate(txt):
        if col_check_str in line:
            columns = line.strip().split()
            start_idx = line_idx + 1
        if end_check_str in line and columns:
            end_idx = line_idx - 1

    ## PRINT DEBUG
    # print(columns)
    # print(start_idx,end_idx)
    # print(data0[-1:])

    data0 = txt[start_idx:end_idx]
    data = [row for row in data0]
    columns_entry = None

    ## write the CSV file
    csv_name = f'{file_stem}.csv'
    with open(csv_name, 'w') as f:
        f.write(",".join(columns) + "\n")
        for start_idx in data:
            columns_entry = start_idx.strip().split()
            f.write(",".join(columns_entry) + "\n")
