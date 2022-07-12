import os, sys
import shutil

bash_src = '/home/bcma/AutomationDump/script_template/CNT_n_m_d.bash'

## Testing components that parse the file names
all_the_data_files = [f for f in os.listdir() if f.endswith('.dat')]

for data_file in all_the_data_files:
    file_stem = data_file.replace('.dat','')

    # Test Component for .dat files
    with open(data_file, 'r') as f:
        lines = f.readlines()
        for row, line in enumerate(lines):
            if row in [3]:
                rm_newline = line.strip('\n')
                float_value = float(rm_newline)    #TEST
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

    ## Create bash script
    bash_name = f'{file_stem}.bash'
    bash_dst = f'/home/bcma/AutomationDump/{bash_name}'

    ## Fit number of atoms to number of nodes
    float_value = round((float_value / 45) / 16)
    str_value = str(float_value)
    #print(float_value)

    try:
        shutil.copy(bash_src, bash_dst)
        print('Bash script successfully copied.')
    except Exception as e:
        print('Bash script was not copied successfully.')

    with open(bash_name, 'r') as f:
        lines3 = f.readlines()

    bash_job_name = f'#SBATCH --job-name {file_stem}\n'
    bash_num_nodes = f'#SBATCH --nodes={str_value}\n'
    bash_input = f'mpiexec --n $(($cores*$nodes)) /ascldap/users/bcma/lammps-develop/build/lmp -in {file_stem}.in'

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
