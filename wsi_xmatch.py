import warnings
import numpy as np
import pandas as pd
from utils_xmatch import wsi_gaia_xmatch
warnings.simplefilter(action='ignore', category=FutureWarning)

# load in data
wsi = pd.read_csv('data/wsi24.prepped.csv')
gaia_pri = pd.read_csv('data/gaia.results/pri.04mag.05as-result.csv')
gaia_sec = pd.read_csv('data/gaia.results/sec.04mag.10as-result.csv')

# crossmatch
xmatch = wsi_gaia_xmatch( wsi, gaia_pri, gaia_sec )

# see where our answers match simbad
xmatch['xm_chk1'] = np.where( xmatch.gaia_designation1 == xmatch.sb_id1, True, False )
xmatch['xm_chk2'] = np.where( xmatch.gaia_designation2 == xmatch.sb_id2, True, False )

# save results
xmatch.to_csv('data/wsi24.xmatch.csv', index=False)
