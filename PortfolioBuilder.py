import PortfolioBuilderObjects as obj
import TagHeuer
import sys
import itertools
import time
import statistics
import random
import numpy as np
import pandas as pd

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


def getArgs() -> list:
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


def readAssetReturns(file_path : str, file_type : str):
    """
    Reads the input excel or csv containing asset returns per asset class

    Returns a list of AssetClass objects and a correlation matrix
    """
    asset_class_list = []

    if file_type not in ["csv", "excel"]:
        print("ERROR : Invalid file type. Please use Excel or csv")
        exit(1)

    if file_type == "csv":
        # df stands for data frame
        df = pd.read_csv(file_path, delimiter=DELIMITER, header=0, index_col=0)
        df = df.T

    elif file_type == "excel":
        try:
            df = pd.read_excel(file_path, header=0, index_col=0)
            df = df.T
        except PermissionError:
            print("ERROR : Could not read Excel file.\nThis could be because the file is open. Please close it before running the program.")
            exit(1)

    # create list of AssetClass objects for each row in the df
    for key, val in df.items():

        name = key
        returns_dict = {}
        for period, returns in val.items():
            returns_dict[period] = returns
        asset_class = obj.AssetClass(name=name, historical_returns=returns_dict)
        asset_class_list.append(asset_class)

    # Get corr_matrix
    corr_matrix = df.corr()

    return asset_class_list, corr_matrix


def createRandomPortfolios(asset_classes : list, corr_matrix : object, sample_size : int) -> list:
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
        print("ERROR : Passed an empty list to createRandomPortfolios")
        exit(1)

    portfolios = []
    portfolio_num = 1

    for observation in range(sample_size):
        # pick n ints, one for each asset class
        # TODO
        # check random distribution 
        random_weights = []
        for i in asset_classes:
            random_number = random.randint(0, BIG_NUMBER)
            random_weights.append(random_number) 

        # turn into weights out of 100%
        total = sum(random_weights)

        for i in range(n):
            here = random_weights[i] 
            random_weights[i] = here/total * 100

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


def create_Er_sd_graph(portfolios : list, filename = "EfficientFrontier") -> None:
    """
    Creates a graph plotting portfolios with:
    x-axis : E(r)
    y-axis : sd
    """
    return

def main():
    # Prepare TimeTracker
    tt = TagHeuer.TimeTracker()

    func_name = "Read command line arguments"
    tt.start(func_name)
    # Get command line arguments
    user_input = getArgs()
    returns_file  = user_input[ASSET_RETURNS]
    file_type = user_input[FILE_TYPE]
    time_flag = user_input[TIME_FLAG]
    tt.end(func_name)

    func_name = "Read input data"
    tt.start(func_name)
    # Create AssetClass objects from .csv file
    asset_classes, corr_matrix = readAssetReturns(returns_file, file_type)
    tt.end(func_name)

    func_name = "createPortfolios"
    tt.start(func_name)
    # Generate portfolios
    portfolios = createRandomPortfolios(asset_classes, corr_matrix, SAMPLE_SIZE)
    tt.end(func_name)

    
    print(f"Number of generated portfolios : {len(portfolios)}")
    if len(portfolios) >= 1:
        print(f"{portfolios[0]}")
    
    

    if time_flag:
        tt.report()
    
    return 


if __name__ == "__main__":
    main()