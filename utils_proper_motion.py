import numpy as np
import pandas as pd

# function to calculate total proper motions in wsi catalog
def total_pm(ras, decs):
    
    # convert to lists
    ra_list = list( ras )
    dec_list = list( decs )
    
    # only proceed if lists are the same size
    if len(ra_list) == len(dec_list):

        # calculate total pm for each index in list
        total_pms = []
        for i in range( len(ra_list) ):
            
            # try to convert indexed items to float & calculate total pm
            try:
                ra = float( ra_list[i] )
                dec = float( dec_list[i] )

                # calculate total pm
                pm = np.sqrt( ra**2 + dec**2 )

                # append value to list
                total_pms.append( pm )

            # if it fails to convert to float, the target is missing pm data
            # flag it instead
            except:
                total_pms.append( np.nan )
                
        return total_pms
    
    else:
        print('inputs are different sizes/shapes')
