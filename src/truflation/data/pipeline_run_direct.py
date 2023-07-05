#!/usr/bin/env python3
# pip install. && ./examples/example.py

"""
Usage:
  pipeline_coupler.py <details_path> ... [--debug] [--dry_run]

Arguments:
  details_path     the relative path to the pipeline details module
"""

import importlib
import logging
from truflation.data.pipeline import Pipeline
from docopt import docopt
from typing import List


def load_path(file_path_list: List[str] | str, debug: bool, dry_run: bool):
    """
    Dynamically import and run module, pipeline_details
    """
    return_value = []
    print(f'in pipeline_run_direct...')

    # convert strings to lists
    if type(file_path_list) is str:
        file_path_list = file_path_list.split(" ")
        print(f'new file path list: {file_path_list}')

    for file_path in file_path_list:
        print(f'file_path: {file_path}')
        if debug:
            print('debugging')
            logging.basicConfig(level=logging.DEBUG)
        module_name = 'my_pipeline_details'
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f'processing file path {file_path}')

        if hasattr(module, 'get_details_list'):
            return_value.extend([
                Pipeline(detail).ingest(dry_run)
                for detail in module.get_details_list()
            ])
        elif hasattr(module, 'get_details'):
            print(f'found get details...')
            pipeline_details = module.get_details()
            my_pipeline = Pipeline(pipeline_details)
            return_value.append(my_pipeline.ingest(dry_run))
            print(f'pipeline returned: {return_value}')
        else:
            raise Exception("get_details not found in supplied module,")
    print(f'final return value: {return_value}')
    return return_value

if __name__ == '__main__':
    # Get file_path from argument
    args = docopt(__doc__)

    load_path(args['<details_path>'], args['--debug'], args['--dry_run'])
