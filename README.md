# NYT Book API Analysis Program

This Python program performs analysis on data obtained from the New York Times (NYT) Best Sellers API. It retrieves data on authors, book titles, NYT best seller rank, and weeks on the list, among other attributes, and provides insights into the average weeks on the NYT Best Sellers list by rank.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/stephenpetersen/DSI-BRS-Assignment.git    
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   
## Usage

### Configuration

Before running the program, ensure that you have configured the necessary parameters:

- **System Configurations**: In .gitignore.
- **User Configurations**: Optionally, customize user-specific settings in the `configs/user_config.yml` file.
- **Analysis Configuration**: Specify the path to the analysis/job-specific configuration file.

### Running the Program

To run the program, execute the following command:
```bash
python Analysis.py path_to_analysis_config.yml
```
Replace `path_to_analysis_config.yml` with the path to your analysis configuration file.

## Functionality

### Loading Data

The program retrieves data from the NYT Best Sellers API, fetching records for the past 8 weeks. The retrieved data includes information about authors, book titles, best seller rank, weeks on the list, etc. The data is stored within the program for further analysis.

### Analysis

The program computes the average weeks on the NYT Best Sellers list by rank. It uses the pandas library to calculate the mean weeks on the list for each rank, providing insights into the relationship between book rank and duration on the best sellers list.

### Plotting Data

The program generates a bar plot to visualize the analysis results. It displays the mean weeks on the list for each rank, providing a graphical representation of the analysis.

### Notification

Upon completion of the analysis, the program sends a notification to the ntfy.sh webpush service. The notification includes details about the completion time and prompts the user to check the analysis results and generated figure.

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`

## Credits

This program was developed by Stephen Petersen.

## License

This project is licensed under the terms of the MIT license.
