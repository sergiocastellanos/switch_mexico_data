"""
    Utilities por switch data creation
"""
import os
import sys
import logging
import pdb
import pandas as pd
from logging.config import fileConfig

logfile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.ini')
print (logfile_path)
fileConfig(logfile_path)
logger = logging.getLogger('Logger')

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



def create_default_scenario():

    gen_project = pd.read_csv('src/generation_projects_info.tab', sep='\t')

    # This should be a dictionary
    load_zones = pd.read_csv('src/load_zones.tab', sep='\t',
            usecols=[0])
    gen_predeterimend = pd.read_csv('./src/gen_build_predetermined.tab', sep='\t')

    iter_name = 1
    new_gens = []
    for row in load_zones.itertuples():
        print (row[1])
        gen_default = pd.read_csv('./src/generation_default.csv')
        lz_tech = gen_project.groupby(['gen_load_zone'])['gen_tech'].get_group((row[1])).unique()
        new_gen = gen_default.loc[gen_default['gen_tech'].isin(lz_tech)].copy()
        new_gen.loc[:, 'gen_load_zone'] = row[1]
        new_gen.loc[:, 'GENERATION_PROJECT'] = new_gen['GENERATION_PROJECT'].map(str.lower) + f'_{iter_name:03d}'
        #  gen_project = gen_project.append(new_gen, ignore_index=True)
        new_gens.append(new_gen)
        iter_name +=1
    gen_project = pd.concat(new_gens)
    gen_project.to_csv('generation_test.tab', sep='\t', index=False)


if __name__ == '__main__':
    #  pp = PowerPlant('UUUID', 'solar', 'solar', 'Mulege')
    #  pp.add()
    create_default_scenario()

