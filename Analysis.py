import matplotlib.pyplot as plt 
import yaml
import requests
import base64


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

    def get_token(self):
        # Spotify API credentials
        with open('configs/system_config.yml', 'r') as f:
            sys_config = yaml.safe_load(f)
            client_id = sys_config['client_id']
            client_secret = sys_config['client_secret']

        # Base64 encode client ID and client secret
        client_credentials = f"{client_id}:{client_secret}"
        client_credentials_b64 = base64.b64encode(client_credentials.encode()).decode()

        # Define headers for authorization
        headers = {'Authorization': f'Basic {client_credentials_b64}'}

        # Define payload for token request
        payload = {'grant_type': 'client_credentials'}

        # Make a POST request to get the access token
        response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=payload)

        # Check if request was successful
        if response.status_code == 200:
            # Extract access token from response
            access_token = response.json()['access_token']
            print("Authentication successful! Access Token:", access_token)
            return access_token
        else:
            print("Authentication failed:", response.text)