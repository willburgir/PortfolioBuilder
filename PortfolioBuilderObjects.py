import numpy as np
import pandas as pd
from xlwings import view

DAYS_IN_YEAR   = 365
WEEKS_IN_YEAR  = 52
MONTHS_IN_YEAR = 12
YEARS_IN_YEAR  = 1

def get_num_periods_in_year(period: str) -> float:
    """
    Takes in a period as str, returns m: the number of periods in a year 
    """
    daily   = ["d", "daily", "day"]
    weekly  = ["w", "weekly", "week"]
    monthly = ["m", "monthly", "month"]
    yearly  = ["y", "yearly", "year", "annual"]

    m = None
    period = period.lower()

    if period in yearly:
        m = YEARS_IN_YEAR
    elif period in monthly:
        m = MONTHS_IN_YEAR
    elif period in weekly:
        m = WEEKS_IN_YEAR
    elif period in daily:
        m = DAYS_IN_YEAR
    else:
        print("ERROR: Provided invalid period to period_to_annual_rate()")
        print("Select from [daily, weekly, monthly, yearly]")
        exit(1)
    return m


def period_to_annual_rate(PR: float, period: str):
    """
    Converts a daily rate into annual using:
    AR = ((PR + 1)**m - 1) * 100

    Where
    AR: Annual rate in % form
    PR: Period rate in decimal form
    m: number of periods per year

    period:
    daily   -> ["d", "daily", "day"]
    weekly  -> ["w", "weekly", "week"]
    monthly -> ["m", "monthly, "month"]
    yearly  -> ["y", "yearly", "year", "annual"]

    Assumes DR is given in decimal form, not %

    Formula Source:
    https://www.fool.com/investing/how-to-invest/stocks/how-to-convert-daily-returns-to-annual-returns/#:~:text=The%20same%20equation%20can%20be,365%20%E2%80%93%201)%20x%20100.
    """ 
    m = get_num_periods_in_year(period)

    return ((PR + 1)**m - 1) * 100


def period_to_annual_sd(sd: float, period: str) -> float:
    """
    Turn period standard deviation into annual sd using square root of time rule

    NOTE
    I am coding this in the airplane without wifi... 
    If I remember correctly, the formula goes like:
        sd_annual = sd_period * sqrt(m)
    """
    m = get_num_periods_in_year(period)

    return sd * m**0.5


def convert_tickers_to_AssetClass_obj(composition: dict, asset_classes: list) -> dict:
    """
    Given 
    - A composition dict with strings as keys (tickers)
    - A list of all AssetClass objects
    Outputs a composition dict with AssetClass objects as keys
    """
    # create dict {"ticker" : AssetClass}
    ticker_to_obj = {}
    for asset_obj in asset_classes:
        ticker_to_obj[asset_obj.name] = asset_obj

    new_dict = {}
    # create new dict with obj as keys
    for ticker, weight in composition.items():
        key = ticker_to_obj[ticker]
        new_dict[key] = weight

    return new_dict


class AssetClass:
    """
    Risky asset classes with:
    expected returns as a measure of returns
    standard deviation as a measure of risk (>0)
    """
    name = None 
    historical_returns = None
    period = None
    Er = None # E(r) Expected Return 
    sd = None # Standard deviation 

    def __init__(self, name : str, historical_returns : pd.core.series.Series, period: str):
        # type validation
        if not isinstance(historical_returns, pd.core.series.Series):
            raise ValueError("Historical returns should be provided as a Pandas Series.")
        
        self.name = name
        self.historical_returns = historical_returns
        self.period = period
        self.Er = self.getPandasExpReturn()
        self.sd = self.getPandasSD()


    def getName(self):
        return self.name
    def getEr(self):
        return self.Er
    def getSd(self):
        return self.sd

    
    def getExpReturn(self, historical_returns : dict):
        """
        Finds the arithmetic mean returns from historical_returns

        NOTE 
        Deprecated, now using getPandasExpReturn 
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


    def getPandasExpReturn(self):
        """
        Finds the arithmetic mean returns from historical_returns
        """
        daily_mean = self.historical_returns.mean()
        annual_mean = period_to_annual_rate(daily_mean/100, self.period)
        return annual_mean


    def getSD(self, historical_returns : dict):
        """
        Finds the standard deviation given historical returns

        NOTE 
        Deprecated, now using getPandasSD 
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


    def getPandasSD(self):
        """
        Finds the standard deviation given historical returns
        """ 
        return period_to_annual_sd(self.historical_returns.std(), self.period)


    def __str__(self):
        return f"AssetClass = [{self.name}, E(r) = {(self.Er)*100:.2f}%, sd = {self.sd:.2f}]"


class Portfolio:
    """
    Portfolios of financial products. 
    Can hold risk free assets, other portfolios or asset classes. 

    TODO
    OPTIMIZE USING PANDAS !!!!!!
    """
    name = None 
    color = None
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


    def set_color(self, color):
        self.color = color

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


    def computePandasEr():
            """
            Hmm... TODO
            """
            return


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


    def computePandasSd():
        """
        Hmm... TODO
        """
        return


    def reprComposition(self):
        """
        Returns a visual representation of the composition dict
        """
        string = "{\n"
        for asset_class, w in self.composition.items():
            w = round(w, 2)
            w_str = f"{w:.2f}"
            string += f"    {w_str:>6}% : {asset_class},\n"
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
