import os
import random
import subprocess as sub




__all__ = ["create_initial_box"]

def check_if_file_exists_in_other_directory(filename, directory):
    print("to be created")

def create_initial_box(L, system_name, mol_nums, mol_names, \
                       ID, dummy_single= "test.gro", nS_dummy = 0):
    """
    

    Parameters
    ----------
    path : string
        path to initial single molecule structures
    L : float
        length of simulation box
    system_name : string
        name of g96 file to create
    mol_nums : array(ints)
        array of all species
    mol_names : array(strings)
        array of all species single molecule files
    dummy_single : string, optional
        name of ghost particle single particle. The default is "test.gro".
    nS_dummy : int, optional
        number of ghost particles. The default is 0.
    ID : string
        path to gro files for individual molecule files

    Returns
    -------
    creates g96 file with initial system coordinates

    """
    print(os.path.join(ID, dummy_single))
    box_created = False
    if nS_dummy > 0:
        cmd = 'gmx insert-molecules -ci {0:s} -nmol {1:d} -box {2:f} {3:f} {4:f} \
        -seed {5:d} -o {6:s}'.format(os.path.join(ID, dummy_single), nS_dummy, L,L,L,random.randint(1,100000),system_name )
        p = sub.Popen(cmd, shell=True, stderr = sub.STDOUT, stdout = sub.PIPE).communicate()[0]
        #print(p.decode())
        box_created = True 
        
    for nmol, name in zip(mol_nums, mol_names):
        if box_created:
            cmd = 'gmx insert-molecules -ci {0:s} -f {1:s} -nmol {2:d} -seed {3:d} -o {4:s}' \
                .format(os.path.join(ID, name), system_name, nmol, random.randint(1,100000), system_name )
            p = sub.Popen(cmd, shell=True, stderr = sub.STDOUT, stdout = sub.PIPE).communicate()[0]
        else:
            cmd = 'gmx insert-molecules -ci {0:s} -nmol {1:d} -box {2:f} {3:f} {4:f} \
        -seed {5:d} -o {6:s}'.format(os.path.join(ID, name), nmol, L, L, L, random.randint(1,100000), system_name )
            p = sub.Popen(cmd, shell=True, stderr = sub.STDOUT, stdout = sub.PIPE).communicate()[0]
            box_created = True
            
