from typing import Any, Optional
import matplotlib.pyplot as plt
import yaml
import requests
import pandas as pd
import datetime as dt
import time

class Analysis():

    def __init__(self, analysis_config: str) -> None:

        ''' Load config into an Analysis object

Load system-wide configuration from `configs/system_config.yml`, user configuration from
`configs/user_config.yml`, and the specified analysis configuration file

Parameters
----------
analysis_config : str
    Path to the analysis/job-specific configuration file

Returns
-------
analysis_obj : Analysis
    Analysis object containing consolidated parameters from the configuration files

'''
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in paths:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            config.update(this_config)

        self.config = config

    def load_data(self) -> None:
        ''' Retrieve data from the NYT Best Sellers API

This function makes an HTTPS request to the NYT Best Sellers API and retrieves your Authors and Booktitles. The data is
stored in the Analysis object.

Parameters
----------
None

Returns
-------
None

'''
        # Load system configuration
        with open('configs/system_config.yml', 'r') as f:
            system_config = yaml.safe_load(f)

        # Access NYT API key from the system configuration
        key = system_config.get('nyt_key')

        # loop dates
        current_date = dt.date.today()
        loop_date = current_date - dt.timedelta(weeks=8) # gets us 2 months of weekly books lists
        one_week = dt.timedelta(weeks=1)

        self.books = []

        while loop_date <= current_date:
            print(loop_date)
            # URL for the best-sellers list endpoint
            url = f'https://api.nytimes.com/svc/books/v3/lists/{loop_date}/hardcover-fiction.json?api-key={key}'

            # GET data from NYT API
            response = requests.get(url)

            # check if the request was successful
            if response.status_code == 200:
                print('Data fetched successfully data from the API')
            else:
                print('Error fetching data from the API')

            # parse the JSON response
            data = response.json()

            # append from loop
            self.books.extend(data['results']['books'])

            # increment week
            loop_date += one_week
            
            # Pause for 12 seconds (apparently NYT titrates API calls)
            time.sleep(12)

        self.df = pd.DataFrame(self.books)

    def compute_analysis(self) -> Any:
        '''Provides and average for weeks on NYT Best Sellers list, by rank.

This function uses group by from the pandas library to compute mean 'weeks on list' by the rank of the book on the list and returns the result as a matrix.

Parameters
----------
None

Returns
-------
analysis_output : Any

'''
        # Calculate something       

        pass

    def plot_data(self, save_path: Optional[str] = None) -> plt.Figure:
        ''' Analyze and plot data

Generates a plot, display it to screen, and save it to the path in the parameter `save_path`, or 
the path from the configuration file if not specified.

Parameters
----------
save_path : str, optional
    Save path for the generated figure

Returns
-------
fig : matplotlib.Figure

'''
        # Add plot code here

        fig = plt.figure()
        if save_path:
            plt.savefig(f'{save_path}fig.png')
        else:
            plt.savefig('figures/fig.png')
        return fig

    def notify_done(self, message: str) -> None:
        ''' Notify the user that analysis is complete.

Send a notification to the user through the ntfy.sh webpush service.

Parameters
----------
message : str
  Text of the notification to send

Returns
-------
None

'''
        pass
    