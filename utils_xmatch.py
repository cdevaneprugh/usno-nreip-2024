import numpy as np
import pandas as pd
from utils_xmatch_pri_select import primary_selection
from utils_xmatch_sec_select import secondary_selection
from utils_xmatch_crude_select import crude_selection
from utils_xmatch_gen_df import generate_xmatch_df

###################################################################################################################################################

def primary_loop(wsi, gaia):

    gaia_ids = []
    indexes = [] 
    flags = []

    for oid in wsi.index:

        # get dataframe of potential matches from xmatch based on oid (index from queried wsi csv, called target_oid in gaia)
        matches = gaia.loc[ gaia['target_oid'] == oid ].reset_index(names='original_index')
       
        # run selection function, will fail if matches is empty
        try:
            gaia_id, index, flag = primary_selection( matches )

        except:
            gaia_id, index, flag = '', np.nan, '$' # flag if there are no potential matches

        gaia_ids.append( gaia_id )
        indexes.append( index )
        flags.append( flag )

    xmatch = generate_xmatch_df(gaia, indexes, flags) # build df of matches based on saved indexes

    return xmatch
    
###################################################################################################################################################

#!!!!!!!!!!!!!!!!!!! the only way this currently works is if you have a match for the primary !!!!!!!!!!!!!!!

def secondary_loop( wsi, gaia ):

    gaia_ids = []
    indexes = [] 
    flags = []

    for oid in wsi.index:
        
        # gaia choice of primary
        primary_choice = wsi.iloc[oid]
        
        # get dataframe of potential matches from xmatch based on oid (index from queried wsi csv, called target_oid in gaia)
        matches = gaia.loc[ gaia['target_oid'] == oid ].reset_index(names='original_index')
       
        # run selection function, will fail if matches is empty
        try:
            gaia_id, index, flag = secondary_selection( primary_choice, matches )

        except:
            gaia_id, index, flag = '', np.nan, '$' # flag if there are no potential matches

        gaia_ids.append( gaia_id )
        indexes.append( index )
        flags.append( flag )

    xmatch = generate_xmatch_df(gaia, indexes, flags) # build df of matches based on saved indexes

    return xmatch
    
###################################################################################################################################################

def wsi_gaia_xmatch( wsi, gaia_query_pri, gaia_query_sec ):
    
    # cross match primaries ###########################################################
    xmatch_pri = primary_loop( wsi, gaia_query_pri )
    
    # rename columns
    xmatch_pri = xmatch_pri.rename( columns={'gaia_id':'gaia_id1', 'gaia_mag':'gaia_mag1', 'gaia_pm':'gaia_pm1',
                                             'gaia_ra':'gaia_ra1', 'gaia_dec':'gaia_dec1', 'target_dm':'wds_gaia_dm1', 
                                             'target_sep':'wds_gaia_sep1', 'gaia_flag':'gaia_flag1'} )

    # remove primary gaia id choices from secondary search pool #######################
    primary_gaia_ids = np.unique( xmatch_pri.gaia_id1 )
    gaia_query_sec = gaia_query_sec.loc[ ~gaia_query_sec['gaia_id'].isin( primary_gaia_ids ) ].reset_index(drop=True)

    # add primary matches to wsi ######################################################
    wsi_primaries_matched = pd.concat( [ wsi.reset_index(drop=True), xmatch_pri.reset_index(drop=True) ], axis=1 )
    
    # cross match secondaries #########################################################
    xmatch_sec = secondary_loop( wsi_primaries_matched, gaia_query_sec )
    
    # rename columns
    xmatch_sec = xmatch_sec.rename( columns={'gaia_id':'gaia_id2', 'gaia_mag':'gaia_mag2', 'gaia_pm':'gaia_pm2',
                                             'gaia_ra':'gaia_ra2', 'gaia_dec':'gaia_dec2', 'target_dm':'wds_gaia_dm2',
                                             'target_sep':'wds_gaia_sep2','gaia_flag':'gaia_flag2'} )

    # combine wsi, primary xmatch, and secondary xmatch dataframes
    wsi_xmatch = pd.concat( [ wsi.reset_index(drop=True), 
                              xmatch_pri.reset_index(drop=True), 
                              xmatch_sec.reset_index(drop=True) ], axis=1 )

    return wsi_xmatch # return combined df
