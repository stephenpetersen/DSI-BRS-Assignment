from typing import Any, Optional
import matplotlib.pyplot as plt 
import yaml
import requests


class Analysis():

    def __init__(self) -> None:
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml', 'configs/analysis_config.yml']

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS

        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in paths:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            config.update(this_config)

        self.config = config
