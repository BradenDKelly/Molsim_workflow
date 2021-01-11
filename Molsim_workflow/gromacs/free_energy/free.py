from alchemlyb.parsing.gmx import extract_u_nk
import pandas as pd
import os

R = 8.31446261815324 / 1000   # kJ / mol / K
T = 239.6                     # K, Kelvin

# get xvg files in this folder
directory = os.path.abspath(os.curdir)
file_list = []
for file in os.listdir(directory):
    if file.endswith('xvg'):
        file_list.append(file)

u_nk = pd.concat([extract_u_nk(xvg, T=239.6) for xvg in file_list])

from alchemlyb.estimators import MBAR

mbar = MBAR().fit(u_nk)

print("FEP {} kT +/- {}".format(mbar.delta_f_.loc[0.00, 1.00], mbar.d_delta_f_.loc[0.00, 1.00]))
print("FEP {} kJ/mol +/- {}".format(mbar.delta_f_.loc[0.00, 1.00] * R * T, mbar.d_delta_f_.loc[0.00, 1.00] * R * T))
# print(mbar.delta_f_)
# print(mbar.d_delta_f_)
