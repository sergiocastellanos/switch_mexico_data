"""
Code to automatically generate inputs for switch.

Developers:
    Pedro Andres Sanchez Perez
    Sergio Castellanos Rodriguez
    And other I do not know.
"""
import os
import sys
import yaml
import numpy as np
import pandas as pd
from collections import OrderedDict

data_path  = '../data/clean/loads/'
output_path  = '../data/clean/switch_inputs/'

def get_load_data(path=data_path, filename='HighLoads.csv',
        corrections=True, total=False, *args, **kwargs):
    """
        Load consumption data
        TODO:
            * This could be a csv or it could connect to a DB.
    """
    print (os.path.join(path, filename))
    try:
        df = pd.read_csv(os.path.join(path, filename))
    except FileNotFoundError:
        raise ('File not found. Please verify the file is in: {}'.format(os.path.join(path, filename)))
    # Calculate the sum of loads
    df['total'] = df.sum(axis=1)
    # Convert to datetime if does not exist
    last_year = df['year'].iloc[-1:].values
    if corrections:
        try:
            df.loc[df['hour'] == 24, 'hour'] = 0
            df.loc[df['hour'] == 0, 'hour'] +=  1
            # Fix below code to represent a year regression
            df.loc[df['year'] > last_year] -= pd.DateOffset(day=365)
        except ValueError as e:
            # TODO: Check why this function breaks
            #raise ('24 Hour timestamp  not found in Load data. Try another hour')
            pass
    df.index = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

    if total:
        df = df[['total']].sort_index()
    df = df.sort_index()
    # TODO: Fix to return only total load
    return (df)

def get_peak_day(data, number=4, freq='MS'):
    """ Construc a representative day based on a single timestamp

    Args:
        data (pd.DataFrame): data to filter,
        number (float): number of days to return.

    Note: Month start is to avoid getting more timepoints in a even division
    """
    years = []
    if number & 1:
        raise ValueError('Odd number of timepoints. Use even number')
    for index, group in data.groupby([pd.Grouper(freq='A'),\
        pd.Grouper(freq=freq)]):
        # Get index of max value
        peak_timestamp = group.idxmax()
        # Convert the max value index to timestamp
        mask = peak_timestamp.strftime('%Y-%m-%d')
        # Get the number of points inside the max timestamp
        years.append(group.loc[mask].iloc[::int((24/number))].reset_index())

    output_data = pd.concat(years)
    output_data = output_data.rename(columns={'index':'date',
                                    'total':'peak_day'})
    return (output_data)

def get_median_day(data, number=4, freq='MS'):
    """ Calculate median day giving a timeseries

    Args:
        data (pd.DataFrame): data to filter,
        number (float): number of days to return.

    Note: Month start is to avoid getting more timepoints in a even division

    """
    years = []
    for index, group in data.groupby([pd.Grouper(freq='A'),\
        pd.Grouper(freq=freq)]):
        # Calculate the daily mean
        grouper = group.groupby(pd.Grouper(freq='D')).mean()
        if len(grouper) & 1:
            # Odd number of days
            index_median = grouper.loc[grouper==grouper.median()].index[0]
        else:
            # Even number of days
            index_median = (np.abs(grouper-grouper.median())).idxmin()
        years.append(group.loc[index_median.strftime('%Y-%m-%d')].iloc[::int((24/number))].reset_index())
    output_data = pd.concat(years)
    output_data.rename(columns={'index':'date', 'total':'median_day'},\
            inplace=True)

    return (output_data)

def create_investment_period(data, ext='.tab'):
    """
        Create periods file
    """
    output_file = output_path + 'periods' + ext

    # TODO: Migrate this to a function in utilities

    with open("periods.yaml", "r") as stream:
        try:
            periods = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise (exc)

    d = OrderedDict(periods)
    periods_tab = pd.DataFrame(d)
    periods_tab = periods_tab.set_index('INVESTMENT_PERIOD')
    periods_tab.to_csv(output_file, sep='\t')


def create_timepoints(data, ext='.tab'):
    """
        Create timepoints file
    """

    # Filename convention
    if ext == '.tab': sep='\t'
    output_file = output_path + 'timepoints' + ext

    # If multiple timeseries included in data
    if isinstance(data, list):
        data = pd.concat(data)

    # TODO: Write test to check if columns exist
    data = data[['timestamp', 'TIMESERIES', 'daysinmonth']]
    data.index.name = 'timepoint_id'
    data = data.reset_index(drop=True)
    data = data.rename(columns={'TIMESERIES':'timeseries'})
    data.index += 1  # To start on 1 instead of 0
    data.index.name = 'timepoint_id'
    output_cols = ['timestamp', 'timeseries']
    data[output_cols].to_csv(output_file, sep=sep)


def create_strings(data, scale_to_period, identifier='P',  ext='.tab'):
    """
        Create timestamp file

    """
    strftime = '%Y%M%d%H' #  Strftime for label
    data['timestamp'] = data['date'].dt.strftime(strftime)
    data['TIMESERIES'] = data['date'].dt.strftime('%Y_%m{}'.format(identifier))
    data['daysinmonth'] = data['date'].dt.daysinmonth

    # TODO: Fix this. Probably bug in near future
    data['ts_period'] = data['date'].dt.year
    data['scale_to_period'] = scale_to_period

    return (data)

def create_timeseries(data, number=4, ext='.tab'):
    """
        Create timeseries file
    """

    # Filename convention
    output_file = output_path + 'timeseries' + ext
    if ext == '.tab': sep='\t'

    # If multiple timeseries included in data
    if isinstance(data, list):
        data = pd.concat(data)

    size = len(data) #  Size to divide the timeseries in a timeperiod

    # Extract unique timeseries_id
    timeseries = data[['TIMESERIES', 'daysinmonth', 'ts_period',
        'scale_to_period']].drop_duplicates('TIMESERIES')
    timeseries = timeseries.reset_index(drop=True)

    timeseries['ts_duration_of_tp'] = 24/number
    timeseries['count'] = timeseries.groupby('ts_period')['TIMESERIES'].transform(len)
    timeseries['ts_num_tps'] = data[['timestamp', 'TIMESERIES']].groupby('TIMESERIES').count().values
    # TODO: Change value of 24 for number of days to represent and 365 for
    # the total amount of years?
    scaling = timeseries['scale_to_period']*24*(365/timeseries['count'])/(timeseries['ts_duration_of_tp']*timeseries['ts_num_tps'])
    timeseries['ts_scale_to_period'] = scaling
    #  timeseries.index += 1  # To start on 1 instead of 0
    timeseries.index.name = 'timepoint_id'

    # Delete unused columns
    del timeseries['daysinmonth']
    del timeseries['scale_to_period']
    del timeseries['count']

    timeseries.to_csv(output_file, index=False, sep=sep)

def create_variablecp(data, timeseries_dict, ext='.tab'):
    """
        Create variable capacity factor file
    """
    # Filename convention
    output_file = output_path + 'variable_capacity_factors' + ext
    if ext == '.tab': sep='\t'

    # If multiple timeseries included in data
    if isinstance(data, list):
        data = pd.concat(data)

    # Check if file exist and removeit
    if os.path.exists(output_file):
        os.remove(output_file)

    periods = set(data.date.dt.year)
    output_file = output_path + 'variable_capacity_factors' + ext
    data_path = '../data/clean/SWITCH/'
    ren_cap_data = pd.read_csv(data_path + 'ren-all2.csv', index_col=0,
                               parse_dates=True)

    # Extract datetime without year information
    filter_dates = pd.DatetimeIndex(data['date'].reset_index(drop=True)).strftime('%m-%d %H:%M:%S')
    #  filter_dates = pd.DatetimeIndex(data['date'].reset_index(drop=True))
    df = pd.DataFrame([])
    ren_tmp = ren_cap_data.copy()
    #ren_tmp.index = ren_tmp.index + pd.DateOffset(years=2)

    # DEPRECATED FOR CYCLE.
    # This function will dissapear in the nex version.
    #for year in periods:
    #    df = df.append(ren_tmp)
    #    ren_tmp.index = ren_tmp.index + pd.DateOffset(years=1)
    
    list1 = []
    for row, value in timeseries_dict.items():
        print (row)
        tmp2 = pd.concat(value)
        filter_dates = pd.DatetimeIndex(tmp2['date'].reset_index(drop=True)).strftime('%m-%d %H:%M:%S')
        grouped = (ren_tmp[ren_tmp['time'].isin(filter_dates)]
                    .reset_index(drop=True)
                    .groupby('GENERATION_PROJECT', as_index=False))
        list1.append(pd.concat([group.reset_index(drop=True) for name, group in grouped]))
    variable_cap = pd.concat(list1)
    variable_tab = variable_cap.groupby('GENERATION_PROJECT')
    for keys in variable_tab.groups.keys():
        data = variable_tab.get_group(keys).reset_index(drop=True)
        data.index +=1
        data.index.name = 'timepoint'
        data.rename(columns={'capacity_factor': 'gen_max_capacity_factor'},
                   inplace=True)
        data.reset_index()[['GENERATION_PROJECT', 'timepoint',
            'gen_max_capacity_factor']].to_csv(output_file, sep=sep,
                    index=False, mode='a', header=(not
                        os.path.exists(output_file)))

def create_loads(load, data, ext='.tab'):
    """
        Create loads file
    """
    # Filename convention
    output_file = output_path + 'loads' + ext
    if ext == '.tab': sep='\t'

    # If multiple timeseries included in data
    if isinstance(data, list):
        data = pd.concat(data)

    loads_tmp = load.copy() #[load.year <= 2025]
    list_tmp = []

    # Get data from the datetime provided
    tmp = (loads_tmp.loc[data['date']]
            .drop(['year', 'month','day','hour', 'total'], axis=1)
            .reset_index()
            .drop_duplicates('index')
            .reset_index(drop=True))

    # TODO: Check why this column is created
    del tmp['index']

    tmp = tmp.unstack(0)
    for name, group in tmp.groupby(level=0):
        list_tmp.append(group.reset_index())
    loads_tab = pd.concat(list_tmp)
    loads_tab.index += 1
    loads_tab = loads_tab.rename(columns={'level_0':'LOAD_ZONE', 0:'zone_demand_mw'})
    # TODO: Check why this is necesary
    del loads_tab['level_1']
    loads_tab.index.name = 'TIMEPOINT'
    loads_tab = loads_tab.reset_index()[['LOAD_ZONE', 'TIMEPOINT', 'zone_demand_mw']]
    loads_tab.to_csv(output_file, sep=sep, index=False)

def create_gen_build_cost(data, ext='.tab', **kwargs):
    if ext == '.tab': sep='\t'
    output_file = output_path + 'gen_build_costs' + ext
    # TODO: 
    # * Change the direction of this file
    with open("periods.yaml", "r") as stream:
        try:
            periods = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise (exc)
    asd = []
    for period in periods['INVESTMENT_PERIOD']:
        costs = pd.read_csv('gen_build_costs.tab', sep=sep)
        costs['build_year'] = period
        asd.append(costs)
    gen_build_costs = pd.concat(asd)
    gen_build_costs.to_csv(output_file, sep=sep, index=False)


def create_inputs(**kwargs):
    """
        Create all inputs
    """
    load_data = get_load_data()

    with open("periods.yaml", "r") as stream:
        try:
            periods = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise (exc)

    d = OrderedDict(periods)
    periods_tab = pd.DataFrame(d)
    periods_tab = periods_tab.set_index('INVESTMENT_PERIOD')

    # Create timeseries selction. This will extract peak and median day

    timeseries = []
    timeseries_dict = {}
    for periods, row in periods_tab.iterrows():
        timeseries_dict[periods] = []
        scale_to_period = row[1] - row[0]
        peak_data = get_peak_day(load_data[str(periods)]['total'], freq='1MS', **kwargs)
        median_data = get_median_day(load_data[str(periods)]['total'], freq='1MS', **kwargs)
        timeseries_dict[periods].append(create_strings(peak_data, scale_to_period))
        timeseries_dict[periods].append(create_strings(median_data, scale_to_period,
                                        identifier='M'))
        timeseries.append(create_strings(peak_data, scale_to_period))
        timeseries.append(create_strings(median_data, scale_to_period,
                                        identifier='M'))
    print (len(timeseries_dict[2030]))
    create_investment_period(peak_data)
    create_gen_build_cost(peak_data)
    create_timeseries(timeseries, **kwargs)
    create_timepoints(timeseries)
    create_variablecp(timeseries, timeseries_dict)
    create_loads(load_data, timeseries)


if __name__ == '__main__':
    create_inputs(number=4)

