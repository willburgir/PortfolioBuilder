import pandas as pd
import plotly.express as px


def create_scatter_plot(df, x, y, title: str):
    """
    USELESS?
    Probably easier to use library directly...

    Create a scatter plot using Plotly Express
    Returns the figure object
    """
    fig = px.scatter(df, x=x, y=y, title=title)
    return fig


def save_fig_as_html(fig, file_path) -> None:
    """
    Saves the figure at the provided path (including the name)
    """
    fig.write_html(file_path)

