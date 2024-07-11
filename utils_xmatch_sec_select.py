import pandas as pd

# identical to primary selection, but selects dimmest star out of two closest
def secondary_selection(matches):
    
        # if there's only one match, choose it        
        if len(matches)==1:
            gaia_id = matches['gaia_id'].iloc[ 0 ]
            index = matches['original_index'].iloc[ 0 ]
            flag = '.'
            return gaia_id, index, flag

        # if there are multiple candidates, return the closest match
        else:
            min_sep_index = matches['target_sep'].idxmin()
            gaia_id = matches['gaia_id'].iloc[ min_sep_index ]
            index = matches['original_index'].iloc[ min_sep_index ]
            flag = '!'
            
            return gaia_id, index, flag
            
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
#        # if not, pick the dimmest target out of the two closest matches
#        else:
#
#            # sort matches by increasing separation, and select the two closest stars in the match list
#            matches = matches.sort_values('target_sep').iloc[:2].reset_index(drop=True)
#
#            # get index for the dimmer one
#            max_mag_index = matches['gaia_mag'].idxmin()
#            
#            # set the variables for the match
#            gaia_id = matches['gaia_id'].iloc[ max_mag_index ]
#            index = matches['original_index'].iloc[ max_mag_index ]
#            flag = '!'
#            
#            return gaia_id, index, flag
