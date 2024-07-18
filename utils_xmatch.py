import math
import numpy as np
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord
# from utils_xmatch_pri_select import primary_selection
# from utils_xmatch_sec_select import secondary_selection

#################################################################################################################################################

# function to select primary star in xmatch
# picks the brighter of the two closest matches if there are multiple matches
def primary_selection(matches):

        if len(matches)==1:
            gaia_id = matches['designation'].iloc[ 0 ]
            index = matches['original_index'].iloc[ 0 ]
            flag = '.'
            return gaia_id, index, flag

        # if not, pick the brightest target out of the two closest matches
        # this should only be needed to catch double stars with fairly small separation
        else:

            # sort matches by increasing separation, and select the two closest stars in the match list
            matches = matches.sort_values('target_sep').iloc[:2].reset_index(drop=True)

            # get index for the brighter one
            min_mag_index = matches['phot_g_mean_mag'].idxmin()
            
            # set the variables for the match
            gaia_id = matches['designation'].iloc[ min_mag_index ]
            index = matches['original_index'].iloc[ min_mag_index ]
            flag = '!'
            
            return gaia_id, index, flag

#################################################################################################################################################

def secondary_selection( primary, matches ):
    
        # if there's only one match, choose it ##################################################        
        if len(matches)==1:
            
            gaia_id = matches['designation'].iloc[ 0 ]
            index = matches['original_index'].iloc[ 0 ]
            flag = '.'
            
            return gaia_id, index, flag
        
        # if the closest in magnitude also has the best wsi separation ###############################
        min_dm_index = matches['target_dm'].idxmin()
   
        # wsi separation to check against
        wsi_sep = primary.wsi_sep
 
        # set a skycoord object for the primary
        pri = SkyCoord( ra=primary.gaia_ra1, dec=primary.gaia_dec1, unit=u.degree )
        
        # set skycoords for the secondary candidates
        secs = SkyCoord( ra=matches.ra, dec=matches.dec, unit=u.degree )
 
        # calculate separations
        separations = pri.separation( secs )
 
        # diff in separation compared to our wsi measurement
        sep_diff = np.abs( separations.arcsec - wsi_sep )
 
        # which is the closest to our measurement?
        best_sep_index = sep_diff.argmin()

        # if these are the same star, select it as our match
        if best_sep_index == min_dm_index:
        
            # set the variables for the match
            gaia_id = matches['designation'].iloc[ min_dm_index ]
            index = matches['original_index'].iloc[ min_dm_index ]
            flag = ':'
        
            return gaia_id, index, flag
           
        # return the closest match otherwise ################################
        else:
            min_sep_index = matches['target_sep'].idxmin()
            gaia_id = matches['designation'].iloc[ min_sep_index ]
            index = matches['original_index'].iloc[ min_sep_index ]
            flag = '!'
            
            return gaia_id, index, flag
            
#################################################################################################################################################

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
    
##################################################################################################################################################

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
    
##################################################################################################################################################

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

    # drop any unwanted columns
    wsi_xmatch = wsi_xmatch.drop(columns=['gaia_target_oid1','gaia_target_oid2'])
    
    return wsi_xmatch # return combined df