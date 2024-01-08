#! /bin/bash
REPERTOIRE_MACUFILES="/user/jemonet/home/Documents/These/Macular files/Session retinocortical/RefactoredMacular/diSymGraph_pConnecParams"
REPERTOIRE_MACUDATA="/user/jemonet/home/Documents/These/Data Macular/RefactoredMacular/diSymGraph_pConnecParams/41x15c/horizontal_white_bar/bar0,67x0,9°_6dps/barSpeed"
REPERTOIRE_STIM="/user/jemonet/home/Documents/These/stimuli/stim_database_newName/horizontal_motion/black_background_white_bar/horizontalScreen/2700x945/bar201x270"


macular-batch -r -f "$REPERTOIRE_MACUFILES/9x3,15°_N41x15_nue0_1,86_nui0_12,66_horizWhiteBarMotion0,67x0,9°_6dps_deltat0,0167_ampOPL0,025.json" \
-o "$REPERTOIRE_MACUDATA/" \
-s "$REPERTOIRE_STIM/"


