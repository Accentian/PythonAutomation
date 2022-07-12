import os, sys

log_files = [f for f in os.listdir() if f.endswith('lammps')]

## DEBUG PRINT
# print("log_files")
# print(log_files)
# print('log_files_test - same as log_files?')
# print(log_files_test)
# print(start_idx)
# print(end_idx)
# #

test_log = log_files[1]

with open(test_log, "r") as f:
    txt = f.readlines()

## notes on test_log
## line 196 in Atom is the data header for CNT_13_12_1.696
## --> have to use a for loop check

start_idx, end_idx = 0, len(txt)
col_check_str = 'Step          Temp         v_strain      v_sigmaxx      v_sigmayy'
end_check_str = 'Loop time of '
columns = None

for line_idx, line in enumerate(txt):
    if col_check_str in line:
        columns = line.strip().split()
        start_idx = line_idx + 1
    if end_check_str in line and columns:
        end_idx = line_idx - 1

print(columns)
print(start_idx,end_idx)
data0 = txt[start_idx:end_idx]
print(data0[-1:])

data = [row for row in data0]
columns_entry = None

with open("CNT_16_14_2.036.csv", "w") as f:
    f.write(",".join(columns) + "\n")
    for start_idx in data:
        columns_entry = start_idx.strip().split()
        f.write(",".join(columns_entry) + "\n")
