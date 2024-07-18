import numpy as np
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord

wsi = pd.read_csv('data/wsi24.xmatch.csv')

# calculate separation of gaia choices (when available)
pri = SkyCoord( ra=wsi.gaia_ra1.to_list()*u.deg, dec=wsi.gaia_dec1.to_list()*u.deg, frame='icrs' )
sec = SkyCoord( ra=wsi.gaia_ra2.to_list()*u.deg, dec=wsi.gaia_dec2.to_list()*u.deg, frame='icrs' )
sep = pri.separation(sec).arcsec
wsi['gaia_sep'] = sep

# calculate Bp-Rp color for primaries and secondaries
wsi['gaia_br_diff1'] = wsi.gaia_phot_bp_mean_mag1 - wsi.gaia_phot_rp_mean_mag1
wsi['gaia_br_diff2'] = wsi.gaia_phot_bp_mean_mag2 - wsi.gaia_phot_rp_mean_mag2

# isolate filters
y = wsi.loc[ wsi.wsi_filter=='y' ].reset_index(drop=True)
V = wsi.loc[ wsi.wsi_filter=='V' ].reset_index(drop=True)

# read in sythetic photometry results
STG1 = pd.read_csv( 'data/syn.phot/STG1.syn.csv' )
STG2 = pd.read_csv( 'data/syn.phot/STG2.syn.csv' )
JKC1 = pd.read_csv( 'data/syn.phot/JKC1.syn.csv' )
JKC2 = pd.read_csv( 'data/syn.phot/JKC2.syn.csv' )

# loop through y dataframe and pull synthetic mags for primary and secondary
y1_mags = []
y2_mags = []

for pri, sec in zip( y.gaia_designation1, y.gaia_designation2 ):

    try:
        pri_id = int( pri[9:] ) # primary gaia designation to source id as an int 

        # pull stromgren y mag and add to list
        mag = STG1.loc[ STG1.source_id == pri_id ].StromgrenStd_mag_y.iloc[0]
        y1_mags.append( mag )
        
    except:
        y1_mags.append( np.nan )
    
    # try for secondary, will fail at nan
    try:
        sec_id = int( sec[9:] )
        mag = STG2.loc[ STG2.source_id == sec_id ].StromgrenStd_mag_y.iloc[0]
        y2_mags.append( mag )
        
    # append a nan if no id was found
    except:
        y2_mags.append(np.nan)

# loop through V dataframe and pull synthetic mags for primary and secondary
V1_mags = []
V2_mags = []

for pri, sec in zip( V.gaia_designation1, V.gaia_designation2 ):

    try:
        pri_id = int( pri[9:] ) # primary gaia designation to source id as an int 

        # pull stromgren y mag and add to list
        mag = JKC1.loc[ JKC1.source_id == pri_id ].JkcStd_mag_V.iloc[0]
        V1_mags.append( mag )
        
    except:
        V1_mags.append( np.nan )
    
    # try for secondary, will fail at nan
    try:
        sec_id = int( sec[9:] )
        mag = JKC2.loc[ JKC2.source_id == sec_id ].JkcStd_mag_V.iloc[0]
        V2_mags.append( mag )
        
    # append a nan if no id was found
    except:
        V2_mags.append(np.nan)

# add to data frames
y['syn1'] = y1_mags
y['syn2'] = y2_mags
V['syn1'] = V1_mags
V['syn2'] = V2_mags

# calculate synthetic dm
y['syn_dm'] = np.abs( y.syn1 - y.syn2 )
V['syn_dm'] = np.abs( V.syn1 - V.syn2 )

# concat data frames
wsi_syn = pd.concat( [y.reset_index(drop=True), V.reset_index(drop=True)] ).reset_index(drop=True)
wsi_syn = wsi_syn.sort_values(['wsi_oid']).reset_index(drop=True)

# export data
wsi_syn.to_csv('data/syn.phot/wsi24.syn.csv', index=False)
y.to_csv('data/syn.phot/y.syn.csv', index=False)
V.to_csv('data/syn.phot/v.syn.csv', index=False)
