"""
    Utilities por switch data creation
"""
import os
import sys
import yaml
import logging
import pdb
import pandas as pd
from logging.config import fileConfig

logfile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.ini')
print (logfile_path)
fileConfig(logfile_path)
logger = logging.getLogger('Logger')
script_path = os.path.dirname(__file__)
parent_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(parent_path, 'data/clean/loads')
output_path  = os.path.join(parent_path, 'data/clean/switch_inputs/')

def read_yaml(path, filename: str):
    """ Read yaml file"""

    file_path = os.path.join(path, filename)

    with open(file_path, 'r') as stream:
        try:
            yaml_file = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise (exc)

    return yaml_file

def create_renewable_data(path: os.PathLike, filename: str):
    logger.debug('often makes a very good meal of %s', 'visiting tourists')
    return (path)

class PowerPlant:
    """
    Power plant class testing
    """

    def __init__(self, uuid, tech, fuel, lz):
        self.uuid = uuid
        self.tech = tech
        self.lz = lz

    def add(self):
        print (type(self))

def create_gen_build_cost_new(ext='.tab', path=script_path,
    **kwargs):
    """ Create gen build cost output file

    Args:
        data (pd.DataFrame): dataframe witht dates,
        ext (str): output extension to save the file.

    Note(s):
        * .tab extension is to match the switch inputs,
    """
    cost_table = pd.read_csv('src/gen_cost_reference.csv')
    tech_costs = pd.read_csv('./src/technology_cost.csv')
    gen_project = pd.read_csv('generation_test.tab', sep='\t')

    if ext == '.tab': sep='\t'

    output_file = output_path + 'gen_build_costs' + ext

    # TODO:  Change the direction of this file

    periods = read_yaml(path, 'periods.yaml')

    # FIXME: This will only work if there is no repeated elements

    gen_costs = pd.merge(gen_project, cost_table, on='gen_tech')
    cols = ['GENERATION_PROJECT', 'build_year', 'gen_overnight_cost',
            'gen_fixed_om', 'gen_tech']

    output_list = []
    #  output_list.append(gen_costs[cols])
    for period in periods['INVESTMENT_PERIOD']:
        print (period)
        gen_costs.loc[:, 'build_year'] = period
        output_list.append(gen_costs[cols])

    gen_build_cost = pd.concat(output_list)
    gen_build_cost.to_csv('gen_build_cost.tab', sep=sep)

    return (gen_build_cost)

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
        for tech in df['gen_tech'].unique():
            if tech in cost_table['Technology'].unique():
                mask2 = (cost_table['Technology'] == tech) & (cost_table['Year'] == index)
                cost_table.loc[mask2, 'gen_overnight_cost'].values[0]
                df.loc[mask & (df['gen_tech'] == tech), 'gen_overnight_cost'] = cost_table.loc[mask2, 'gen_overnight_cost'].values[0]
                df.loc[mask & (df['gen_tech'] == tech), 'gen_fixed_om'] = cost_table.loc[mask2, 'gen_fixed_om'].values[0]
    df.sort_values(['GENERATION_PROJECT', 'build_year'], ascending=[True, True]).to_csv('gen_build_cost.tab', sep=sep, index=False)
    return (df)


def create_default_scenario():
    """  Create default scenario with existing technology for each loadzone """

    gen_project = pd.read_csv('src/generation_projects_info.tab', sep='\t')
    column_order = gen_project.columns
    print (column_order.values)

    #FIXME: Quick fix to replace tg for turbo_gas
    gen_project['gen_tech'] = gen_project['gen_tech'].replace('tg','turbo_gas')

    # This should be a dictionary
    load_zones = pd.read_csv('src/load_zones.tab', sep='\t',
            usecols=[0])

    iter_name = 1
    new_gens = []
    for row in load_zones.itertuples():
        print (row[1])
        gen = f'{row[1]}_hh'
        gen_default = pd.read_csv('./src/technology_cost.csv')
        lz_tech = gen_project.groupby(['gen_load_zone'])['gen_tech'].get_group((row[1])).unique()
        new_gen = gen_default.loc[gen_default['gen_tech'].str.startswith(tuple(lz_tech))].copy()
        new_gen.loc[:, 'gen_load_zone'] = row[1]
        new_gen.loc[:, 'GENERATION_PROJECT'] = new_gen['GENERATION_PROJECT'].map(str.lower) + f'_{iter_name:03d}'
        #  gen_project = gen_project.append(new_gen, ignore_index=True)
        new_gens.append(new_gen)
        iter_name +=1
    gen_project = pd.concat(new_gens)
    gen_project[column_order].to_csv('generation_test.tab', sep='\t', index=False)


if __name__ == '__main__':
    #  pp = PowerPlant('UUUID', 'solar', 'solar', 'Mulege')
    #  pp.add()
    create_default_scenario()
    gen_build_cost = create_gen_build_cost_new()
    modify_costs(gen_build_cost)

