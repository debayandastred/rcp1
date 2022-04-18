from dash import dcc
from dash import html
from dash import dash_table

from datetime import datetime as dt
import plotly.graph_objs as go
import pathlib
import pandas as pd
import os

# get relative data folder
PATH = pathlib.Path().parent
DATA_PATH = PATH.joinpath("../Resource Capacity Planner/datasets/").resolve()
#DATA_PATH2 = os.path.abspath("../Resource Capacity Planner/datasets/")
DATA_PATH3 = pathlib.Path("datasets/04_Resource_Capacity.xlsx").parent.resolve()
#print(PATH)
print(DATA_PATH)
#print(DATA_PATH2)
print(DATA_PATH3)
