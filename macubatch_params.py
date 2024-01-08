#! /usr/bin/env python3

import subprocess
import os

# ./macubatch_params config_file.json

# TODO : CREATE CONFIGURATION FILE TO IMPORT

# Set configuration parameters
dict_json = {
    "macufiles_dir":"/user/jemonet/home/Documents/These/Macular files/Session retinocortical/RefactoredMacular/diSymGraph_pConnecParams/",
    "macudata_dir":"/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/diSymGraph_pConnecParams/41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/ampGang/",
    "macustim_dir":"/user/jemonet/home/Documents/These/stimuli/stim_database_newName/horizontal_motion/black_background_white_bar/horizontalScreen/2700x945/bar201x270/",
    "macufiles_file":"9x3,15°_N41x15_nue0_1,86_nui0_12,66_horizWhiteBarMotion0,67x0,9°_6dps_deltat0,0167_ampOPL0,025.json",
    "macudata_file":"RC_RM_dSGpCP{num_sim}_{name_caract_sim}{value_caract_sim}{unit_caract_sim}_0f.csv",
    "macustim_file":"D187_motion30_trajX-191to2689_Y338to338_0f.mp4",
    "num_sim":["0012"],
    "name_caract_sim":"ampGang",
    "unit_caract_sim":"Hz",
    "values_caract_sim":[1, 5, 10, 15, 20, 25, 35, 40, 45, 50],
    "params_values_macular":{"virtual_retina/relative_ampOPL":
                            [0.00083, 0.004, 0.0079, 0.0119, 0.0159, 0.0198, 0.0292, 0.0333, 0.0375, 0.0417]},
}

# Create the path where saving data
if not os.path.exists(dict_json["macudata_dir"]):
    os.makedirs(dict_json["macudata_dir"])

# Create all data file name
# For a simulation with one or multiple id number simulation
if len(dict_json["num_sim"])==1:
    list_macudata_file = [dict_json["macudata_file"].replace("{num_sim}",dict_json["num_sim"][0]
                                ).replace("{name_caract_sim}",dict_json["name_caract_sim"]
                                ).replace("{value_caract_sim}",str(dict_json["values_caract_sim"][i])
                                ).replace("{unit_caract_sim}",dict_json["unit_caract_sim"])
                          for i in range(len(dict_json["values_caract_sim"]))
                         ]
else:
        list_macudata_file = [dict_json["macudata_file"].replace("{num_sim}",dict_json["num_sim"][i]
                                ).replace("{name_caract_sim}",dict_json["name_caract_sim"]
                                ).replace("{value_caract_sim}",str(dict_json["values_caract_sim"][i])
                                ).replace("{unit_caract_sim}",dict_json["unit_caract_sim"])
                          for i in range(len(dict_json["values_caract_sim"]))
                             ]

# Run each macular-batch processes
for i in range(len(list_macudata_file)):
    list_subprocess = ["macular-batch","-r",
                    "-f", f"{dict_json['macufiles_dir']}{dict_json['macufiles_file']}",
                    "-o", f"{dict_json['macudata_dir']}{list_macudata_file[i]}",]
    for param in dict_json["params_values_macular"]:
        list_subprocess += ["-p", f"{param}={dict_json['params_values_macular'][param][i]}"]
    print(list_subprocess)
    subprocess.run(list_subprocess)


