import numpy as np
import pandas as pd

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord

from utils_skycoords import set_wds_skycoord

import warnings 
from erfa import ErfaWarning

# ignore erfa warnings
warnings.simplefilter('ignore', category=ErfaWarning)

# propagate positions for all primaries and secondaries in the wsi
def wsi_J2016_prop( wsi ):

    # lists to hold coords and flags
    pri_J2000 = []
    pri_J2016 = []
    sec_J2000 = []
    sec_J2016 = []
    # flags = []
    
    # J2016 time for astropy space motion method
    J2016 = Time(2016.0, format='jyear', scale='tcb')

    # loop through wsi, calculate J2000 & J2016 positions of pri and sec
    for i in range( len(wsi) ):

        # skycoord object for current index
        pri, sec = set_wds_skycoord( wsi, i )
        
        # propogate motion
        pri_prop = pri.apply_space_motion( J2016 )
        sec_prop = sec.apply_space_motion( J2016 )

        # add coordinates (in degrees) to results list
        pri_J2000.append( [pri.ra.degree, pri.dec.degree] )  
        pri_J2016.append( [pri_prop.ra.degree, pri_prop.dec.degree] )
        sec_J2000.append( [sec.ra.degree, sec.dec.degree] )
        sec_J2016.append( [sec_prop.ra.degree, sec_prop.dec.degree] )
        # flags.append( flag )

    # add results to wsi data frame
    # wsi['wds_ra1_J2000'] =  [x[0] for x in pri_J2000]
    # wsi['wds_dec1_J2000'] = [x[1] for x in pri_J2000]
    # wsi['wds_ra2_J2000'] =  [x[0] for x in sec_J2000]
    # wsi['wds_dec2_J2000'] = [x[1] for x in sec_J2000]
    wsi['wds_ra1']  = [x[0] for x in pri_J2016]
    wsi['wds_dec1'] = [x[1] for x in pri_J2016]
    wsi['wds_ra2']  = [x[0] for x in sec_J2016]
    wsi['wds_dec2'] = [x[1] for x in sec_J2016]
    # wsi['epoch_prop_flag'] = flags

    return wsi
