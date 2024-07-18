import warnings
import numpy as np
import pandas as pd
from astroquery.simbad import Simbad
from astropy.utils.exceptions import AstropyWarning

from utils_simbad import query_gaia_by_wds

warnings.simplefilter('ignore', category=AstropyWarning)
pd.set_option('mode.chained_assignment', None)


# load wds component file
wds = pd.read_csv( 'data/simbad.comp.query/wds_components.summ.csv' ).iloc[225000:]

ids = tuple( wds.wds_id )
comps = tuple( wds.wds_comp )

# allocate array to hold ids and flags
simbad_results = []
simbad_flags = []

# loop through wsi and try to find a matches through simbad
for i, ID in enumerate( ids ):

    # show and save progress
    if i % 1000 == 0:
        print(i)
        df = pd.DataFrame( {'id':simbad_results, 'flag':simbad_flags} )
        df.to_csv( 'data/simbad.comp.query/sb.checkpoint.csv' )
    
    # if the component is an A, run the AB specific search
    if comps[i] == 'A':
    
        # try to find match for A directly
        try:
            simbad_results.append( query_gaia_by_wds( 'WDS J' + ID + 'A' ) )
            simbad_flags.append( '' )
        
        # if nothing is found, try AB
        except: 
            try:
                simbad_results.append( query_gaia_by_wds( 'WDS J' + ID + 'AB' ) )
                simbad_flags.append( '!' ) # flag that first choice wasnt found
                 
            except: # if nothing is still found, flag it
                simbad_results.append( '' )
                simbad_flags.append( '$' )

    # run a direct search for everything other component
    else:
        try:
            simbad_results.append( query_gaia_by_wds( 'WDS J' + ID + comps[i] ) )
            simbad_flags.append( '' )

        except:
            simbad_results.append( '' )
            simbad_flags.append( '$' )

# add columns to wds
wds['sb_id'] = simbad_results
wds['sb_flag'] = simbad_flags

# export csv
wds.to_csv('data/simbad.comp.query/sb.225k.end.csv', index=False)
