# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 04:55:29 2020

@author: bkell
"""

__all__ = [
    "MdpFile",
    "mdp_options",
    "mdp_categories",
    ]

class MdpFile():
    
    # def __init__(self, protocols, user_info, filename = "filename.mdp", title = "default_title"):
    def __init__(self, user_info={}, custom_defs={}, filename = "filename.mdp",
                 title = "default_title", runtype=""):
        """
        Initialize a mdp file instance
        
        Parameters
        ----------
        title : string
        custom_defs : Dict
            contains user specified simulation protocols for gromacs
        user_info : Dict
            contains user name, the date
        filename : string
            whatever the user wants the file to be called
        runtype : string
            all parameters for the molecular dynamics simulation
        title : string
            name for the simulation
        """
        print("Starting initialization")
        self.title = title
        self.user_info = user_info
        # self.mdp_options = protocols
        self.filename = filename
        print("1")
        self.prep_output_file(runtype)
        print("modify")
        self.modify_output_file(custom_defs)
        print("output")
        self.make_output_file()
        
    def prep_output_file(self, run_type):
        """
        
        Parameters
        -----------
        run_type : string
            contains a series of key words

        """
        import copy
        self.mdp_options = copy.deepcopy(mdp_options)
        
        if "min" in run_type.lower() or "enmin" in run_type.lower():
            self.mdp_options['integrator'][1] = "steep" 
            self.mdp_options.update(mdp_categories['mdp_em'])
            self.mdp_options['nsteps'][1] = 20000
            self.mdp_options['dt'][0] = "; dt    =  "
        if "md" in run_type.lower():
            self.mdp_options['integrator'][1] = "md"
            
        self.mdp_options.update(mdp_categories['mdp_output'])
        self.mdp_options.update(mdp_categories['mdp_cutoffs'])
        if "pme" in run_type.lower():
            self.mdp_options.update(mdp_categories['mdp_ewald'])
        else:
            self.mdp_options.update(mdp_categories['mdp_coul'])
        if "stoich" in run_type.lower() or "lang" in run_type.lower():
            self.mdp_options.update(mdp_categories['mdp_temp_langevin'])
        else:
            self.mdp_options.update(mdp_categories['mdp_temp_thermo'])
        # if using barostat
        if "baro" in run_type.lower() or "npt" in run_type.lower():
            self.mdp_options.update(mdp_categories['mdp_pressure'])
        self.mdp_options.update(mdp_categories['mdp_init'])
        # if using LINCS
        self.mdp_options.update(mdp_categories['mdp_constraints'])
        # if doing free energy calculation
        if "free" in run_type.lower() or "fep" in run_type.lower():
            self.mdp_options.update(mdp_categories['mdp_free'])
            
    def modify_output_file(self, custom_dict):
        for key, value in custom_dict.items():
            self.mdp_options[key][1] = value
    
    def make_output_file(self):
        f = open(self.filename, 'w')
        f.write('{}\n'.format('; ' + self.title))
        
        for value in self.user_info.values():
            f.write('{}\n'.format('; ' + str(value)))
        f.write('\n\n')
        
        for value in self.mdp_options.values():
            f.write('{}\n'.format(value[0] + str(value[1])))



mdp_options = {"integrator":["integrator  =  ", "sd"],
               "initial time":["tinit = ", 0],
               "initial step":["init-step   = ", 0],
               "dt" : ["dt  = ", 0.002],
               "nsteps" : ["nsteps  = ", 1000000],                                                    
               }
mdp_em = {"emtol" : ["emtol   =  ", 100],
          "emstep" : ["emstep   =  ", 0.01]    
    }

mdp_output = { "comm-mode" : ["comm-mode   =  ", "Linear"],
               "nstcomm" : ["nstcomm   = ", 10],
               "nstxout" : ["nstxout   =  ", 0],
               "nstvout" : ["nstvout   =  ", 0],
               "nstfout" : ["nstfout   =  ", 0],
               "nstlog" : ["nstlog   =  ", 0],
               "nstenergy" : ["nstenergy   =  ", 10000],
               "nstcheckpoint" : ["nstcheckpoint  =  ", 100000],
               "cutoff-scheme" : ["cutoff-scheme   =  ", "Verlet"],
               "nstlist" : ["nstlist   =  ", 10],
               "ns-type" : ["ns-type   =  ", "grid"]
               }

mdp_cutoffs = {"pbc" : ["pbc   =  ", "xyz"],
               "periodic-molecules" : ["periodic-molecules   =  ", "no"],
               "rlist" : ["rlist   =  ", 1.5],
               "rcoulomb" : ["rcoulomb   =  ", 1.2],
               "vdwtype" : ["vdwtype   =  ", "switch"],
               "rvdw-switch" : ["rvdw-switch   =  ", 1.18],
               "rvdw" : ["rvdw   =  ", 1.2],
               "DispCorr" : ["DispCorr   =  ", "EnerPres"]
               }

mdp_ewald = {"coulombtype" : ["coulombtype   =  ", "PME"],
             "fourierspacing" : ["fourierspacing   =  ", 0.10],
             "pme-order" : ["pme-order   =  ", 6],
             "ewald-rtol" : ["ewald-rtol   =  ", "1e-06"],
             "ewald-geometry" : ["ewald-geometry   =  ", "3d"],
             "epsilon-surface" : ["ns-type   =  ", 0],
             "optimize_fft" : ["optimize_fft   =  ", "yes"]
               }
mdp_coul = {"coulombtype" : ["coulombtype   =  ", "cutoff"],
            "epsilon-r" : ["epsilon-r   = ", 0.9],
    }

mdp_temp_langevin = {"tcoupl" : ["tcoupl   =  ", "no"],
               "tc_grps" : ["tc_grps   =  ", "system"],
               "tau-t" : ["tau-t   =  ", 2.0],
               "ref-t" : ["ref-t   =  ", 298.15],
               "nsttcouple" : ["nsttcouple   =  ", 1]
               }
mdp_temp_thermo = {"tcoupl" : ["tcoupl   =  ", "berendsen"],
               "tc_grps" : ["tc_grps   =  ", "system"],
               "tau-t" : ["tau-t   =  ", 2.0],
               "ref-t" : ["ref-t   =  ", 298.15],
               }

mdp_pressure = {"pcoupl" : ["pcoupl   =  ", "Parrinello-Rahman"],
               "pcoupltype" : ["pcoupltype   =  ", "isotropic"],
               "tau-p" : ["tau-p   =  ", 5.0],
               "ref-p" : ["ref-p   =  ", 1.0],
               "compressibility" : ["compressibility   =  ", "4.5e-5"],
               "nstpcouple" : ["nstpcouple   =  ", 1]
               }

mdp_init = {   "gen-vel" : ["gen-vel   =  ", "no"],
               "gen-temp" : ["gen-temp   =  ", "298.15"],
               "gen-seed" : ["gen-seed   =  ", "123456"]
               }

mdp_constraints = {"constraints" : ["constraints   =  ", "all-bonds"],
               "constraint-algorithm" : ["constraint-algorithm  =  ", "LINCS"],
               "lincs-order" : ["lincs-order   =  ", 12],
               "lincs-iter" : ["lincs-iter   =  ", 1],
               "lincs-warnangle" : ["lincswarnangle   =  ", 45],
               "morse" : ["morse   =  ", "no"]    
               }

mdp_free = {"free-energy" : ["free-energy   =  ", "yes"],
            "sc-alpha" : ["sc-alpha   =  ", 0.5],
            "sc-r-power" : ["sc-r-power   =  ", 6],
            "sc-power" : ["sc-power   =  ", 1],
            "couple-moltype" : ["couple-moltype   =  ", " "],
            "init_lambda_state" : ["init_lambda_state   =  ", " "],
            "couple-lambda0" : ["couple-lambda0   =  ", "vdw-q"],
            "couple-lambda1" : ["couple-lambda1   =  ", "none"],
            "couple-intramol" : ["couple-intramol   =  ", "no"],
            "vdw-lambdas" : ["vdw-lambdas   =  ", " "],
            "coul-lambdas" : ["coul-lambdas   =  ", " "],
            "calc-lambda-neighbors" : ["calc-lambda-neighbors  =  ", -1],
            "nstdhdl" : ["nstdhdl   =  ", 100]
            }

mdp_categories = {"mdp_output" : mdp_output,
                  "mdp_em" : mdp_em,
                  "mdp_cutoffs" : mdp_cutoffs,
                  "mdp_ewald" : mdp_ewald,
                  "mdp_coul" : mdp_coul,
                  "mdp_temp_langevin" : mdp_temp_langevin,
                  "mdp_temp_thermo" : mdp_temp_thermo,
                  "mdp_pressure" : mdp_pressure,
                  "mdp_init" : mdp_init,
                  "mdp_constraints" : mdp_constraints,
                  "mdp_free" : mdp_free
                  }
