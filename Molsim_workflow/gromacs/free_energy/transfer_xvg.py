import numpy as np
import fileinput
import os
import shutil


directory = os.path.abspath(os.curdir)
target = "npt_pro"

directory_list = [dI for dI in os.listdir(directory) if os.path.isdir(os.path.join(directory,dI))]
directory_list.remove('__pycache__')
directory_list = [ x for x in directory_list if "free" not in x.lower() ]
xvg_list = []
for entry in directory_list:
    run_num = entry.split('_')[1]
    folder_name = "Free_Energy_" + str(run_num)
    try:
        os.makedirs(folder_name)
    except OSError as e:
        print('folder {} already exists'.format(folder_name))
    lambda_dir = os.path.join(directory, entry)
    fep_dir = os.path.join(directory, folder_name)
    
    for folder in os.listdir(lambda_dir):
        if type(int(folder.split('_')[1])) == int:
            postfix = folder.split('_')[1]
            this_lambda_dir = os.path.join(lambda_dir, folder)
            try:
                xvg_file = os.path.join(this_lambda_dir, target + '.xvg')
                fep_file = os.path.join(fep_dir, target + '_' + str(postfix) + '.xvg')
                if os.path.exists(xvg_file):
                    shutil.copy(xvg_file, fep_file)
            except:
                print('failed to copy {} to {}'.format(xvg_file, fep_file))
            
            
        

