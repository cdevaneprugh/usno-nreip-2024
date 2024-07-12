import numpy as np
import pandas as pd
import astropy.units as u
from astropy.coordinates import SkyCoord

# identical to primary selection, but selects dimmest star out of two closest
def secondary_selection( primary, matches ):
    
        # if there's only one match, choose it        
        if len(matches)==1:
            
            gaia_id = matches['gaia_id'].iloc[ 0 ]
            index = matches['original_index'].iloc[ 0 ]
            flag = '.'
            
            return gaia_id, index, flag
            
        # if there are multiple candidates, return the one with the separation closest to the wsi measurement
        else:

            # wsi separation to check against
            wsi_sep = primary.wsi_sep

            # set a skycoord object for the primary
            pri = SkyCoord( ra=primary.gaia_ra1, dec=primary.gaia_dec1, unit=u.degree )
            
            # set skycoords for the secondary candidates
            secs = SkyCoord( ra=matches.gaia_ra, dec=matches.gaia_dec, unit=u.degree )

            # calculate separations
            separations = pri.separation( secs )

            # diff in separation compared to our wsi measurement
            sep_diff = np.abs( separations.arcsec - wsi_sep )

            # which is the closest to our measurement?
            match_index = sep_diff.argmin()

            # return match for candidate
            gaia_id = matches['gaia_id'].iloc[ match_index ]
            index = matches['original_index'].iloc[ match_index ]
            flag = '!'
            
            return gaia_id, index, flag
            
        # # if there are multiple candidates, return the closest match
        # else:
        #     min_sep_index = matches['target_sep'].idxmin()
        #     gaia_id = matches['gaia_id'].iloc[ min_sep_index ]
        #     index = matches['original_index'].iloc[ min_sep_index ]
        #     flag = '!'
            
        #     return gaia_id, index, flag
            
#        # find the index of the target with the smallest dm and separation
#        min_sep_index = matches['target_sep'].idxmin()
#        min_dm_index  = matches['target_dm'].idxmin()
#    
#        # if these are the same star, select it as our match
#        if min_sep_index == min_dm_index:
#            
#            # set the variables for the match
#            gaia_id = matches['gaia_id'].iloc[ min_sep_index ]
#            index = matches['original_index'].iloc[ min_sep_index ]
#            flag = ':'
#            
#            return gaia_id, index, flag
#            
       # if not, pick the dimmest target out of the two closest matches
        # else:

        #    # sort matches by increasing separation, and select the two closest stars in the match list
        #     matches = matches.sort_values('target_sep').iloc[:2].reset_index(drop=True)

        #    # get index for the dimmer one
        #     max_mag_index = matches['gaia_mag'].idxmin()
           
        #    # set the variables for the match
        #     gaia_id = matches['gaia_id'].iloc[ max_mag_index ]
        #     index = matches['original_index'].iloc[ max_mag_index ]
        #     flag = '!'
           
        #     return gaia_id, index, flag
