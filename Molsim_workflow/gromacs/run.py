# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 21:33:33 2020

@author: bkell
"""

import subprocess as sub
import random

__all__ = ["run_gromacs"]

def run_gromacs(g96Name,ensembleName,mdpName, top): # calls grompp, then runs the md
    """ 
    Parameters
    -----------
    g96Name : string
        name of the g96 file with all molecule postions
    ensembleName : string
        name of the output tpr file
    top : string
        name of the topology file being used
    
    Returns
    --------
    calls gromacs and creates many files
    
    """

    cmd = 'gmx grompp -c {0:s} -p {1:s} -f {2:s} -o {3:s}.tpr'.format(g96Name, top, mdpName, ensembleName)
    p = sub.Popen(cmd, shell=True, stderr = sub.STDOUT, stdout = sub.PIPE).communicate()[0]
    print(p.decode())
    cmd = 'gmx mdrun -deffnm {0:s} -c {1:s}'.format(ensembleName,ensembleName + '.g96')
    p = sub.Popen(cmd, shell=True, stderr = sub.STDOUT, stdout = sub.PIPE).communicate()[0]
    print(p.decode())
    

