# Project modules
import PortfolioBuilderObjects as obj
import TagHeuer
import Graphs as gr

# Other modules
import sys
import itertools
import time
import statistics
import random
import numpy as np
import pandas as pd
import plotly.express as px

"""
GitHub Link:
https://github.com/willburgir/PortfolioBuilder
"""

# Number of portfolios generated 
SAMPLE_SIZE = 1_000

# csv dialect
DELIMITER = ";"

# String resources
CMD_FORMAT     = "Please follow this format:\npython3 PortfolioBuilder.py [path to csv file].csv [optional flags]"
CMD_FLAGS      = "Available flags:\n--time : Shows the time tracker report." 
TIME_FLAG_STR  = "--time"

# Input arguments indexes
ASSET_RETURNS = 0
FILE_TYPE     = 1
TIME_FLAG     = 2


def get_args() -> list:
    """
    Obtains the input from the command line including:
    - Path to csv file containing historical returns of asset classes
    - File type either "csv" or "excel"
    - Flags
        -> --time : show time tracker report
        -> ? : More flags could be added in the future     

    returns a list of the form:
    [file_path : str, file_type: str, t : bool]   
    """
    args = sys.argv
    file_path = None
    t_flag    = False
    is_csv    = False
    is_excel  = False
    file_type = None

    # No args
    if len(args) < 2:
        print("ERROR : Did not provide path to historical returns (csv file)")
        print(CMD_FORMAT)
        exit(1)

    # Invalid file path
    file_path = args[1]
    if len(file_path) < 5 or file_path[-5:] != ".xlsx":
        try:
            with open(file_path, "r"):
                pass
        except FileNotFoundError:
            print(f"ERROR : No such file: '{file_path}'")
            exit(1)
    
    # Valid file path
    if file_path[-4:] == ".csv":
        file_type = "csv"
    elif len(file_path) >= 5 and file_path[-5:] == ".xlsx":
        file_type = "excel"


    flags = args[2:] # keep flags only
    for flag in flags:
        if flag == TIME_FLAG_STR:
            t_flag = True
        else:
            print(f"ERROR : Provided invalid flag '{flag}'\n")
            print(CMD_FLAGS+"\n")
            exit(1)
    
    return [file_path, file_type, t_flag]


def translate_period(period: str) -> str:
    """
    Takes in the period string provided by the user and translates it to the format 
    required by pandas resample()
    """
    daily   = ["d", "daily", "day"]
    weekly  = ["w", "weekly", "week"]
    monthly = ["m", "monthly", "month"]
    yearly  = ["y", "yearly", "year", "annual"]

    period = period.lower()
    if period in yearly:
        p = "Y"
    elif period in monthly:
        p = "M"
    elif period in weekly:
        p = "W"
    elif period in daily:
        p = "D"
    else:
        print("ERROR: Provided invalid period to translate_period()")
        print("Select from [daily, weekly, monthly, yearly]")
        exit(1)
    
    return p


def read_excel_parameters(file_path: str, sheet_name: str):
    """
    Obtains parameters from excel sheet:
    1. Risk free rate
    2. Available borrowing interest rate
    3. Periodocity of historical returns
    """
    # Params indices
    NAME = 0
    VAL  = 1
    SRC  = 2
    
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=0, index_col=0)
    except PermissionError:
        print("ERROR : Could not read Excel file.\nThis could be because the file is open. Please close it before running the program.")
        exit(1)

    params = []
    for tp in df.itertuples():
        param_name = tp[0]
        param_val = tp[1]
        param_src = tp[2]
        params.append((param_name, param_val, param_src))

    risk_free_rate = params[0][VAL]
    available_rate = params[1][VAL]
    periodicity    = params[2][VAL]

    return risk_free_rate, available_rate,  periodicity


def read_excel_user_portfolios(file_path: str, sheet_name: str) -> list:
    """
    Returns a list of user defined Portfolio objects from the input Excel file
    """
    user_portfolios = []

    return user_portfolios


def read_excel_input(file_path : str, file_type : str):
    """
    Reads the input excel containing:
    1. Asset Classes historical returns
    2. Rates (risk free & available borrowing interest rate)
    3. Portfolios with compositions

    Returns:
    1. List of AssetClass objects
    2. Correlation matrix
    3. Risk free rate
    4. Available borrowing interest rate
    5. Periodicity of historical returns
    6. List of User Portfolio objects to be highlighted 
    """
    DATE_DF_LABEL = "Date"
    ASSET_CLASSES_SHEET = "Asset Classes"
    PARAMETERS_SHEET    = "Parameters"
    PORTFOLIOS_SHEET    = "Portfolios"

    #arguments 
    file_type = "excel"
    file_path = "input/input.xlsx"

    asset_class_list = []

    if file_type != "excel":
        print("ERROR : Invalid file type. Please use Excel")
        exit(1)

    try:
        rf, available_rate, period = read_excel_parameters(file_path, PARAMETERS_SHEET)
        df = pd.read_excel(file_path, sheet_name="Asset Classes", header=0, index_col=0)
    except PermissionError:
        print("ERROR : Could not read Excel file.\nThis could be because the file is open. Please close it before running the program.")
        exit(1)

    resample_period = translate_period(period)

    # Assuming 'Date' is the column with datetime values
    df = df.resample(resample_period).apply(lambda x: (1 + x).prod() - 1)
    df = df.T
    
    # create list of AssetClass objects for each row in the df
    for tp in df.itertuples():
        name = tp[0]
        row  = pd.Series(tp[1:])
        asset_class = obj.AssetClass(name=name, historical_returns=row, period=period)
        asset_class_list.append(asset_class)

    # Get corr_matrix
    corr_matrix = df.T.corr()
    corr_matrix

    return asset_class_list, corr_matrix, rf, available_rate, period, None


def get_random_weights(n):
    """
    Creates a list of n random weights which sum up to 1
    """
    weights = []
    
    for i in range(n):
        weights.append(random.random())
    
    # Scale to 1
    weights = weights/np.sum(weights)*100
    return weights


def create_portfolios(asset_classes : list, corr_matrix : object, sample_size : int) -> list:
    """
    Creates all possible portfolios based on different weighing 
    of asset classes in increments of 1% 

    returns a list of Portfolio objects
    """
    # TODO
    # Add multithreading to this function
    BIG_NUMBER = 1_000_000

    n = len(asset_classes)
    
    if n == 0:
        print("ERROR : Passed an empty list to create_portfolios")
        exit(1)

    portfolios = []
    portfolio_num = 1

    for observation in range(sample_size):
        # pick n ints, one for each asset class
        # TODO
        # check random distribution 
        random_weights = get_random_weights(n)

        # combine into {AssetClass : weight}
        composition = {}
        index = 0
        for asset_class in asset_classes:
            composition[asset_class] = random_weights[index]
            index += 1
        
        # create portfolio
        portfolio = obj.Portfolio(f"Portfolio{portfolio_num}", composition, corr_matrix)
        portfolios.append(portfolio)
        portfolio_num += 1

    return portfolios


def compute_sharpe(df: pd.DataFrame, rf: float) -> pd.DataFrame:
    """
    Input: 
        - df : pandas DataFrame containing portfolios
        - rf : Risk free rate in %

    Returns a df with additional column "Sharpe Ratio"

    Requirement:
    The df passed into this function must have columns named exactly 
    "E(r)" and "sd"
    """
    ER = "E(r)"
    SD = "sd"

    df["Sharpe"] = np.maximum(0, (df[ER] - rf) / df[SD])
    return df



def main():
    # Prepare TimeTracker
    tt = TagHeuer.TimeTracker()

    func_name = "Read command line arguments"
    tt.start(func_name)
    # Get command line arguments
    user_input = get_args()
    returns_file  = user_input[ASSET_RETURNS]
    file_type = user_input[FILE_TYPE]
    time_flag = user_input[TIME_FLAG]
    tt.end(func_name)

    func_name = "Read input data"
    tt.start(func_name)
    # Create AssetClass objects from .csv file
    asset_classes, corr_matrix, risk_free_rate, available_rate, period, user_portfolios = read_excel_input(returns_file, file_type)
    tt.end(func_name)

    func_name = "create_portfolios"
    tt.start(func_name)
    # Generate portfolios
    portfolios = create_portfolios(asset_classes, corr_matrix, SAMPLE_SIZE)
    tt.end(func_name)

    func_name = "portfolios_df_conversion"
    tt.start(func_name)
    portfolios_df = obj.convert_portfolios_into_df(portfolios)
    tt.end(func_name)

    func_name = "compute_sharpe"
    tt.start(func_name)
    portfolios_df = compute_sharpe(portfolios_df, risk_free_rate)
    tt.end(func_name)

    func_name = "get_scatter_plot"
    tt.start(func_name)
    eff_frontier = gr.get_scatter_plot(portfolios_df, title=f"Efficient Frontier based on {period.lower()} returns : {SAMPLE_SIZE} portfolios")
    eff_frontier, optimal_portfolio = gr.add_CAL(eff_frontier, portfolios_df, risk_free_rate)
    eff_frontier.show()
    tt.end(func_name)

    print("\n~~~ Optimal Portfolio (with given asset classes) ~~~\n")
    print(optimal_portfolio)

    
    

    if time_flag:
        tt.report()
    
    return 


if __name__ == "__main__":
    main()