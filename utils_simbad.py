import re
import warnings
from astroquery.simbad import Simbad
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore', category=AstropyWarning)

#######################################################################################################################################

# given a wds id, look for a gaia match
def query_gaia_by_wds( wds_id ):

    # query simbad with wds id
    results = Simbad.query_objectids( wds_id )

    # astropy table to list of strings
    results_list = [ results[i][0] for i in range( len(results) ) ]
        
    # perform a regex search to find wds id in list of results
    regex_result = list( filter(lambda id: re.match('Gaia DR3', id), results_list) )
        
    return regex_result[0] # WILL FAIL if the list is empty, need to catch failure and flag in function

#######################################################################################################################################

# simple search for single letter component
def A_search(wds_id, A):
    try:
        A = query_gaia_by_wds( 'WDS J' + wds_id + A )
        flag = '.'
        return A, flag

    except:
        A = ''
        flag = '$'
        return A, flag

#######################################################################################################################################

# tries to direct match A component first, then searches for match using AB
# for when a complete component is of an AB format ("AB", "AC", "BC", etc.)
def AB_search(wds_id, AB):

    # split components
    A,B = wds_comp
    
    # try to find match for A
    try:
        pri = query_gaia_by_wds( 'WDS J' + wds_id + A )
        pri_flag = '.'
        return pri, pri_flag
        
    # if nothing is found, try AB
    except: 
        try:
            pri = query_gaia_by_wds( 'WDS J' + wds_id + AB )
            pri_flag = '!' # flag that first choice wasnt found
            return pri, pri_flag
            
        # if nothing is still found, flag it
        except:
            pri = ''
            pri_flag = '$'
            return pri, pri_flag        

#######################################################################################################################################

# opposite of AB search
# for when an individual component is of an AB format ( total comp is "AB,C", "A,BC", "AB,CD", etc.)
def AB_rev_search(wds_id, AB):
    A,B = AB
    
    try:
        AB = query_gaia_by_wds( 'WDS J' + wds_id + AB ) # try to find match for AB
        flag = '.'
        return AB, flag
        
    except: 
        try:
            A = query_gaia_by_wds( 'WDS J' + wds_id + A ) # if nothing is found, try A
            flag = '!' # flag that first choice wasnt found
            return A, flag 
            
        except:
            AB = '' # if nothing is still found, flag it
            flag = '$'
            return AB, flag
