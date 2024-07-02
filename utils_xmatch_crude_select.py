import pandas as pd

# find the match with the closest separation and delta magnitude
# drops targets with increasing separation until condition is true
def crude_selection(matches):

        # find the index of the target with the smallest dm and separation
        min_sep_index = matches['target_sep'].idxmin()
        min_dm_index  = matches['target_dm'].idxmin()

        # does the candidate with the smallest separation also have the smallest dm?
        if  min_sep_index == min_dm_index:

            gaia_id = matches['gaia_id'].iloc[ min_sep_index ]
            index = matches['original_index'].iloc[ min_sep_index ]
            flag = '.'
            
            return gaia_id, index, flag
            
        # if target with smallest separation does not have the smallest dm, figure out which candidate is the best match
        else:
            
            while min_sep_index != min_dm_index:

                # sort matches by increasing separation
                matches = matches.sort_values('target_sep').reset_index(drop=True)
                
                # if yes, then drop lowest separation
                matches = matches.drop( index=0 ).reset_index(drop=True)

                # update sep and dm index
                min_sep_index = matches['target_sep'].idxmin()
                min_dm_index  = matches['target_dm'].idxmin()
                
            # once min_sep_index == min_dm_index, select the target
            gaia_id = matches['gaia_id'].iloc[ min_sep_index ]
            index = matches['original_index'].iloc[ min_sep_index ]
            flag = '!'
            
            return gaia_id, index, flag

