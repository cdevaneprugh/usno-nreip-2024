import numpy as np
import pandas as pd

######################################################################################################################################################

# reduce targets in slave catalog, based off of unique targets in a master catalog
def reduce_targets(slave_catalog, master_catalog):
    
    # get list of unique targets in master catalog
    master_target_list = list( np.unique( master_catalog['wds_id'] ) )

    # reduce slave catalog based on list of targets
    slave_catalog = slave_catalog.loc[ slave_catalog['wds_id'].isin(master_target_list) ].reset_index(drop=True)

    return slave_catalog # return the reduced catalog

######################################################################################################################################################

# check that two lists of unique targets are identical
def compare_targets(catalog_1, catalog_2):

    # get lists of unique targets from each catalog
    cat_1_uniq = list( np.unique( catalog_1['wds_id']) )
    cat_2_uniq = list( np.unique( catalog_2['wds_id']) )

    # are lists the same targets and length?
    status = cat_1_uniq == cat_2_uniq

    len_1 = len( cat_1_uniq )

    return status, len_1

######################################################################################################################################################

# check unique entries in a dataframe, return counts
def show_unique_items( input_list ):

    # get unique items and counts
    uniq_items = np.unique( input_list, return_counts=True )
   
    # print the unique item, and the number of occurences 
    for i in range( len( uniq_items[0] ) ):
        print( uniq_items[0][i], ':', uniq_items[1][i] )

