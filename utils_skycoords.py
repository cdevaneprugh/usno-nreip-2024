import math
import numpy as np
import pandas as pd

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord

import warnings                                                         
from erfa import ErfaWarning

# ignore erfa warnings
warnings.simplefilter('ignore', category=ErfaWarning)

###################################################################################################################################################

# takes the wsi (as a pandas df) and the index you want to turn into a skycord
def set_wds_skycoord(df, i):
    
    # flag to indicate secondary propagation PM source
    # no flag means secondary has its own pm data
    # flag = '.'

    # define primary star values
    primary_coords = df.wds_coord1.iloc[i] 
    primary_pm_ra =  df.wds_pm1_ra.iloc[i]  * u.mas/u.yr
    primary_pm_dec = df.wds_pm1_dec.iloc[i] * u.mas/u.yr
    J2000 = Time( 2000.0, format='jyear', scale='tcb' ) # shared with secondary


    # establish skycoord for primary
    primary = SkyCoord(
                        primary_coords, unit=(u.hourangle, u.degree),
                        pm_ra_cosdec = primary_pm_ra,
                        pm_dec = primary_pm_dec,
                        obstime = J2000 
    )
    
    # calculate directional offset of secondary
    position_angle =   df.wsi_pa.iloc[i]  * u.degree
    separation_angle = df.wsi_sep.iloc[i] * u.arcsec
    secondary_coords = primary.directional_offset_by( position_angle, separation_angle )
    
    # try establish skycord for secondary with proper motion
    # secondary pm will be read in as string due to flags in column
    # force pm into float or else it will always fail
    try:
    
        # define secondary star values
        secondary_pm_ra  = float( df.wds_pm2_ra.iloc[i] )  * u.mas/u.yr
        secondary_pm_dec = float( df.wds_pm2_dec.iloc[i] ) * u.mas/u.yr
        
        secondary = SkyCoord(
                             secondary_coords,
                             pm_ra_cosdec = secondary_pm_ra,
                             pm_dec = secondary_pm_dec,
                             obstime = J2000
        )
    
    # if pm data is missing for secondary, use proper motion data of primary
    # when we advance time, this will effectively be the same as propogating the primary THEN calculating the offset of secondary
    except:
        secondary = SkyCoord(
                            secondary_coords,
                            pm_ra_cosdec = primary_pm_ra,
                            pm_dec = primary_pm_dec,
                            obstime = J2000
        )
        
        # set flag if we use primary's pm
        # flag = '!'
    
    return primary, secondary#, flag
