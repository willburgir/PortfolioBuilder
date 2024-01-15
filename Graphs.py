import PortfolioBuilderObjects as obj
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



def get_scatter_plot(df: pd.DataFrame, title = "Scatter Plot"):
    """
    Given a pandas DataFrame of portfolios, creates a graph plotting them with:
    x-axis : E(r)
    y-axis : sd

    Returns the figure object (type from Plotly Express)
    """
    labels = {
        "sd" : "Standard Deviation",
        "E(r)" : "Expected Return"
    }
    figure = px.scatter(df, x="sd", y="E(r)", title=title, labels=labels,  color_discrete_sequence=["grey"], opacity=0.5)
    figure.update_layout({'plot_bgcolor': "white"})
    return figure


def add_CAL(figure, df, rf) -> obj.Portfolio:
    """
    Plots the Capital Allocation Line onto the scatter plot provided into the figure parameter

    Returns:
    1. The updated figure (scatter plot) object
    2. The optimal portfolio as a Portfolio object
    """
    SHARPE = "Sharpe"
    P_OBJ  = "Portfolio Object"
    # 1. Find max Sharpe 
    max_index = df[SHARPE].idxmax()
    optimal_portfolio = df.loc[max_index][P_OBJ]
    
    # Highlight the optimal portfolio (max sharpe) and Risk Free point
    figure.add_trace(go.Scatter(x = [optimal_portfolio.sd], y = [optimal_portfolio.Er], mode = 'markers', name = 'Optimal Portfolio', marker = dict(size=[25], color = 'green')))
    figure.add_trace(go.Scatter(x = [0], y = [rf], mode = 'markers', name = 'Risk Free Asset', marker = dict(size=[25], color = 'lightblue')))


    # Draw CAL
    cal = (go.Scatter(x = [0, optimal_portfolio.sd], y = [rf, optimal_portfolio.Er], mode = 'lines', name = "Capital Allocation Line (CAL)"))
    cal.line.color = 'blue'  # Set line color
    cal.line.width = 3      # Set line width
    figure.add_trace(cal)


    return figure, optimal_portfolio


def add_user_portfolios(figure, portfolios):
    """
    Plots the user portfolios on the Scatter plot figure
    Returns the updated figure
    """
    for p in portfolios:
        figure.add_trace(go.Scatter(x = [p.sd], y = [p.Er], mode = 'markers', name = p.name, marker = dict(size=[25], color = p.color)))

    return figure


def save_fig_as_html(fig, file_path) -> None:
    """
    Saves the figure at the provided path (including the name)
    """
    fig.write_html(file_path)

