import numpy as np
import pandas as pd

from utils_xmatch import wsi_gaia_xmatch

# read in wsi
wsi = pd.read_csv('data/wsi.prop.csv')

# filter wsi
sample = wsi.loc[ (wsi.wds_mag1 > 3) & (wsi.wsi_sep > 0.8) ].reset_index(drop=True)

# export sample
sample.to_csv('data/wsi.query_sample.csv', index=True, index_label='wsi_oid')

