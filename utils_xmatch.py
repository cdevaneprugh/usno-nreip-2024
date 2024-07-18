import math
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

    xmatch = gaia.iloc[ indexes ].drop( columns=['wds_id','wds_comp','wsi_sep','target_ra','target_dec','target_sep','target_dm','target_mag'] )
    xmatch['flag'] = flags

    return xmatch
    
###################################################################################################################################################

#!!!!!!!!!!!!!!!!!!! the only way this currently works is if you have a match for the primary !!!!!!!!!!!!!!!!!!!!!

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
    
    # filter nans out of index
    filtered_indexes = [x for x in indexes if not math.isnan(x)]
    
    # build dataframe of xmatches
    xmatch = gaia.iloc[ filtered_indexes ].drop( columns=['wds_id','wds_comp','wsi_sep','target_ra','target_dec','target_sep','target_dm','target_mag'] ).reset_index(drop=True)
    
    # empty dataframe to hold spots where we are missing secondaries
    empty_df = pd.DataFrame( index = wsi.index, columns = xmatch.columns )
    empty_df['target_oid'] = wsi.wsi_oid

    # loop through the found matches and add them to the empty dataframe
    for i, oid in enumerate( xmatch.target_oid ):
        empty_df.iloc[oid] = xmatch.iloc[i]
    
    empty_df['flag'] = flags
    return empty_df
    
###################################################################################################################################################

def wsi_gaia_xmatch( wsi, gaia_query_pri, gaia_query_sec ):
    
    # cross match primaries ###########################################################
    xmatch_pri = primary_loop( wsi, gaia_query_pri )
    
    # rename columns
    xmatch_pri = xmatch_pri.add_prefix('gaia_').add_suffix('1')

    # remove primary gaia id choices from secondary search pool #######################
    primary_gaia_ids = np.unique( xmatch_pri.gaia_designation1 )
    gaia_query_sec = gaia_query_sec.loc[ ~gaia_query_sec['designation'].isin( primary_gaia_ids ) ].reset_index(drop=True)

    # add primary matches to wsi ######################################################
    wsi_primaries_matched = pd.concat( [ wsi.reset_index(drop=True), xmatch_pri.reset_index(drop=True) ], axis=1 )

    # cross match secondaries #########################################################
    xmatch_sec = secondary_loop( wsi_primaries_matched, gaia_query_sec )
    
    # rename columns
    xmatch_sec = xmatch_sec.add_prefix('gaia_').add_suffix('2')

    # combine wsi, primary xmatch, and secondary xmatch dataframes
    wsi_xmatch = pd.concat( [ wsi.reset_index(drop=True), 
                              xmatch_pri.reset_index(drop=True), 
                              xmatch_sec.reset_index(drop=True) ], axis=1 )

    # drop any unneeded columns
    wsi_xmatch = wsi_xmatch.drop(columns=['gaia_target_oid1','gaia_target_oid2'])
    
    return wsi_xmatch # return combined df