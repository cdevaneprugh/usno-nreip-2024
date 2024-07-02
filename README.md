# usno-nreip-2024
Double star synthetic photometry. Backup of all my work for the internship at usno 2024.

# Methods
1. Clean up `wsi24` star catalog
	1. Filtering criteria:
	* remove all targets not using the stromgen y filter
	* remove targets with a dm of 0.0 or 7.5 (error in one of the pipelines)
	* remove anything with a angular separation less than 0.8" (not an actual Gaia number, just a noticed trend from other papers). Look for a Ziegler 19-21 published paper as a possible reference for this number if needed.
	* remove anything with the noisy flag: `dm_flag=:` (for now, add back in later)
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
	4. Comp: AB | A,BC | AaAb

2. Filter `wds` catalog for just our targets
	* get list of unique targets from `wsi24` catalog
	* possibly a few missnamed ones. but all should match, i.e. should get the same amount of unique targets in each list after filtering
	* check and see which ones are missing BEFORE filtering and save them - give list to Rachel/Brian

3. Looking up coordinates in Gaia database and linking to a specific target.
	1. data link vs gaia data query on their website?
		* pregenerated spectra should be available in tables, datalink is possibly just for generating our own spectra.
	
	2. What properties do we want to pull from gaia for each target?
		* color (b and r) -  see if color of star affects our measurements
		* proper motion
		* parallax
		* RUWE renormalized unit weight error - value on how good the astrometry is. If above 1.4 (avg=1) likely an unresolved binary.
		* Variability flag
		* nss (non single star) flag

4. Crossmatches
	1. Plan & Ideas
	* Going to start with just the primaries
	* look at gaia data link to see if querying is easier/different
	* Minimum 75% matching the ID's
	* Need to read through the other intern's work and brainstorm some ideas.
	* this is going to be tricky. best to start with some VERY simple cases and add complexity
	* could potentially start with `SIMBAD`. Query WDS targets with `WDS J"WDSID"`
	* look at the primary matched catalog as a reference, then recreate what the intern worked on

	2. There are a few ways to propogate our positions and match to Gaia.
	* One way is to use astropy to propogate the primary star, then calculate the offset of the secondary. With these coordinates, query using Gaia.
	* Another option is to use astropy to calculate the offset of the secondary before propogating the primary. Then use gaia to propogate the positions of the primary and secondary (for the stars that have proper motions). We could also use astropy again to propogate forward.
	* A key piece of information is finding out what percentage of our targets have proper motion data for the secondaries.
	* I also need to know which secondaries have magnitude measurements.
	* The ideal set has magnitude and proper motion data for both stars. I'll need to have a line that gives an exception when nothing is found so we don't get nans screwing everything up.
	* Figuring out a way to not repeat searches would be nice. Say for a given system we have AB, and BC measurements. We don't need to spend time calculating the offset of B in the AB observation, because the BC observation will already have the precise coordinate.
	* The Gaia ADQL method will take some experimentation to get working. I think I can add other tables in with proper motion and magnitude data where available.
	What would be ideal to set up is for it to try and propogate the motion forward, then adjust the search radius dynamically, and default to a wider search radius of the original coordinate if no proper motion data is available.
