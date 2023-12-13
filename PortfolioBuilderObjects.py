import numpy as np
import pandas as pd
from xlwings import view


class AssetClass:
    """
    Risky asset classes with:
    expected returns as a measure of returns
    standard deviation as a measure of risk (>0)
    """
    name = None 
    historical_returns = {}
    Er = None # E(r) Expected Return 
    sd = None # Standard deviation 

    def __init__(self, name : str, historical_returns : dict):
        # type validation
        if not isinstance(historical_returns, dict):
            raise ValueError("Historical returns should be provided as a dictionary.")
        
        self.name = name
        self.historical_returns = historical_returns
        self.Er = self.getExpReturn(historical_returns)
        self.sd = self.getSD(historical_returns)


    def getName(self):
        return self.name
    def getEr(self):
        return self.Er
    def getSd(self):
        return self.sd

    
    def getExpReturn(self, historical_returns : dict):
        """
        Finds the arithmetic mean returns from historical_returns
        """
        nan_counter = 0
        sum = 0
        n = len(historical_returns)
        mean = 0

        for val in historical_returns.values():
            # ignore NaN (Not a Number)
            if np.isnan(val):
                nan_counter+=1
                continue
            else:
                sum += val

        n = n - nan_counter
        mean = sum / n
        return mean


    def getSD(self, historical_returns : dict):
        """
        Finds the standard deviation given historical returns
        """
        nan_counter = 0
        sd = None
        n = len(historical_returns)
        total = 0

        for val in historical_returns.values():
            if np.isnan(val):
                nan_counter += 1
                continue
            else:
                total += (val - self.Er) ** 2
        
        variance = total / (n-1-nan_counter)
        sd = variance ** 0.5
        return sd


    def __str__(self):
        return f"AssetClass = [{self.name}, E(r) = {(self.Er)*100:.2f}%, sd = {self.sd:.2f}]"


class Portfolio:
    """
    Portfolios of financial products. 
    Can hold risk free assets, other portfolios or asset classes. 
    """
    name = None 
    composition = {}
    corr_matrix = None # Correlation between asset classes' returns (Pandas DataFrame)
    Er = None # E(r) Expected Return 
    sd = None # standard deviation

    def __init__(self, name : str, composition : dict, corr_matrix : object):
        self.name = name
        self.composition = composition
        self.corr_matrix = corr_matrix
        self.Er = self.computeEr()
        self.sd = self.computeSd()


    def computeEr(self):
        """
        Calculates and returns portfolio expected return as:
        Er_p = (w_1 * Er_1) + (w_2 * Er_2) + (w_3 * Er_3) + (...)

        Where:
        Er_p is the expected return of the portfolio
        w_i  is the weight of asset class i
        Er_i is the expected return of asset class i
        """
        Er_p = 0
        for a, w_i in self.composition.items():
            Er_i = a.getEr()
            Er_p += w_i * Er_i
        return Er_p


    def computeSd(self):
        """
        Calculates and returns portfolio standard deviation as:
        sqrt( ΣΣw(i)w(j)sd(i)sd(j)p(i,j) )
        """
        variance = 0
        n = len(self.composition)

        for asset_i, w_i in self.composition.items():
            for asset_j, w_j in self.composition.items():
                name_i = asset_i.getName()
                name_j = asset_j.getName()
                corr = self.corr_matrix[name_i][name_j]
                sd_i = asset_i.getSd()
                sd_j = asset_j.getSd()

                variance += w_i * w_j * corr * sd_i * sd_j

        sd = variance ** 0.5
        return sd


    def reprComposition(self):
        """
        Returns a visual representation of the composition dict
        """
        string = "{\n"
        for asset_class, w in self.composition.items():
            string += f"    {w:.0f}% : {asset_class},\n"
        string += "}"
        return string 
    

    def __str__(self):
        return f"Portfolio = [{self.name}, composition = {self.reprComposition()},\nE(r) = {self.Er}\nsd   = {self.sd}]"


def convert_portfolios_into_df(portfolios: list) -> pd.DataFrame:
    """
    Input:  A list of Portfolio objects
    Output: A pandas dataframe with tuples (name, Er, sd, reference_to_object)
    """
    # NOTE: "tuple" is used in the database meaning here, not the Python meaning 
    tuples = []
    labels = ["Name", "E(r)", "sd", "Portfolio Object"]

    for p in portfolios:
        portfolio_as_tuple = [p.name, p.Er, p.sd, p]
        tuples.append(portfolio_as_tuple)

    df = pd.DataFrame(tuples, columns=labels)
    
    return df

