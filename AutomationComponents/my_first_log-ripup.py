import os, sys

## list comprehension to gather files in this directory
log_files = [f for f in os.listdir() if f.endswith('lammps')]

## for-loop version
log_files_test = []
for f in os.listdir():
    if f.endswith('lammps'):
        log_files_test.append(f)
    ## hint: use if clause

## DEBUG PRINT
# print("log_files")
# print(log_files)
# print('log_files_test - same as log_files?')
# print(log_files_test)
##

## ------- we'll use list comprehension for the rest of the time
test_log = log_files[0]

with open(test_log, "r") as f:
    txt = f.readlines()

## check that we're loading the correct file
# print(f'\nTEST FILE: {test_log}')
# print(txt[:10])

## notes on test_log
## line 196 in Atom is the data header for file 13
## line 198 in Atom is the data header for file 16
## --> have to use a for loop check

columns = None
start_idx, end_idx = 0, len(txt)
deform_check_str = '--DEFORMATION--'
col_check_str = 'Step          Temp         v_strain      v_sigmaxx      v_sigmayy'
end_check_str = 'Loop time of '
deform_started = False
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

## for string row
data = [row for row in data0]

## to make this data numeric:
# for row in data0:
#     numeric = [float(item) for item in row]
    # data.append(row)

print(data[-1:])

with open("file_to_write.csv", "w") as f:
    f.write(",".join(columns) + "/n")
    for str_row in data:
        f.write(",".join(str_row) + "/n")
