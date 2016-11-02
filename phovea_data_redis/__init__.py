###############################################################################
# Caleydo - Visualization for Molecular Biology - http://caleydo.org
# Copyright (c) The Caleydo Team. All rights reserved.
# Licensed under the new BSD license, available at http://caleydo.org/license
###############################################################################


def phovea(registry):
  """
  register extension points
  :param registry:
  """
  registry.append('manager','idmanager','phovea_data_redis.assigner', {
   'priority': -5,
   'singleton': True
  })

  registry.append('manager','mappingmanager','phovea_data_redis.mapper', {
   'priority': -5,
   'singleton': True
  })

  registry.append('mapping_table','phovea_data_redis','phovea_data_redis.mapping_table', {
   'mappings': [
    'Ensembl2UniProt',
    'UniProt2Ensembl'
   ]
  })
  pass


def phovea_config():
  """
  :return: file pointer to config file
  """
  from os import path
  here = path.abspath(path.dirname(__file__))
  config_file = path.join(here, 'config.json')
  return config_file if path.exists(config_file) else None
