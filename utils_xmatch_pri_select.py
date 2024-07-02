import pandas as pd

# function to select primary star in xmatch
# will first check if the star with the smallest separation also has the closest mag
# picks the brighter of the two closest matches if first condition isnt true
def primary_selection(matches):
    
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

            # get index for the brighter one
            min_mag_index = matches['gaia_mag'].idxmin()
            
            # set the variables for the match
            gaia_id = matches['gaia_id'].iloc[ min_mag_index ]
            index = matches['original_index'].iloc[ min_mag_index ]
            flag = '!'
            
            return gaia_id, index, flag
