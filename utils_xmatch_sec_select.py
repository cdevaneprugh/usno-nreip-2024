import pandas as pd

# identical to primary selection, but selects dimmest star out of two closest
def secondary_selection(matches):
    
        # find the index of the target with the smallest dm and separation
        min_sep_index = matches['target_sep'].idxmin()
        min_dm_index  = matches['target_dm'].idxmin()
    
        # if these are the same star, select it as our match
        if  min_sep_index == min_dm_index:
            
            # set the variables for the match
            gaia_id = matches['gaia_id'].iloc[ min_sep_index ]
            index = matches['original_index'].iloc[ min_sep_index ]
            flag = '.'
            
            return gaia_id, index, flag

        # if not, pick the brightest target out of the two closest matches
        # this should only be needed to catch double stars with fairly small separation
        else:

            # sort matches by increasing separation, and select the two closest stars in the match list
            matches = matches.sort_values('target_sep').iloc[:2].reset_index(drop=True)

            # get index for the dimmer one
            max_mag_index = matches['gaia_mag'].idxmax()
            
            # set the variables for the match
            gaia_id = matches['gaia_id'].iloc[ max_mag_index ]
            index = matches['original_index'].iloc[ max_mag_index ]
            flag = '!'
            
            return gaia_id, index, flag
