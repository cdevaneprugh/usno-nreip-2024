import warnings
import numpy as np
import pandas as pd
from astroquery.simbad import Simbad
from astropy.utils.exceptions import AstropyWarning
from utils_simbad import A_search, AB_search, AB_rev_search

warnings.simplefilter('ignore', category=AstropyWarning)
pd.set_option('mode.chained_assignment', None)

# load wsi
wsi = pd.read_csv('data/wsi24.csv').replace({'wds_comp':np.NaN},'AB')

# ids and comps in wds
ids = list( wsi.wds_id )
comps = list( wsi.wds_comp )

sim_pri = []
sim_sec = []
sim_pri_flg = []
sim_sec_flg = []

# loop through wsi and try to find a gaia match through simbad
count = 0
for id, comp in zip( ids, comps ):

    # show progress
    count += 1
    if count % 100 == 0:
        print(count)
        
    # if it's an AB format comp, run AB_search
    if len( comp ) == 2:

        # query primary
        res1, flg1 = AB_search( id, comp )

        # query secondary with A search
        res2, flg2 = A_search( id, comp[1] ) 
    
    # if not, split the components
    else:
        pri, sec = comp.split( ',' )
        
        # query primary
        if len( pri ) == 1: # check for single letter comp first
            res1, flg1 = A_search( id, pri )
        else:
            res1, flg1 = AB_rev_search( id, pri )

        # query secondary
        if len( sec ) == 1:
            res2, flg2 = A_search( id, sec )
        else:
            res2, flg2 = AB_rev_search( id, sec )

    # append the results
    sim_pri.append( res1 )
    sim_sec.append( res2 )
    sim_pri_flg.append( flg1 )
    sim_sec_flg.append( flg2 )

# add results to data frame
wsi['sb_id1'] = sim_pri
wsi['sb_id2'] = sim_sec
wsi['sb_flg1'] = sim_pri_flg
wsi['sb_flg2'] = sim_sec_flg

# export csv
wsi.to_csv('data/wsi24.sb.csv', index=False)
