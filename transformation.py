import petl as etl
import pandas as pd
import yaml
import os
import logging
from transformer import Transformer
from oracle_operator import OracleOperator

db_operator = OracleOperator("config.yaml")
logger = logging.getLogger(__name__)
defined_task_type = ['data_pull', 'data_push', 'joiner']

uri = db_operator.get_db_uri()

transformer = Transformer(uri, logger)
cur_dir = os.path.dirname(os.path.abspath(__file__))
transformer_config_file = 'transformation.yaml'
transformer_config_file = os.path.join(cur_dir, transformer_config_file)

if os.path.exists(transformer_config_file):
    with open(transformer_config_file) as f:
        transformer_config = yaml.safe_load(f)

print(transformer_config['transformation'])


for task_name in transformer_config['transformation'].keys():
    task = transformer_config['transformation'][task_name]
    print("{}-{}".format(task_name, task['task_type']))
    task_type = task.get('task_type').lower()
    if task_type in defined_task_type:
        if task_type == 'data_pull':
            task_command = "task_name+'_op' = transformer.db_data_pull(task.get('sql'))"
        elif task_type == 'data_push':
            task_command = "transformer.db_data_push(task.get('table_name'), task.get('df')+'_op', task.get('write_mode'))"
        elif task_type == 'joiner':
            task_command = "transformer.joiner(task.get('left')+'_op', task.get('right')+'_op', task.get('join_type'), task.get('left_key_cols'), task.get('right_key_cols'))"
    else:
        logger.error("Task type undefined")
        exit(1)
