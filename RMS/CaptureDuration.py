from __future__ import print_function, absolute_import

import ephem
import datetime



def captureDuration(lat, lon, elevation):
    """ Calcualtes the start time and the duration of capturing, for the given geographical coordinates. 
    
    Arguments:
        lat: [float] latitude +N in degrees
        lon: [float] longitude +E in degrees
        elevation: [float] elevation above sea level in meters

    Return:
        (start_time, duration):
            - start_time: [datetime object] time when the capturing should start, True if capturing should
                start right away
            - duration: [float] seconds of capturing time
    """

    # Initialize the observer
    o = ephem.Observer()  
    o.lat = str(lat)
    o.long = str(lon)
    o.elevation = elevation

    # The Sun should be about 5.5 degrees below the horizon when the capture should begin/end
    o.horizon = '-5:26'

    # Calculate the locations of the Sun
    s = ephem.Sun()  
    s.compute()

    # Calculate the time of next sunrise and sunset
    next_rise = ephem.localtime(o.next_rising(s))
    next_set = ephem.localtime(o.next_setting(s))
    
    current_time = datetime.datetime.now()

    # If the nest sunset is later than the next sunrise, it means that it is night, and capturing should start immediately
    if next_set > next_rise:

        start_time=True

    # Otherwise, start capturing after the next sunset
    else:

        start_time = next_set
        

    # Calculate how long should the capture run
    if start_time == True:
        duration = next_rise - current_time

    else:
        duration = next_rise - next_set

    # Calculate the duration of capture in seconds
    duration = duration.total_seconds()

    return start_time, duration
    



if __name__ == "__main__":
    

    # Test
    print(captureDuration(43, -81, 265))
