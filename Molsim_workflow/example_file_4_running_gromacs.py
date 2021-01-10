# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 03:09:34 2020

@author: Braden Kelly

template for running gromacs simulations
"""
from datetime import datetime
import os
import numpy as np


from Molsim_workflow.gromacs.mdp_options import MdpFile
from Molsim_workflow.gromacs.auxillary import create_initial_box
from Molsim_workflow.gromacs.run import run_gromacs
from Molsim_workflow.subprocess.subprocess import make_folder

       
def execute(function, failure_message="", *args, **kwargs):
    """
    runs the passed function using commandline (subprocess)
    
    Parameters
    -----------
    function : function
        a commandline function called using subprocess
    failure_message : formatted string
        a message saying where the program has failed at
    *args : list
        list of input variables to send to the commandline function
    **kwargs : list
        list of input variables to send to the commandline function
        
    Returns
    --------
    Runs the command line function
    
    """
    
    try:  
        function(*args, **kwargs) 
    except Exception as exception:
        print(exception)
        raise RunTimeError(failure_message)
        
# label necessary directories
import Molsim_workflow
molsim_dir_path = os.path.dirname(Molsim_workflow.__file__)
gmx_topol_path = os.path.join(molsim_dir_path, 'gromacs/topologies/')
single_structs_path = os.path.join(molsim_dir_path,'structures/single_molecule')
system_structs_path = os.path.join(molsim_dir_path,'structures/system')
data_path = os.path.join(molsim_dir_path,'data')

# paths can be easily modified. For instance, if you want to put all topologies and mdp
# files in the same folder as this script, you can simply uncomment the following:
# initial_directory = os.path.abspath(os.curdir)      # starting directory (this one)
# ID = initial_directory                              # Abbreviated name for starting directory
# gmx_topol_path = ID
# single_structs_path = ID
# system_structs_path = ID                            # system_structs_path is not currently used anywhere.
# data_path = ID                                      # data_path is not currently used anywhere.


############################################################
#
#                     USER INPUTS
#
############################################################      
# TODO add option to add more mdp inputs other than default attributes in mdp_options        
num_replicates = 1                                  # number of replicate runs to do
num_lambdas = 10                                     # number of lambda windows
vdw_lambdas = ""                            
for item in np.linspace(0, 1, num_lambdas + 1):
    vdw_lambdas += str(item) + " "
box = 3.4  # nm     box length
T = 239.6  # Kelvin temperature
P = 2094.9 # bar    pressure
mol_nums = np.array([333, 333, 333])                # composition
mol_names = np.array(["A.pdb", "D.pdb", "E.pdb"])   # names of molecule files
coupled_mol = "ED"                                  # if doing alchemical, name of molecule to couple
user_info = {"name" : "Braden Kelly", "date" : str(datetime.now())} # information to add to files 
top = "A_D_E.top"                                   # name of topology file to be used
top_path = os.path.join(gmx_topol_path, top)
title = "A_D_E"                                     # title for mdp file
max_lambda_iter = 1
npt_equil_steps = 10000
npt_pro_steps = 20000

# some flexibility can be added. This assumes all alchemical replicates have same # of lambdas
num_lambda_array = [num_lambdas for i in range(num_replicates)]
start_lambda = np.zeros((num_replicates),dtype = int)

# array of starting points... i.e., if we have already done 4 lambdas for one replicate, we can start at lambda 5
start_lambda[0] = 0                                 
failure_message = "Failed at {} for replicate {} lambda {}"

############################################################
#
#              Begin loop over replicates
#
############################################################ 

for i in range(0, num_replicates):
    
    new_folder = "run_" + str(i)
    try:
        make_folder(new_folder)                     # each replicate run gets a new folder
    except:
        print('folder for run {} already exists'.format(i))
    os.chdir(new_folder)
    run_fold = os.path.abspath(os.curdir)
    
    # for each replicate run, do all of the lambda windows
    for j in range(start_lambda[i] , num_lambda_array[i] + 1):
        
        counter = 0
        passed = True
        while counter < max_lambda_iter:
            # try to make the following series of simulations. If it fails, try again maxIt times.
            try:
                #lambda_fold = os.path.abspath(os.curdir)
                new_folder = "lambda_" + str(j)
                # try to make a folder, if it already exists (follow except clause), go into it and delete everything for a fresh start.
                try:
                    make_folder(new_folder)
                    os.chdir(new_folder)
                    lambda_fold = os.path.abspath(os.curdir)
                except:
                    print('folder for lambda {} exists'.format(j))
                    os.chdir(new_folder)
                    lambda_fold = os.path.abspath(os.curdir)
                    # remove files already in the folder
                    for f in os.listdir(lambda_fold):
                        os.remove(f)
                        
                this_scenario = "generating system box"
                execute(create_initial_box,
                     failure_message.format(this_scenario, i, j),
                     box, "system.g96", mol_nums, mol_names, single_structs_path,
                     dummy_single = "E_dummy.pdb", nS_dummy =1                     
                     )

                # make enmin file
                enmin_dict = {"couple-moltype" : coupled_mol, 
                             "vdw-lambdas" : vdw_lambdas,
                              "init_lambda_state" : j}
                              
                runtype = "min free" 
                enmin = MdpFile(user_info=user_info, custom_defs=enmin_dict,
                                filename="EM.mdp", title=title, runtype=runtype
                                )
                this_scenario = "energy minimization"
                execute(run_gromacs, failure_message.format(this_scenario, i, j),
                        "system.g96", "enmin", "EM.mdp" , top_path
                        )
                
                # equilibrate NPT                
                nptEquil_dict = {"ref-t":T, "ref-p": P, "nsteps":npt_equil_steps, "couple-moltype":coupled_mol,
                                 "vdw-lambdas":vdw_lambdas, "init_lambda_state":j}
                runtype = "lang baro free"  # use langevin integrator, default barostat(Paranello-Rahman) and do free energy calculation
                # this creates an mdp file in the current working directory, but nptEquil is also an object              
                nptEquil = MdpFile( user_info=user_info, custom_defs = nptEquil_dict,
                                    filename = "npt_equil.mdp", title = title,
                                    runtype = runtype)
                # run gromacs using the mdp file just generated. Start config is taken from enmin.g96, final config is saved as npt_equil.g96
                this_scenario = "npt equilibration"
                execute(run_gromacs, failure_message.format(this_scenario, i, j),
                        "enmin.g96", "npt_equil", "npt_equil.mdp" , top_path
                        )
                
                # production NPT
                runtype = "lang baro free"
                nptPro_dict = {"ref-t":T, "ref-p": P, "nsteps":npt_pro_steps, "couple-moltype":coupled_mol,
                               "vdw-lambdas":vdw_lambdas, "init_lambda_state":j}
                nptPro = MdpFile( user_info=user_info, custom_defs = nptPro_dict,
                                    filename = "npt_pro.mdp", title = title,
                                    runtype = runtype)
                # run gromacs using the mdp file just generated. Start config is taken from npt_equil.g96, final config is saved as npt_pro.g96
                this_scenario = "npt production"
                execute(run_gromacs, failure_message.format(this_scenario, i, j),
                        "npt_equil.g96", "npt_pro", "npt_pro.mdp" , top_path
                        )

                os.chdir( os.path.abspath(os.path.join(os.getcwd(),"../")) )  # Back one directory
            except:
                print("failed", i, j)
                counter += 1
                passed = False
                os.chdir( os.path.abspath( os.path.join(os.getcwd(), "../")) )
            if passed:
                break
    os.chdir( os.path.abspath(os.path.join(os.getcwd(),"../")) )  # Back one directory
 
 
