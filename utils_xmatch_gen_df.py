import numpy as np
import pandas as pd
       
# Index(['target_oid', 'wds_id', 'wds_comp', 'wsi_sep', 'target_ra',
#        'target_dec', 'target_mag', 'designation', 'source_id', 'ra', 'dec',
#        'parallax', 'pmra', 'pmdec', 'pm', 'phot_g_mean_mag',
#        'phot_bp_mean_mag', 'phot_rp_mean_mag', 'has_xp_continuous', 'ruwe',
#        'phot_variable_flag', 'non_single_star', 'target_dm', 'target_sep'],
#       dtype='object')

# take indexes selected during cross match and build a dataframe of the results
# append empty entries when no match was found
# still working on slicker ways to do this with np.where

def generate_xmatch_df(gaia, indexes, flags):

    # lists for xmatch columns
    ids = []
    # gmag = []
    # bmag = []
    # rmag = []
    # ras = []
    # dcs = []
    # plx = []
    # pms = []
    # pmra = []
    # pmdec = []
    # xp = []
    # ruwe = []
    # var = []
    # nss = []

    # loop through indexes of matches that correspond to original crossmatch catalog
    for index in indexes:
    
        # try to locate match from original index in gaia dataframe
        try:
            match = gaia.iloc[ index ]
    
            # if a match is found, add the following data points
            ids.append( match['designation'] )
            # gmag.append( match['phot_g_mean_mag'] )
            # bmag.append( match['phot_bp_mean_mag'] )
            # rmag.append( match['phot_rp_mean_mag'] )
            # ras.append( match['ra'] )
            # dcs.append( match['dec'] )
    
            # # pm data may not be available, try to add
            # try:
            #     pms.append( match['pm'] )
            #     pmra.append( match['pmra'] )
            #     pmdec.append( match['pmdec'] )
            # except:
            #     pms.append( np.nan )
            #     pmra.append( np.nan )
            #     pmdec.append( np.nan )
            
        # if no match was found, the '$' flag will raise an indexing error
        # append an empty place holder
        except:
            ids.append( '' )
            # gmag 
            # bmag 
            # rmag 
            # ras 
            # dcs 
            # plx 
            # pms 
            # pmra 
            # pmdec
            # xp  
            # ruwe 
            # var 
    # datafrnss =ame of xmatches to return
    # add columns to wsi as needed
    xmatch = pd.DataFrame({
                        'designation':ids,
                        # 'gaia_mag':mag,
                        # 'gaia_pm':pms,
                        # 'gaia_ra':ras,
                        # 'gaia_dec':dcs,
                        # 'target_dm':dms,
                        # 'target_sep':sep,
                        # 'gaia_flag':flags
                            })
    
    return xmatch
