# CREDIT: Megan McCarthy
# COMPILED: Brandon Ma

import os, sys

all_the_data_files = [f for f in os.listdir() if f.endswith('.dat')]

for data_file in all_the_data_files:
    file_stem = data_file.replace('.dat','')

    ## get the text from the log file
    with open(data_file, 'r') as f:
        txt = f.readlines()

    col_check_str = 'Atoms'
    columns = None
    start_idx, end_idx = 0, len(txt)

    for line_idx, line in enumerate(txt):
        if col_check_str in line:
            columns = line.strip().split()
            start_idx = line_idx + 1

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
