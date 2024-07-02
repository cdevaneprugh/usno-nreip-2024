import numpy as np
import pandas as pd

# import wds as dataframe
wds = pd.read_csv('data/wds_components.summ.csv').replace(np.NaN, '')
wsi = pd.read_csv('data/wsi24.csv').replace(np.NaN, '')

# filter wds based on wsi targets

# list of unique targets remaining in wsi (using WDS ID)
wsi_unique_targets = list( np.unique( wsi['wds_id'] ) )

# reduce wds catalog based on the wsi unique targets
wds = wds.loc[ wds['wds_id'].isin(wsi_unique_targets) ]

# reset index
wds = wds.reset_index(drop=True)

# find number of empty coordinates

# get list of unique coordinates
uniq_coord = np.unique(wds.wds_coord)

# 'empty coord'
empty_coord = uniq_coord[0]

# entries in the wds with this coordinate
wds_blanks = wds.loc[ wds.wds_coord == empty_coord ]

# unique targets with this coord
targ_list = np.unique( wds_blanks.wds_id )

# find the wsi entries that correspond
wsi = wsi.loc[ wsi['wds_id'].isin(targ_list) ]

wsi_targs = np.unique(wsi.wds_id)

print('targets with possible issues in wsi')
for target in wsi_targs:
    print(target)
print('------------------------------------------------------')

print('wsi entries for these targets')
print(wsi.loc[:,['wds_id','wds_comp']])

print('------------------------------------------------------')

# look at all observations in wds of these targets
print('wds entries for these targets')
print(wds.loc[ wds['wds_id'].isin(targ_list) ].loc[:,['wds_id','wds_comp','wds_coord']])
