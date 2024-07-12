# usno-nreip-2024
Double star synthetic photometry. Backup of all my work for the internship at usno 2024.

# Methods
1. Clean up `wsi24` star catalog
	1. Filtering criteria for our sample:
	* remove all targets not using the stromgen y filter
	* remove targets with a dm of 0.0 or 7.5 (error in one of the pipelines)
	* may need to remove anything with a angular separation less than 0.8" (not an actual Gaia number, just a noticed trend from other papers). Look for a Ziegler 19-21 published paper as a possible reference for this number if needed.
	* may need to remove anything with the noisy flag: `dm_flag=:`
	* remove RA and Dec columns (this # not as accurate, remove so I don't accidentally use it)

	Column notes:
	1. dm flags:
	* `*`: dm calculated using standard photometry
	* `:`: noisy (can be removed on initial pass)
	* `q`: companion quadrant is known due to use of photometric calculation methods. could _potentially_ be useful for finding companions in gaia.
	* ` `: dm calculated using speckle method
		* what are the dm flags and their meaning? should we remove any of them?
		* nav and Avg meaning
		* separation value I should use to reduce catalog
	
	2. nav: total number of observations that were averaged
	3. avg: how many final observations averaged. ex: For 3 nights of observing with 4 observations per night: nav=12 and avg=3
	4. Comp: AB | A,BC | Aa,Ab

2. Filter `wds` catalog for just our targets
	* get list of unique targets from `wsi24` catalog
	* possibly a few missnamed ones. but all should match, i.e. should get the same amount of unique targets in each list after filtering
	* check and see which ones are missing BEFORE filtering and save them - give list to Rachel/Brian

3. Looking up coordinates in Gaia database and linking to a specific target.
	1. After the crossmatch, query Gaia for our target stars.

	2. What properties do we want to pull from gaia for each target?
		* color (b and r) -  see if color of star affects our measurements
		* proper motion
		* parallax
		* RUWE renormalized unit weight error - value on how good the astrometry is. If above 1.4 (avg=1) likely an unresolved binary.
		* Variability flag
		* nss (non single star) flag

4. Crossmatch
	1. Initial steps
	* Going to start with just the primaries - Done and used simbad to check where available. Tried several different algorithms
	* Minimum 75% matching the ID's - I have a 90-95% success rate when comparing to simbad results.

	2. Propogating positions for Gaia
	* Use astropy to calculate the position of the secondary, then propogate the motion forward to J2016. For secondaries with no proper motion, use the proper motion of the primary as a substitute and flag.
	* Figuring out a way to not repeat searches would be nice. Say for a given system we have AB, and BC measurements. We don't need to spend time calculating the offset of B in the AB observation, because the BC observation will already have the precise coordinate.
