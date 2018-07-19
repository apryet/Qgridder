# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgridder_time_utils
                        Part of Qgridder - A QGIS plugin
 Builds 2D grids for finite difference
                              -------------------
        begin                : 2013-04-08
        copyright            : (C) 2013 by Pryet
        email                : alexandre.pryet@ensegid.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import numpy as np
import datetime as dt

try : 
    import matplotlib.dates as mdates
except : 
    print('Could not load matplotlib.dates module')


# ---------------------------------------------------------------
def gen_time_seq(date_start_string, tstep, n_tstep, date_string_format = '%Y-%m-%d %H:%M' ) :
    """
    Description.

    Parameters
    ----------
    date_start_string : date from which to start the sequence in string format
                        '%Y-%m-%d %H:%M', e.g. '2015-03-02 12:00'.
    tstep : length of time step in seconds.
    n_tstep : number of time steps
    date_string_format : date string format used in input file, 
                         see https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    
    Returns
    -------

    dates_out : list of datetime objects

    Examples
    --------
    # generate a sequence of 20 datetimes instances starting from 2015-03-02 12:00 at 1-minute-interval. 
    >>> dates_out = gen_time_seq(date_start_string = '2015-03-02 12:00' ,tstep = 60 ,n_tstep = 20)

    """
    # convert date_start_string to datetime format
    date_start = dt.datetime.strptime(date_start_string, date_string_format)
    # estimate date_end in datetime format
    date_end = date_start + dt.timedelta(seconds = tstep*n_tstep)
    # generate sequence of dates
    datenums_out = mdates.drange(date_start,date_end - dt.timedelta(seconds=0.001), dt.timedelta(seconds=tstep))
    # convert to list of datetime 
    dates_out = mdates.num2date(datenums_out)

    return(dates_out)

# ---------------------------------------------------------------
def lin_time_interp(dates_in, vals_in, dates_out) : 
    """
    Perform linear interpolation from an input time series so as to provide
    output values at required times. If output times are found before / after
    first / last time of input time series, then first / last value are returned.

    Parameters
    ----------
    dates_in : Pandas DataFrame object with a date index and a 'val' column
    vals_in : dates for which to provide interpolated values.
    
    Returns
    -------
    vals_out : a numpy array with interpolates values at t_out

    Examples
    --------
    >>> vals_out = lin_time_interp(dates_in, vals_in, dates_out)

    """

    # eval number of time steps to interpolate
    n_tstep = len(dates_out)

    # convert dates to datenums
    datenums_in = mdates.date2num(dates_in)
    datenums_out = mdates.date2num(dates_out)
        
    # array of indexes corresponding with closest timestamp after "observed" value 
    idx_after = np.searchsorted(datenums_in, datenums_out)

    # look for dates outside time span of input values
    is_outside = np.zeros( (n_tstep,)) # default value, for dates within time span of input values
    is_outside[ idx_after == 0 ] = -1 # value for dates before first input value
    is_outside[ idx_after == n_tstep ] = 1 # value for dates after last input value
    idx_after[ idx_after == 0 ] = 1 # correct idx_after to avoid index value out of bound 
    idx_after[ idx_after == len(datenums_in) ] = len(datenums_in) - 1 # correct idx_after to avoid index value out of bound


    # timestamp before/after resample
    times_before = datenums_in[idx_after - 1]
    times_after = datenums_in[idx_after]
    # values before/after resample
    vals_before = vals_in[idx_after - 1]
    vals_after = vals_in[idx_after]


    #calculate new weighted value
    span = times_after - times_before   
    weight_before = (times_after - datenums_out) / span
    weight_after = (datenums_out - times_before ) / span
    vals_out = weight_before * vals_before + weight_after * vals_after 


    # set values outside to first / last value
    vals_out[ is_outside == -1 ] = vals_in[0]
    vals_out[ is_outside == 1 ] = vals_in[-1]

    return(vals_out)



# ---------------------------------------------------------------
def interp_from_file(in_file_path, dates_out, date_string_format =  '%Y-%m-%d %H:%M',
        csv_delimiter =',' , skip_header = 1, quotechar='\"'
          ) : 
    """
    Performs linear interpolation from an input csv file with lin_time_interp

    Parameters
    ----------
    in_file_path : input csv file following format 
                TIMESTAMP,val
                2012-01-01 12:00,0.0
                2012-02-01 13:00,0.0

                A header line must be present, but column names may be chosen freely.
                The first column should be the date in string format.
                The second column should 

    dates_out : list of datetime objects, as generated by gen_time_seq(...).

    date_string_format : date string format used in input file, 
                         see https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior

    csv_delimiter, skip_header, quotechar : parameters for numpy.genfromtxt(...)
    
    Returns
    -------

    vals_out : a numpy array with interpolated values at t_out

    Examples
    --------
    >>> dates_out = gen_time_seq(date_start_string = '2015-03-02 12:00' ,tstep = 60 ,n_tstep = 120)
    >>> vals_out = interp_from_file('./data_in.dat', dates_out  )

    """

    # read observed data

    try :
        datenums_in, vals_in = np.genfromtxt(in_file_path,delimiter=csv_delimiter, 
                unpack=True,skip_header=skip_header,
                converters={ 0: mdates.strpdate2num(date_string_format)}
                )

    except :
        print('Error while reading file ' + in_file_path + '.\n'+
                'Check file path and format (should be a 2 column CSV file).'
                )
        return(None)

    # convert datesnums to datetime
    dates_in = mdates.num2date(datenums_in)

    # compute vals_out 
    vals_out = lin_time_interp(dates_in, vals_in, dates_out)

    return( vals_out ) 


