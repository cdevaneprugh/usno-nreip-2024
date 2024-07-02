import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import and clean up csvs
wds = pd.read_csv('data/wds.summ.csv').replace({'wds_comp':np.NaN},'AB')
xmatch = pd.read_csv('data/xmatch_old/crossmatch_gaiadr3_wds_nov_15_2023.txt')
wds = wds.loc[wds.wds_mag1 != '.']

wds = wds.iloc[:1000]

# fold xmatch gaia ids into reduced wds
wds_targs = list(wds.wds_id)
wds_mags = list(wds.wds_mag1)

gaia_ids = []
gaia_mags = []
missing_targets = 0

for i, target in enumerate(wds_targs):

    # find gaia id based on target name and magnitude of primary
    id = xmatch.loc[ (xmatch['wds_wds'] == target) & (xmatch['wds_mag1'] == float(wds_mags[i])) ]
    
    try:
        gaia_ids.append(id.gaia_source_id.iloc[0]) # could be multiple observations of primary, only add one id
        gaia_mags.append(id.gaia_gmag.iloc[0]) # add primary mag too for comparison to wds mag
    except:
        gaia_ids.append('') # if we have an observation that was not crossmatched, add empty space
        gaia_mags.append('')
        missing_targets += 1

# add gaia ids to wds dataframe
wds['gaia_id_0']=gaia_ids
wds['gaia_mag_0']=gaia_mags


print(len(wds), missing_targets) # how many missing targets?

# get an idea of how different the wds mags are from the gaia mags we just added

# wds and gaia mags to list
wds_mags = list(wds.wds_mag1)

# take difference of each entry, use a try/except to skip blank entries in gaia mags
diff = []
diff_full_list = []

for i in range( len(wds) ):
    try:
        result = float(wds_mags[i]) - gaia_mags[i]
        diff.append(result)
        diff_full_list.append(result)
        
    except:
        diff_full_list.append('')

wds['wds_gaia_dm'] = diff_full_list # append the full results to the dataframe

plt.hist(diff, bins=12)
plt.yscale('log')
plt.title('histogram of wds-gaia mags')
plt.ylabel('number (log scaled)')
plt.xlabel('magnitude difference')
plt.show()
