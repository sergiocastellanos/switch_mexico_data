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
import click
import numpy as np
import pandas as pd
from collections import OrderedDict

script_path = os.path.dirname(__file__)
parent_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(parent_path, 'data/clean/loads')
output_path  = os.path.join(parent_path, 'data/clean/switch_inputs/')

def get_load_data(path=data_path, filename='HighLoads.csv',
         total=False, *args, **kwargs):
    """ Read load consumption data

    Args:
        path (str): path to the file,
        filename (str): name of the file,
        total (bool): if true returns only the sum of all loads.

        TODO:
            * Migrate this function to utilities
            * This could be a csv or it could connect to a DB.
            * This could be a csv or it could connect to a DB.
    """

    file_path = os.path.join(path, filename)

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise ('File not found. Please verify the file is in: {}'.format(os.path.join(path, filename)))

    # Calculate the sum of loads
    df['total'] = df.sum(axis=1)

    try:
        # Shift load data to match generation.
        df.loc[:, 'hour'] -= 1
    except:
        print ('Something went wrong')
        pass

    # Add datetime index
    df.index = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

    df = df.sort_index()

    if total:
        return df[['total']]
    else:
        return df

def get_peak_day(data, number, freq='MS'):
    """ Construc a representative day based on a single timestamp

    Args:
        data (pd.DataFrame): data to filter,
        number (float): number of days to return.

    Note:
        * Month start is to avoid getting more timepoints in a even division
    """
    years = []

    # Check if number of timepoints is multiple
    if not 24 % number == 0 :
        raise ValueError('Odd number of timepoints. Use even number')

    # Iterate over all months
    for _, group in data.groupby([pd.Grouper(freq='A'),\
        pd.Grouper(freq=freq)]):

        delta_t = int(24/number)

        #Temporal fix for duplicates
        group = group[~group.index.duplicated(keep='last')]

        # Get index of max value
        peak_timestamp = group.idxmax()

        # Convert the max value index to timestamp
        mask = peak_timestamp.strftime('%Y-%m-%d')

        peak_loc = group[mask].index.get_loc(peak_timestamp)

        # Check if delta_t does not jump to next day
        if (peak_timestamp.hour + delta_t ) > 23:
            peak_timestamps = group.loc[mask].iloc[peak_loc::-delta_t]
            if len(peak_timestamps) < delta_t:
                missing = number - len(peak_timestamps)
                peak_timestamps = (peak_timestamps.append(group
                                    .loc[mask]
                                    .iloc[peak_loc::delta_t][1:missing+1]))
        else:
            peak_timestamps = group.loc[mask].iloc[peak_loc::delta_t]
            if len(peak_timestamps) < delta_t:
                missing = number - len(peak_timestamps)
                peak_timestamps = (peak_timestamps.append(group
                                    .loc[mask]
                                    .iloc[peak_loc::-delta_t][1:missing+1]))

        # Sort the index. Why not?
        peak_timestamps = peak_timestamps.sort_index().reset_index()

        years.append(peak_timestamps)

    output_data = pd.concat(years)
    output_data = output_data.rename(columns={'index':'date',
                                    'total':'peak_day'})
    return (output_data)

def get_median_day(data, number, freq='MS'):
    """ Calculate median day giving a timeseries

    Args:
        data (pd.DataFrame): data to filter,
        number (float): number of days to return.

    Note(s):
        * Month start is to avoid getting more timepoints in a even division
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

def create_investment_period(path=script_path, ext='.tab', **kwargs):
    """ Create periods file using periods.yaml input

    Args:
        path (str): path to file,
        ext (str): output extension to save the file

    Note(s):
        * .tab extension is to match the switch inputs,
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
    """ Create timepoints file

    Args:
        data (pd.DataFrame): dataframe witht dates ,
        ext (str): output extension to save the file.

    Note(s):
        * .tab extension is to match the switch inputs,
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


def create_strings(data, scale_to_period, identifier='P',  ext='.tab',
        **kwargs):
    """ Create strings to process files

    Args:
        data (pd.DataFrame): dataframe witht dates,
        scale_to_period (int): difference between period ranges,
        identifier (str): identifier for each series
        ext (str): output extension to save the file.

    Note(s):
        * .tab extension is to match the switch inputs,
    """

    strftime = '%Y%m%d%H' #  Strftime for label
    data['timestamp'] = data['date'].dt.strftime(strftime)
    data['TIMESERIES'] = data['date'].dt.strftime('%Y_%m{}'.format(identifier))
    data['daysinmonth'] = data['date'].dt.daysinmonth

    # TODO: Fix this. Probably bug in near future
    data['ts_period'] = data['date'].dt.year
    data['scale_to_period'] = scale_to_period

    return (data)

def create_timeseries(data, number, ext='.tab', **kwargs):
    """ Create timeseries output file

    Args:
        data (pd.DataFrame): dataframe witht dates,
        number (int) : number of timepoints
        ext (str): output extension to save the file.

    Note(s):
        * .tab extension is to match the switch inputs,
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
    #       the total amount of years?
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
    """ Create variable capacity factor  output file

    Args:
        data (pd.DataFrame): dataframe witht dates,
        timeseries_dict (Dict): dictionary with the timeseries for each period,
        path (string): path to renewable energy file,
        ext (str): output extension to save the file.

    Note(s):
        * .tab extension is to match the switch inputs,
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

    file_name = 'ren-all2.csv'
    file_path = os.path.join(path, 'data/clean/SWITCH/')

    ren_cap_data = pd.read_csv(os.path.join(file_path, file_name), index_col=0,
                               parse_dates=True)

    # Quick fix to names
    replaces = ['é', 'á', 'í', 'ó', 'ú', 'ñ']
    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('é', 'e')
    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('á', 'a')
    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('í', 'i')
    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('ó', 'o')
    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('ú', 'u')
    ren_cap_data['GENERATION_PROJECT'] = ren_cap_data['GENERATION_PROJECT'].str.replace('ñ', 'n')

    # Extract datetime without year information
    filter_dates = pd.DatetimeIndex(data['date'].reset_index(drop=True)).strftime('%m-%d %H:%M:%S')

    ren_tmp = ren_cap_data.copy()
    print (ren_tmp.head())

    list1 = []
    for row, value in timeseries_dict.items():
        print (row)
        tmp2 = pd.concat(value)
        filter_dates = (pd.DatetimeIndex(tmp2['date']
                                    .reset_index(drop=True))
                                    .strftime('%m-%d %H:%M:%S'))
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
    """ Create load data output file

    Args:
        load (pd.DataFrame): load data
        data (pd.DataFrame): dataframe witht dates,
        ext (str): output extension to save the file.

    Note(s):
        * .tab extension is to match the switch inputs,
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
    """ Create gen build cost output file

    Args:
        data (pd.DataFrame): dataframe witht dates,
        ext (str): output extension to save the file.

    Note(s):
        * .tab extension is to match the switch inputs,
    """

    if ext == '.tab': sep='\t'
    output_file = output_path + 'gen_build_costs' + ext

    # TODO:  Change the direction of this file
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

def create_gen_build_cost_new(data, ext='.tab', path=script_path,
    **kwargs):
    """ Create gen build cost output file

    Args:
        data (pd.DataFrame): dataframe witht dates,
        ext (str): output extension to save the file.

    Note(s):
        * .tab extension is to match the switch inputs,
    """
    gen_project = pd.read_csv('src/generation_projects_info.tab', sep='\t')
    cost_table = pd.read_csv('src/cost_tables.csv')

    if ext == '.tab': sep='\t'

    output_file = output_path + 'gen_build_costs' + ext

    # TODO:  Change the direction of this file
    file_path = os.path.join(path, 'periods.yaml')
    with open(file_path, "r") as stream:
        try:
            periods = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise (exc)

    df = data.copy()
    techo = cost_table['Technology'].unique()
    for period in periods['INVESTMENT_PERIOD']:
        print (period)
        mask = (gen_project['gen_tech'].isin(techo)))
        sys.exit(1)
        df.loc[mask]
        cost_table.loc[cost_table['Year'] == index]
        for tech in df['gen_tech'].unique():
            if tech in cost_table['Technology'].unique():
                mask2 = (cost_table['Technology'] == tech) & (cost_table['Year'] == index)
                df.loc[mask & (df['gen_tech'] == tech)]
                cost_table.loc[mask2, 'gen_overnight_cost'].values[0]
                df.loc[mask & (df['gen_tech'] == tech), 'gen_overnight_cost'] = cost_table.loc[mask2, 'gen_overnight_cost'].values[0]
    return (df)

def modify_costs(data):
    """ Modify cost data to derate it

    Args:
        data (pd.DataFrame): dataframe witht dates,

    Note(s):
        * This read the cost table and modify the cost by period
    """

    # TODO: Make a more cleaner way to load the file
    cost_table = pd.read_csv('src/cost_tables.csv')

    df = data.copy()
    techo = cost_table['Technology'].unique()
    for index in df.build_year.unique():
        mask = (df['gen_tech'].isin(techo)) & (df['build_year'] == index)
        df.loc[mask]
        cost_table.loc[cost_table['Year'] == index]
        for tech in df['gen_tech'].unique():
            if tech in cost_table['Technology'].unique():
                mask2 = (cost_table['Technology'] == tech) & (cost_table['Year'] == index)
                df.loc[mask & (df['gen_tech'] == tech)]
                cost_table.loc[mask2, 'gen_overnight_cost'].values[0]
                df.loc[mask & (df['gen_tech'] == tech), 'gen_overnight_cost'] = cost_table.loc[mask2, 'gen_overnight_cost'].values[0]
    return (df)

@click.command()
@click.option('--number', default=4, prompt='Number of timepoints',
        help='Number of timepoints')
def create_inputs(number, path=script_path, **kwargs):
    """ Main function that creates all the inputs

    Args:
        path (str): path to script folder

    Note(s):
        * This generates all the inputs
    """
    print (number)

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
        peak_data = get_peak_day(load_data[str(periods)]['total'], number, freq='1MS', **kwargs)
        median_data = get_median_day(load_data[str(periods)]['total'], number, freq='1MS', **kwargs)
        timeseries_dict[periods].append(create_strings(peak_data, scale_to_period))
        timeseries_dict[periods].append(create_strings(median_data, scale_to_period,
                                        identifier='M'))
        timeseries.append(create_strings(peak_data, scale_to_period))
        timeseries.append(create_strings(median_data, scale_to_period,
                                        identifier='M'))
    create_investment_period()
    #  create_gen_build_cost(peak_data)
    create_gen_build_cost_new(peak_data)
    create_timeseries(timeseries, number, **kwargs)
    create_timepoints(timeseries)
    create_variablecp(timeseries, timeseries_dict)
    create_loads(load_data, timeseries)


if __name__ == '__main__':
    create_inputs()

