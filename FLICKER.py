import pandas as pd 
import numpy as np

def linearInt(x,y):
    """Linear interpolation between 2 points.

    Args:
      x: x values
      y: y values

    Returns:
      f: linear function returned that accepts x and return y
    """
    a=(y[1]-y[0])/(x[1]-x[0])
    b=y[0]-a*x[0]
    
    # function to return
    def f(x):
        return a*x+b
    return f


def SingleFlicker(time,flux,Time):
    """Calculate Flicker value for a single lightcurve.

    Args:
      time: time in unit of days
      flux: flux in unit of ppt
      Time: timescale to calculate flicker value, in unit of days

    Returns:
      flicker: flicker value
    """
    # squeeze into 1d array
    time=np.squeeze(time)
    flux=np.squeeze(flux)
    
    #print(np.shape(time))
    # interpolate between missing points
    flux_int=[]
    time_int=[]
        
    # calculate cadence and how many points to calcualte moving median
    timestep=np.median(np.diff(time)) # get the cadence
    points=int(round(Time/timestep)) # get how many points to do the moving median

    printn=0
    for i in range(len(flux)-1):
        intstep=round((time[i+1]-time[i])/timestep)
        if intstep>len(flux)*0.02 and printn==0: # if interpolating more than 5% of the data points...
            print('Warnings: Interpolating over 2\% of the total data!')
            printn=1
        if intstep!=1: # if time is missing
            f = linearInt([time[i],time[i+1]], [flux[i],flux[i+1]])
            intstep=int(intstep)-1
            for k in range(intstep):
                flux_int.append(f(time[i]+(k+1)*timestep))
                time_int.append(time[i]+(k+1)*timestep)
        else:
            flux_int.append(flux[i])
            time_int.append(time[i])
        
    # calculate moving median
    df=pd.Series(flux_int)
    medF=df.rolling(points).median()
        
    # put in pandas to get rid of N/A's
    medF=pd.DataFrame(np.array((flux_int,medF)).T,columns=['flux','median']).dropna()

    # calculate flicker
    flicker=np.sqrt(abs(np.mean((np.power(medF['flux'],2.)-np.power(medF['median'],2.)))))
    return flicker


def Flicker(time,flux,Time=8,Kp=0):
    """Calculate Flicker value for a lightcurve.
    
    Flicker() will return a single flicker value. Input can either be a 1d array/list or a list of
    multiple lists for the times and fluxes from differnt observing quarters. Flicker() will return 
    the median flicker value from all the quarters. 

    Args:
      time: time in unit of days
      flux: flux in unit of ppt
      Time: timescale to calculate flicker value, in unit of hours (optional)
      Kp: Kepler magnitude for correction (optional)

    Returns:
      flicker: flicker value
    """
    
    # figure out if input is a list of list or an array
    try:
        row,col=np.shape(flux)
        quart=min([row,col])
    except ValueError:
        if type(flux[0]) is list:
            quart=2
        else:
            quart=1
   
    ########################################## Sanity checks ##########################################
    # check dimension
    if quart>2:
        raise OverflowError('Input flux and time dimension must be 1 or 2!')
    ########################################## Sanity checks ##########################################
        
    # calculate correction if Kp!=0
    if Kp!=0:
        logF8_c=-0.03910-0.67187*Kp+0.06839*Kp**2.-0.001755*Kp**3.
    
    # convert hours to days
    Time=Time/24
    
    if quart==1: # if 1D
        flicker=SingleFlicker(time,flux,Time)
    else: # if 2d
        flicker_a=np.zeros(len(flux)) # flicker array

        for j in range(len(flux)):
            time_sing=time[j]
            flux_sing=flux[j]
        
            flicker_a[j]=SingleFlicker(time_sing,flux_sing,Time)
            flicker=np.median(flicker_a)
    
    # if no magnitude, return only flicker value, else return corrected flicker value as well
    if Kp==0:
        return flicker
    else:
        return flicker,np.sqrt((flicker)**2-(np.power(10.,logF8_c))**2)
