"""
check for errors in wds ID in the wsi24 list, by matching unique WDS IDs in wsi24 to the wds summary file
"""

import numpy as np
import pandas as pd

# read in wds and wsi24 catalog
wds = pd.read_csv('data/wds.summ.csv')
wsi = pd.read_csv('data/wsi24.csv')

# get list of unique targets in wsi24 catalog and sort them
wsi_unique_targets = np.sort( np.unique( wsi['wds_id'] ) )

# filter wds catalog based on this list
wds_reduced = wds.loc[ wds['wds_id'].isin(wsi_unique_targets) ]

# find unique targets in reduced wds catalog and sort
wds_reduced_unique_targets = np.sort( np.unique( wds_reduced['wds_id'] ) )

# compare the unique target lists
if list(wsi_unique_targets) == list(wds_reduced_unique_targets):
    print("Target Lists Match")

# if they dont match, it outputs two text files to run a diff command on
#else:
#    print("Target Lists Don't Match")
#
#    # write both lists of target names to text files 
#    # write wsi targets
#    with open('data/wsi_unique_targets.txt', 'w+') as f:
#        for items in wsi_unique_targets:
#            f.write('%s\n' %items)
#    f.close()
#    
#    # write wds targets
#    with open('data/wds_unique_targets.txt', 'w+') as f:
#        for items in wds_reduced_unique_targets:
#            f.write('%s\n' %items)
#    f.close()
