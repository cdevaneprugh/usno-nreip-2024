"""
converts the text files for the wds (with secondary precise coordinates) into a csv file
"""

from astropy.io import ascii

# convert the wds summary to csv
file = 'data/wds.summ'

wds = ascii.read(file, format="fixed_width_no_header", delimiter=' ',
                         col_starts=(0, 10, 17, 23, 28, 33, 38, 42, 46, 52, 58, 64, 70, 80, 84, 89, 93, 98, 107, 112),
                         col_ends = (9, 16, 21, 26, 31, 36, 40, 44, 50, 56, 62, 68, 78, 83, 87, 92, 96, 105,110, 134),
                         names=('wds_id','wds_dd','wds_comp',
                                'wds_date_first','wds_date_last','wds_num_obs',
                                'wds_pa_first','wds_pa_last',
                                'wds_sep_first','wds_sep_last',
                                'wds_mag1','wds_mag2','wds_spt',
                                'wds_pm1_ra','wds_pm1_dec',
                                'wds_pm2_ra','wds_pm2_dec',
                                'wds_durch_num','wds_notes',
                                'wds_coord'))

# write new csv
#wds.write('data/wds.summ.csv', format='csv', overwrite=True)
