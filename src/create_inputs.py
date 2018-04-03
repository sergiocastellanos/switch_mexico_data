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
import pdb
import numpy as np
import pandas as pd
from collections import OrderedDict

script_path = os.path.dirname(__file__)
parent_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(parent_path, 'data/clean/loads')
output_path  = os.path.join(parent_path, 'data/clean/switch_inputs/')

def get_load_data(path=data_path, filename='HighLoads.csv',
        corrections=True, total=False, *args, **kwargs):
    """
        Load consumption data
        TODO:
            * This could be a csv or it could connect to a DB.
    """
    print (os.path.join(path, filename))
    file_path = os.path.join(path, filename)
    try:
        df = pd.read_csv(file_path)
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
            print (e)
            # TODO: Check why this function breaks
            #raise ('24 Hour timestamp  not found in Load data. Try another hour')
            pass
    df.index = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

    if total:
        df = df[['total']].sort_index()
    df = df.sort_index()
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
    for _, group in data.groupby([pd.Grouper(freq='A'),\
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
    for _, group in data.groupby([pd.Grouper(freq='A'),\
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

def create_investment_period(data, path=script_path, ext='.tab', **kwargs):
    """
        Create periods file
    """
    output_file = output_path + 'periods' + ext

    # TODO: Migrate this to a function in utilities
    file_path = os.path.join(path, 'periods.yaml')
    with open(file_path, "r") as stream:
        try:
            periods = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise (exc)

    d = OrderedDict(periods)
    periods_tab = pd.DataFrame(d)
    periods_tab = periods_tab.set_index('INVESTMENT_PERIOD')
    periods_tab.to_csv(output_file, sep='\t')


def create_timepoints(data, ext='.tab', **kwargs):
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


def create_strings(data, scale_to_period, identifier='P',  ext='.tab', **kwargs):
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

def create_timeseries(data, number=4, ext='.tab', **kwargs):
    """
        Create timeseries file
    """

    # Filename convention
    output_file = output_path + 'timeseries' + ext
    if ext == '.tab': sep='\t'

    # If multiple timeseries included in data
    if isinstance(data, list):
        data = pd.concat(data)


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

def create_variablecp(data, timeseries_dict, path=parent_path, ext='.tab', **kwargs):
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

    output_file = output_path + 'variable_capacity_factors' + ext
    file_path = os.path.join(path, 'data/clean/SWITCH/')
    filename = 'ren-all2.csv'
    ren_cap_data = pd.read_csv(os.path.join(file_path, filename), index_col=0,
                               parse_dates=True)
    # Quick fix to names
    replaces = ['é', 'á', 'í', 'ó', 'ú', 'ñ']
    print (ren_cap_data.head())

    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('é', 'e')
    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('á', 'a')
    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('í', 'i')
    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('ó', 'o')
    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('ú', 'u')
    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('ñ', 'n')
    # Extract datetime without year information
    filter_dates = pd.DatetimeIndex(data['date'].reset_index(drop=True)).strftime('%m-%d %H:%M:%S')
    #  filter_dates = pd.DatetimeIndex(data['date'].reset_index(drop=True))
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

def create_loads(load, data, ext='.tab', **kwargs):
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
    for _, group in tmp.groupby(level=0):
        list_tmp.append(group.reset_index())
    loads_tab = pd.concat(list_tmp)
    loads_tab.index += 1
    loads_tab = loads_tab.rename(columns={'level_0':'LOAD_ZONE', 0:'zone_demand_mw'})
    # TODO: Check why this is necesary
    del loads_tab['level_1']
    loads_tab.index.name = 'TIMEPOINT'
    loads_tab = loads_tab.reset_index()[['LOAD_ZONE', 'TIMEPOINT', 'zone_demand_mw']]
    loads_tab.to_csv(output_file, sep=sep, index=False)

def create_gen_build_cost(data, ext='.tab', path=script_path,
    **kwargs):
    if ext == '.tab': sep='\t'
    output_file = output_path + 'gen_build_costs' + ext
    # TODO: 
    # * Change the direction of this file
    file_path = os.path.join(path, 'periods.yaml')
    with open(file_path, "r") as stream:        
        try:
            periods = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise (exc)
    asd = []
    gen_project = pd.read_csv('src/generation_projects_info.tab', sep='\t')
    gen_predeterimend = pd.read_csv('./src/gen_build_predetermined.tab', sep='\t')
    gen_predeterimend.rename(columns={'PROJECT': 'GENERATION_PROJECT'}, inplace=True)
    costs = pd.read_csv(os.path.join(path,'gen_build_costs.tab'), sep='\t')
    columns = ['GENERATION_PROJECT','gen_overnight_cost', 'gen_fixed_om']
    cols2 = ['GENERATION_PROJECT', 'build_year', 'gen_overnight_cost', 'gen_fixed_om']
    merged = pd.merge(gen_predeterimend, costs[columns], on=['GENERATION_PROJECT'])
    # TODO: Check why we get duplicate values from the previous row
    merged.drop_duplicates('GENERATION_PROJECT', inplace=True)
    predetermined = gen_predeterimend['GENERATION_PROJECT'].unique()
    asd.append(merged[cols2])
    for period in periods['INVESTMENT_PERIOD']:
        costs = pd.read_csv(os.path.join(path,'gen_build_costs.tab'), sep=sep)
        costs = costs[~costs['GENERATION_PROJECT'].isin(predetermined)]
        # TODO: Check why we get duplicate values from the previous row
        costs.drop_duplicates('GENERATION_PROJECT', inplace=True)
        costs['build_year'] = period
        asd.append(costs[cols2])
    gen_build_costs = pd.concat(asd)
    gen_new = pd.merge(gen_build_costs, gen_project[['GENERATION_PROJECT', 'gen_tech']], on=['GENERATION_PROJECT'])    
    gen_new_costs = modify_costs(gen_new)
    gen_new_costs.to_csv(output_file, sep=sep, index=False)

def modify_costs(data):
    cost_table = pd.read_csv('src/cost_tables.csv')
    print (cost_table.head())
    df = data.copy()
    techo = cost_table['Technology'].unique()
    for index in df.build_year.unique():
        print (index)
        mask = (df['gen_tech'].isin(techo)) & (df['build_year'] == index)
        df.loc[mask]
        cost_table.loc[cost_table['Year'] == index]
        for tech in df['gen_tech'].unique():
            if tech in cost_table['Technology'].unique():
                mask2 = (cost_table['Technology'] == tech) & (cost_table['Year'] == index)
                df.loc[mask & (df['gen_tech'] == tech)]
                cost_table.loc[mask2, 'gen_overnight_cost'].values[0]
                df.loc[mask & (df['gen_tech'] == tech), 'gen_overnight_cost'] = cost_table.loc[mask2, 'gen_overnight_cost'].values[0]
    print (data.tail())
    print (df.tail())
    return df


def create_inputs(path=script_path, **kwargs):
    """
        Create all inputs
    """
    load_data = get_load_data()

    file_path = os.path.join(path, 'periods.yaml')
    with open(file_path, "r") as stream:  
        try:
            periods = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise (exc)

    d = OrderedDict(periods)
    periods_tab = pd.DataFrame(d)
    periods_tab = periods_tab.set_index('INVESTMENT_PERIOD')

    # Create timeseries selection. This will extract peak and median day

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
    create_investment_period(peak_data)
    create_gen_build_cost(peak_data)
    create_timeseries(timeseries, **kwargs)
    create_timepoints(timeseries)
    create_variablecp(timeseries, timeseries_dict)
    create_loads(load_data, timeseries)


if __name__ == '__main__':
    create_inputs(number=2)

