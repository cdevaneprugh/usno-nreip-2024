import pandas as pd

# take indexes selected during cross match and build a dataframe of the results
# append empty entries when no match was found
# still working on slicker ways to do this with np.where

def generate_xmatch_df(gaia, indexes, flags):

    # lists for xmatch columns
    ids = []
    mag = []
    dms = []
    sep = []
    pms = []

    # loop through indexes of matches that correspond to original crossmatch catalog
    for index in indexes:
    
        # try to locate match from original index in gaia dataframe
        try:
            match = gaia.iloc[ index ]
    
            # if a match is found, add the following data points
            ids.append( match['gaia_id'] )
            mag.append( match['gaia_mag'] )
            dms.append( match['target_dm'] )
            sep.append( match['target_sep'] )
    
            # pm data may not be available, try to add
            try:
                pms.append( match['gaia_pm'] )
            except:
                pms.append( '' )
            
        # if no match was found, the '$' flag will raise an indexing error
        # append an empty place holder
        except:
            ids.append( '' )
            mag.append( '' )
            dms.append( '' )
            sep.append( '' )
            pms.append( '' )

    # dataframe of xmatches to return
    # add columns to wsi as needed
    xmatch = pd.DataFrame({
                        'gaia_id':ids,
                        'gaia_mag':mag,
                        'gaia_pm':pms,
                        'target_dm':dms,
                        'target_sep':sep,
                        'gaia_flag':flags})
    
    return xmatch
