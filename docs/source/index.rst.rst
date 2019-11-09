.. FLICKER documentation master file, created by
   sphinx-quickstart on Sat Nov  3 16:17:18 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

FLICKER
====================================

*FLICKER* is a tool to calculate Flicker value of a lightcurve. 

Example usage
On single lightcurve from one observing quarter:
-------------

::
    import numpy as np
    import FLICKER as flc

    # Create a simple 100-day lightcurve with 15 day period
    time=np.linspace(0,100,1000) # time array [days]
    flux=np.sin(2*np.pi*time/15.)+np.random.rand(len(time)) # flux array

    # get flicker value
    flicker=flc.Flicker(time,flux)
    
    print(flicker)
    >> 0.1770736690463002

This function will return the median flicker value if input is multiple lightcurves from multiple observing quarters:

::

    # Create 10 lightcurves with observing time span
    time=[[] for i in range(10)] # empty list to put multiple lightcurves
    flux=[[] for i in range(10)] # empty list to put multiple lightcurves
    for i in range(10):
        t_sp=np.random.randint(10,200) # random timespan from 10-200 days
        time[i]=np.linspace(0,t_sp,1000) # time array [days]
        flux[i]=np.sin(2*np.pi*time[i]/15.)+np.random.rand(len(time[i])) # flux array

    # get flicker value
    flicker=flc.Flicker(time,flux)
    print(flicker)
    >> 0.2111953677723607

.. Contents:

User Guide
----------

.. toctree::
   :maxdepth: 2

   user/install
   user/tests
   user/api


Tutorials
---------

.. toctree::
   :maxdepth: 2

   tutorials/Tutorial


License & attribution
---------------------

Copyright 2019, Yuxi(Lucy) Lu.
