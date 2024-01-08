#! /usr/bin/env python3

import subprocess
import os
import sys
import re

macufiles_dir="/user/jemonet/home/Documents/These/Macular files/Session retinocortical/RefactoredMacular/diSymGraph_pConnecParams"
macudata_dir="/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/diSymGraph_pConnecParams/41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/barSpeed/script"
stim_dir="/user/jemonet/home/Documents/These/stimuli/stim_database_newName/horizontal_motion/black_background_white_bar/horizontalScreen/2700x945/bar201x270"
exp_reg_motion = re.compile("motion([0-9]{1,5})")

if not os.path.exists(macudata_dir):
    os.makedirs(macudata_dir)

list_num_id = [num_id for num_id in range(3,12)]
list_speed = [speed for speed in range(3,31,3) if speed!=6]

macufiles_file = "9x3,15°_N41x15_nue0_1,86_nui0_12,66_horizWhiteBarMotion0,67x0,9°_6dps_deltat0,0167_ampOPL0,025.json"
list_stim_file = [file for file in os.listdir(stim_dir) if "motion30" not in file and file[-4:]==".mp4"]
list_stim_file.sort(key=lambda x: int(exp_reg_motion.findall(x)[0]))
list_macudata_file = [f"RC_RM_dSGpCP000{i}_barSpeed{speed}dps_0f.csv" for i, speed in zip(list_num_id, list_speed)]

for stim_file, macudata_file in zip (list_stim_file, list_macudata_file):
    subprocess.run(["macular-batch","-r", "-f", f"{macufiles_dir}/{macufiles_file}", "-o", f"{macudata_dir}/{macudata_file}", "-s", f"{stim_dir}/{stim_file}"])


