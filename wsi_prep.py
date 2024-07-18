import math
import warnings
import numpy as np
import pandas as pd
from erfa import ErfaWarning

from utils_misc import reduce_targets, compare_targets, show_unique_items
from utils_wsi_epoch_prop import wsi_J2016_prop
from utils_proper_motion import total_pm

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter('ignore', category=ErfaWarning)

# read in data
# replace empty coords with AB
wsi = pd.read_csv('data/wsi24.csv').replace({'wds_comp':np.NaN},'AB')
wds = pd.read_csv('data/wds.summ.csv').replace({'wds_comp':np.NaN},'AB')

# flag remaining nans and empty mag measurements to be located ('.' in wds)
wds = wds.replace({'wds_notes':np.NaN}, '') # dont flag empty entries in wds notes
wds = wds.replace([np.NaN, '.'],'%')

# force column data types as needed
wsi = wsi.astype( {'wds_id':str, 'wds_comp':str} )
wds = wds.astype( {'wds_id':str, 'wds_comp':str, 
                   'wds_mag1':str, 'wds_mag2':str,
                   'wds_coord':str} )

# filter wsi
wsi = wsi.drop( columns=['wsi_ra_deg', 'wsi_dec_deg'] ) # drop RA and Dec columns
wsi = wsi.loc[ ~wsi['wsi_dm'].isin([0.0,7.5]) ] # mask off any entry with a dm of 0.0 or 7.5 (pipeline error)
wsi = wsi.reset_index(drop=True)

# reduce wds to targets found in wsi
wds = reduce_targets(wds, wsi)

# loop through wsi and add corresponding data from wds
primary_coords = []
primary_mags = []
secondary_mags = []
primary_pms_ra = []
primary_pms_dec = []
secondary_pms_ra = []
secondary_pms_dec = []
wds_notes = []

for i, wds_id in enumerate( wsi['wds_id'] ): # loop through wds_ids in our wsi catalog

    # define component for current entry
    component = wsi.wds_comp.iloc[i]

    # find match based on current wds id and component
    match = wds.loc[ (wds['wds_id']==wds_id) & (wds['wds_comp']==component) ]

    # add precise primary coordinate
    primary_coords.append( match.wds_coord.iloc[0] )

    # add primary mag
    primary_mags.append( match.wds_mag1.iloc[0] )

    # add secondary mag
    secondary_mags.append( match.wds_mag2.iloc[0] )

    # add primary pms
    primary_pms_ra.append( match.wds_pm1_ra.iloc[0]  )
    primary_pms_dec.append( match.wds_pm1_dec.iloc[0] )
    
    # add secondary pms
    secondary_pms_ra.append( match.wds_pm2_ra.iloc[0] )
    secondary_pms_dec.append( match.wds_pm2_dec.iloc[0] )

    # add notes
    wds_notes.append( match.wds_notes.iloc[0] )

# add the lists to the wsi dataframe
wsi['wds_coord1'] = primary_coords
wsi['wds_mag1'] = primary_mags
wsi['wds_mag2'] = secondary_mags
wsi['wds_pm1_ra'] = primary_pms_ra
wsi['wds_pm1_dec'] = primary_pms_dec
wsi['wds_pm2_ra'] = secondary_pms_ra
wsi['wds_pm2_dec'] = secondary_pms_dec
wsi['wds_notes'] = wds_notes

# drop rows with missing mags
wsi = wsi.drop( wsi.loc[ wsi['wds_mag1'] == '%' ].index ).reset_index(drop=True)
wsi = wsi.drop( wsi.loc[ wsi['wds_mag2'] == '%' ].index ).reset_index(drop=True)

# drop primaries with no pm data
wsi = wsi.drop( wsi.loc[ wsi['wds_pm1_ra'] == '%' ].index ).reset_index(drop=True)

# force mags into float
wsi = wsi.astype({'wds_mag1':float, 'wds_mag2':float})

# remove targets brighter than mag 3
wsi = wsi.loc[ wsi['wds_mag1'] > 3.0 ]
wsi = wsi.loc[ wsi['wds_mag2'] > 3.0 ]

# replace flags with nans
wsi = wsi.replace( {'wds_pm2_ra':'%', 'wds_pm2_dec':'%'}, np.nan )

# force data types
wsi = wsi.astype({'wds_pm1_ra':float, 'wds_pm1_dec':float,
                  'wds_pm2_ra':float, 'wds_pm2_dec':float}).reset_index(drop=True)

# calculate total proper motion and epoch propagation
flags = []

# if the secondary is missing proper motion data, substitute the primary's pm and flag it
for i in range( len(wsi) ):

    # is the sec pm data a nan?
    if math.isnan( wsi.wds_pm2_ra.iloc[i] ):

        # substitute primary pm
        wsi.at[i, 'wds_pm2_ra']  = wsi.wds_pm1_ra.iloc[i]
        wsi.at[i, 'wds_pm2_dec'] = wsi.wds_pm1_dec.iloc[i]
        flags.append('!')
    
    # flag that is has its own pm
    else:
        flags.append('.')

wsi['epoch_prop_flag'] = flags

# fix proper motions for flagged wds entries

# which indexes have a P flag?
P_flag = list( wsi['wds_notes'].str.contains('P') )

# correct these proper motions
for i in range( len(wsi) ):
    if P_flag[i] == True:
        wsi.at[i, 'wds_pm1_ra']  = wsi.wds_pm1_ra.iloc[i] * 10
        wsi.at[i, 'wds_pm1_dec'] = wsi.wds_pm1_dec.iloc[i] * 10
        wsi.at[i, 'wds_pm2_ra']  = wsi.wds_pm2_ra.iloc[i] * 10
        wsi.at[i, 'wds_pm2_dec'] = wsi.wds_pm2_dec.iloc[i] * 10

# calculate total proper motions and add to wsi
wsi['wds_pm1'] = total_pm( wsi.wds_pm1_ra, wsi.wds_pm1_dec )
wsi['wds_pm2'] = total_pm( wsi.wds_pm2_ra, wsi.wds_pm2_dec )

# propogate proper motions
wsi = wsi_J2016_prop( wsi )

# drop J2000 coordinate
wsi = wsi.drop( columns=['wds_coord1'])

# force data types
wsi = wsi.astype({'wds_mag1':float, 'wds_mag2':float,
                  'wds_pm1':float, 'wds_pm2':float}).reset_index(drop=True)

# export csv with original index saved to be used as an object identifier
wsi.to_csv('data/wsi24.prepped.csv', index=True, index_label='wsi_oid')
