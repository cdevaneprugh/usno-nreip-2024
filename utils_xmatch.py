import numpy as np
import pandas as pd
from utils_xmatch_pri_select import primary_selection
from utils_xmatch_sec_select import secondary_selection
from utils_xmatch_crude_select import crude_selection
from utils_xmatch_gen_df import generate_xmatch_df

###################################################################################################################################################

def cross_match_loop(wsi, gaia, component_selection):

    gaia_ids = []
    indexes = [] 
    flags = []

    for oid in wsi.index:

        # get dataframe of potential matches from xmatch based on oid (index from queried wsi csv, called target_oid in gaia)
        matches = gaia.loc[ gaia['target_oid'] == oid ].reset_index(names='original_index')
       
        # run selection function, will fail if matches is empty
        try:
            gaia_id, index, flag = component_selection( matches )

        except:
            gaia_id, index, flag = '', '$', '$' # flag if there are no potential matches

        gaia_ids.append( gaia_id )
        indexes.append( index )
        flags.append( flag )

    xmatch = generate_xmatch_df(gaia, indexes, flags) # build df of matches based on saved indexes

    return xmatch

###################################################################################################################################################

def wsi_gaia_xmatch( wsi, gaia_query_pri, gaia_query_sec ):
    
    # cross match primaries ###########################################################
    xmatch_pri = cross_match_loop( wsi, gaia_query_pri, primary_selection )
    
    # rename columns
    xmatch_pri = xmatch_pri.rename( columns={'gaia_id':'gaia_id1', 'gaia_mag':'gaia_mag1',
                                             'gaia_pm':'gaia_pm1','target_dm':'wds_gaia_dm1', 
                                             'target_sep':'wds_gaia_sep1', 'gaia_flag':'gaia_flag1'} )

    # remove primary gaia id choices from secondary search pool
    primary_gaia_ids = np.unique( xmatch_pri.gaia_id1 )
    gaia_query_sec = gaia_query_sec.loc[ ~gaia_query_sec['gaia_id'].isin( primary_gaia_ids ) ].reset_index(drop=True)

    # cross match secondaries #########################################################
    xmatch_sec = cross_match_loop( wsi, gaia_query_sec, secondary_selection )
   
    # rename columns
    xmatch_sec = xmatch_sec.rename( columns={'gaia_id':'gaia_id2', 'gaia_mag':'gaia_mag2', 
                                             'gaia_pm':'gaia_pm2', 'target_dm':'wds_gaia_dm2',
                                             'target_sep':'wds_gaia_sep2','gaia_flag':'gaia_flag2'} )

    # combine wsi, primary xmatch, and secondary xmatch dataframes
    wsi_xmatch = pd.concat( [ wsi.reset_index(drop=True), 
                              xmatch_pri.reset_index(drop=True), 
                              xmatch_sec.reset_index(drop=True) ], axis=1 )

    return wsi_xmatch # return combined df
