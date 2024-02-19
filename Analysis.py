from typing import Any, Optional
import matplotlib.pyplot as plt
import yaml
import requests
import pandas as pd

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

        # URL for the best-sellers list endpoint
        
        url = f'https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={key}'

        # GET data from NYT API
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response, convert to dataframe
            data = response.json()

            # Extract relevant information from the response
            books = data['results']['books']
            
            # Print the titles of the top 15 books
            for i, book in enumerate(books, 1):
                print(f"{i}. {book['title']} by {book['author']}")  # Print the book title and authors properly
        else:
            print("Error fetching data from the API")

        self.df = pd.DataFrame(books)

    def compute_analysis(self) -> Any:
        '''Analyze previously-loaded data.

This function runs an analytical measure of your choice (mean, median, linear regression, etc...)
and returns the data in a format of your choice.

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
    