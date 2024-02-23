from typing import Any, Optional
import matplotlib.pyplot as plt
import yaml
import requests
import pandas as pd
import datetime as dt
import time
import logging

# configure logging
logging.basicConfig(level=logging.ERROR, filename='error.log')

class nyt_bestsellers():

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
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml', 'configs/analysis_config.yml']

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

    def load_data(self, sleep=12) -> None:
        ''' Retrieve data from the NYT Best Sellers API

        This function makes a series of HTTPS request to the NYT Best Sellers API and retrieves data on authors,
        book titles, NYT best seller rank, weeks on list, etc. The fuction loops over the last 8 weeks to retrieve
        about 120 records (15 per week, times 8 weeks). The data is stored in the Analysis object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        '''
        
        # load system configuration
        with open('configs/system_config.yml', 'r') as f:
            system_config = yaml.safe_load(f)

        # access NYT API key from the system configuration
        key = system_config.get('nyt_key')

        # loop dates
        current_date = dt.date.today()
        loop_date = current_date - dt.timedelta(weeks=7) # gets us 2 months of weekly books lists
        one_week = dt.timedelta(weeks=1)

        # initialize empty list to hold the API data
        self.books = []

        while loop_date <= current_date:
            try:
                print(loop_date)
                # URL for the best-sellers list endpoint
                url = f'https://api.nytimes.com/svc/books/v3/lists/{loop_date}/hardcover-fiction.json?api-key={key}'

                # GET data from NYT API
                response = requests.get(url)
                
                # check if the request was successful
                if response.status_code == 200 :
                    print('Data fetched successfully from the API')
                else :
                    raise Exception(
                        'Error fetching data from the API. One possibility is you overwrote the sleep parameter, which controls the timing of calls to the API. Suggest increasing to at least 12 seconds.')
                    
                # parse the JSON response
                data = response.json()
                
                # append from loop
                self.books.extend(data['results']['books'])
                
                # increment week
                loop_date += one_week
                
                # pause for 12 seconds or user input (apparently NYT controls rapid API calls)
                time.sleep(sleep)
                
            except Exception as e:
                logging.error(f"An error occurred while fetching data: {e}")
                raise

        self.df = pd.DataFrame(self.books).dropna(how='all')

        if not isinstance(self.df, pd.DataFrame) :
            raise TypeError('The stored value is not a DataFrame.')
        else :
            return self.df

    def compute_analysis(self) -> Any:
        '''Compute the average weeks on the New York Times Best Sellers list by rank.

        This function utilizes the groupby functionality from the pandas library to calculate 
        the mean 'weeks on list' for each rank of the book on the New York Times Best Sellers list.
        This checks for endogeneity of rank and weeks on the list (e.g., do higher ranked books stay on
        the list for longer?).

        Parameters
        ----------
        None

        Returns
        -------
        analysis_output : Any
            A pandas Series containing the mean weeks on the list for each rank.
        '''

        # compute average weeks on list by rank       
        mean_weeks_on_list = self.df.groupby('rank')['weeks_on_list'].mean()
        return mean_weeks_on_list

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
        mean_weeks_on_list = self.compute_analysis()

        # plot configs
        color = self.config['plot_config']['color']
        title = self.config['plot_config']['title']
        xtitle = self.config['plot_config']['xtitle']
        ytitle = self.config['plot_config']['ytitle']
        fig_size = self.config['plot_config']['fig_size']

        # bar Plot
        fig1 = plt.figure(figsize=fig_size)
        plt.bar(mean_weeks_on_list.index, mean_weeks_on_list.values, color=color)
        plt.title(title)
        plt.xlabel(xtitle)
        plt.ylabel(ytitle)
        plt.xticks(mean_weeks_on_list.index)
        plt.grid(False)

        if save_path:
            plt.savefig(f'{save_path}fig1.png')
        else:
            plt.savefig('figures/fig1.png')

        plt.show()

        # scatter plot (added from issue #3)
        fig2 = plt.figure(figsize=fig_size)
        plt.scatter(self.df['rank'], self.df['weeks_on_list'], color=color, alpha=0.5)
        plt.title('Scatter Plot of Weeks on List vs Rank')
        plt.xlabel(xtitle)
        plt.ylabel(ytitle)
        plt.grid(True)

        if save_path:
            plt.savefig(f'{save_path}fig2.png')
        else:
            plt.savefig('figures/fig2.png')

        plt.show()

        return fig1, fig2

    def notify_done(self) -> None:
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

        # notification of completed analysis
        datetime = dt.datetime.now()
        requests.post(self.config['ntfy_topic'],
            data = f'✅ Analysis completed at {datetime}. Check results and figure!'.encode(encoding='utf-8'),
            headers = {'Title': 'NYT Book API Assignment'})
    