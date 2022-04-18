#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 16:55:39 2021

@author: rahulkoneru
"""
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import pathlib
import math
import time
from app import app
from datetime import datetime as dt
from datetime import date as dt_date
import plotly.graph_objs as go
import numpy as np

# PATH = pathlib.Path('__file__').parent
# DATA_PATH = PATH.joinpath("../Resource Capacity Planner/datasets").resolve()
DATA_PATH = pathlib.Path("datasets/04_Resource_Capacity.xlsx").parent.resolve()
resource_list = pd.read_excel(DATA_PATH.joinpath("01_Resource_List.xlsx"), engine='openpyxl')  # List of resources
task_list = pd.read_excel(DATA_PATH.joinpath("03_Task_List.xlsx"), engine='openpyxl')  # List of Tasks
holidays = pd.read_excel(DATA_PATH.joinpath('05_Holiday_List.xlsx'), engine='openpyxl')
leaves = pd.read_excel(DATA_PATH.joinpath("06_Leave_List.xlsx"), engine='openpyxl')
resource_project = pd.read_excel(DATA_PATH.joinpath("04_Resource_Capacity.xlsx"), engine='openpyxl')
demand_agg_total = pd.read_excel(DATA_PATH.joinpath("Resource_Capacity_Planner_Deman_Aggregate_Input.xlsx"),
                                 engine='openpyxl')
project_list = pd.read_excel(DATA_PATH.joinpath("02_Project_List.xlsx"), engine='openpyxl')
time_spent = pd.read_excel(DATA_PATH.joinpath("07_Actual_Time_Spent.xlsx"), engine='openpyxl')
demand_capacity_resigns = pd.read_excel(DATA_PATH.joinpath("Demand_Capacity_Input_with_Resigns.xlsx"),
                                        engine='openpyxl')
skill_demand = pd.read_excel(DATA_PATH.joinpath("08_Skill_Demand.xlsx"), engine='openpyxl')


@app.callback(Output('tabs-content-data-entry', 'children'),
              Input('tabs-data-entry', 'value'))
def render_content(tab):
    if tab == 'resource-list':  # Layout for resource list table
        return html.Div([html.H2("Resource List", style={'padding': '25 px', 'text-align': 'center'}),
                         dash_table.DataTable(
                             id='resource-list-table',
                             columns=[{
                                 'name': '{}'.format(i),
                                 'id': '{}'.format(i),
                                 'deletable': True,
                                 'renamable': True
                             } for i in resource_list.columns],
                             data=resource_list.to_dict('records'),

                             editable=True,
                             row_deletable=True,
                             selected_columns=[],  # ids of columns that user selects
                             selected_rows=[],  # indices of rows that user selects
                             # all data is passed to the table up-front or not ('none')
                             page_action="native",
                             page_current=0,  # page number that user is on
                             page_size=10,  # number of rows visible per page
                             style_cell={  # ensure adequate header width when text is shorter than cell's text
                                 'minWidth': 95, 'maxWidth': 95, 'width': 95
                             },
                             style_data={  # overflow cells' content into multiple lines
                                 'whiteSpace': 'normal',
                                 'height': 'auto'
                             },
                             export_format='xlsx',
                             export_headers='display',
                             merge_duplicate_headers=True
                         ),

                         html.Button('Add Row', id='editing-rows-button-resource-list', n_clicks=0),
                         html.Button('Save Data', id='save-data-button-resource-list', n_clicks=0),
                         html.Div(id="output-1-resource-list", children="Press button to save changes"),
                         ])
    elif tab == 'project-list':  # Layput for Resource Project allocation table
        return html.Div([html.H2("Project List", style={'padding': '25 px', 'text-align': 'center'}),
                         dash_table.DataTable(
                             id='project-list-table',
                             columns=[{
                                 'name': '{}'.format(i),
                                 'id': '{}'.format(i),
                                 'deletable': True,
                                 'renamable': True
                             } for i in project_list.columns],
                             data=project_list.to_dict('records'),

                             editable=True,
                             row_deletable=True,
                             selected_columns=[],  # ids of columns that user selects
                             selected_rows=[],  # indices of rows that user selects
                             # all data is passed to the table up-front or not ('none')
                             page_action="native",
                             page_current=0,  # page number that user is on
                             page_size=10,  # number of rows visible per page
                             style_cell={  # ensure adequate header width when text is shorter than cell's text
                                 'minWidth': 95, 'maxWidth': 95, 'width': 95
                             },
                             style_data={  # overflow cells' content into multiple lines
                                 'whiteSpace': 'normal',
                                 'height': 'auto'
                             },
                             export_format='xlsx',
                             export_headers='display',
                             merge_duplicate_headers=True
                         ),

                         html.Button('Add Row', id='editing-rows-button-project-list', n_clicks=0),
                         html.Button('Save Data', id='save-data-button-project-list', n_clicks=0),
                         html.Div(id="output-1-project-list", children="Press button to save changes"),
                         ])

    elif tab == 'resource-project':  # Layput for Resource Project allocation table
        return html.Div([html.H2("Resource Project Allocation", style={'padding': '25 px', 'text-align': 'center'}),
                         dash_table.DataTable(
                             id='resource-project-table',
                             columns=[{
                                 'name': '{}'.format(i),
                                 'id': '{}'.format(i),
                                 'deletable': True,
                                 'renamable': True
                             } for i in resource_project.columns],
                             data=resource_project.to_dict('records'),

                             editable=True,
                             row_deletable=True,
                             selected_columns=[],  # ids of columns that user selects
                             selected_rows=[],  # indices of rows that user selects
                             # all data is passed to the table up-front or not ('none')
                             page_action="native",
                             page_current=0,  # page number that user is on
                             page_size=10,  # number of rows visible per page
                             style_cell={  # ensure adequate header width when text is shorter than cell's text
                                 'minWidth': 95, 'maxWidth': 95, 'width': 95
                             },
                             style_data={  # overflow cells' content into multiple lines
                                 'whiteSpace': 'normal',
                                 'height': 'auto'
                             },
                             export_format='xlsx',
                             export_headers='display',
                             merge_duplicate_headers=True
                         ),

                         html.Button('Add Row', id='editing-rows-button-resource-project', n_clicks=0),
                         html.Button('Save Data', id='save-data-button-resource-project', n_clicks=0),
                         html.Div(id="output-1-resource-project", children="Press button to save changes"),
                         ])
    elif tab == 'task-list':  # Layout for Task List Table
        return html.Div([html.H2("Task List", style={'padding': '25 px', 'text-align': 'center'}),
                         dash_table.DataTable(
                             id='task-list-table',
                             columns=[{
                                 'name': '{}'.format(i),
                                 'id': '{}'.format(i),
                                 'deletable': True,
                                 'renamable': True
                             } for i in task_list.columns],
                             data=task_list.to_dict('records'),

                             editable=True,
                             row_deletable=True,
                             selected_columns=[],  # ids of columns that user selects
                             selected_rows=[],  # indices of rows that user selects
                             # all data is passed to the table up-front or not ('none')
                             page_action="native",
                             page_current=0,  # page number that user is on
                             page_size=10,  # number of rows visible per page
                             style_cell={  # ensure adequate header width when text is shorter than cell's text
                                 'minWidth': 95, 'maxWidth': 95, 'width': 95
                             },
                             style_data={  # overflow cells' content into multiple lines
                                 'whiteSpace': 'normal',
                                 'height': 'auto'
                             },
                             export_format='xlsx',
                             export_headers='display',
                             merge_duplicate_headers=True
                         ),

                         html.Button('Add Row', id='editing-rows-button-task-list', n_clicks=0),
                         html.Button('Save Data', id='save-data-button-task-list', n_clicks=0),
                         html.Div(id="output-1-task-list", children="Press button to save changes"),
                         ])
    elif tab == 'leaves':  # Layout for leaves Table
        return html.Div([html.H2("Leaves", style={'padding': '25 px', 'text-align': 'center'}),
                         dash_table.DataTable(
                             id='leaves-table',
                             columns=[{
                                 'name': '{}'.format(i),
                                 'id': '{}'.format(i),
                                 'deletable': True,
                                 'renamable': True
                             } for i in leaves.columns],
                             data=leaves.to_dict('records'),

                             editable=True,
                             row_deletable=True,
                             selected_columns=[],  # ids of columns that user selects
                             selected_rows=[],  # indices of rows that user selects
                             # all data is passed to the table up-front or not ('none')
                             page_action="native",
                             page_current=0,  # page number that user is on
                             page_size=10,  # number of rows visible per page
                             style_cell={  # ensure adequate header width when text is shorter than cell's text
                                 'minWidth': 95, 'maxWidth': 95, 'width': 95
                             },
                             style_data={  # overflow cells' content into multiple lines
                                 'whiteSpace': 'normal',
                                 'height': 'auto'
                             },
                             export_format='xlsx',
                             export_headers='display',
                             merge_duplicate_headers=True
                         ),

                         html.Button('Add Row', id='editing-rows-button-leaves', n_clicks=0),
                         html.Button('Save Data', id='save-data-button-leaves', n_clicks=0),
                         html.Div(id="output-1-leaves", children="Press button to save changes"),
                         ])
    elif tab == 'holidays':  # Layout for holidays Table
        return html.Div([html.H2("Holiday List", style={'padding': '25 px', 'text-align': 'center'}),
                         dash_table.DataTable(
                             id='holidays-table',
                             columns=[{
                                 'name': '{}'.format(i),
                                 'id': '{}'.format(i),
                                 'deletable': True,
                                 'renamable': True
                             } for i in holidays.columns],
                             data=holidays.to_dict('records'),

                             editable=True,
                             row_deletable=True,
                             selected_columns=[],  # ids of columns that user selects
                             selected_rows=[],  # indices of rows that user selects
                             # all data is passed to the table up-front or not ('none')
                             page_action="native",
                             page_current=0,  # page number that user is on
                             page_size=10,  # number of rows visible per page
                             style_cell={  # ensure adequate header width when text is shorter than cell's text
                                 'minWidth': 95, 'maxWidth': 95, 'width': 95
                             },
                             style_data={  # overflow cells' content into multiple lines
                                 'whiteSpace': 'normal',
                                 'height': 'auto'
                             },
                             export_format='xlsx',
                             export_headers='display',
                             merge_duplicate_headers=True
                         ),

                         html.Button('Add Row', id='editing-rows-button-holidays', n_clicks=0),
                         html.Button('Save Data', id='save-data-button-holidays', n_clicks=0),
                         html.Div(id="output-1-holidays", children="Press button to save changes"),
                         ])
    elif tab == 'time-spent':  # Layout for Actual time spent
        return html.Div([html.H2("Actual Time Spent", style={'padding': '25 px', 'text-align': 'center'}),
                         dash_table.DataTable(
                             id='time-spent-table',
                             columns=[{
                                 'name': '{}'.format(i),
                                 'id': '{}'.format(i),
                                 'deletable': True,
                                 'renamable': True
                             } for i in time_spent.columns],
                             data=time_spent.to_dict('records'),

                             editable=True,
                             row_deletable=True,
                             selected_columns=[],  # ids of columns that user selects
                             selected_rows=[],  # indices of rows that user selects
                             # all data is passed to the table up-front or not ('none')
                             page_action="native",
                             page_current=0,  # page number that user is on
                             page_size=10,  # number of rows visible per page
                             style_cell={  # ensure adequate header width when text is shorter than cell's text
                                 'minWidth': 95, 'maxWidth': 95, 'width': 95
                             },
                             style_data={  # overflow cells' content into multiple lines
                                 'whiteSpace': 'normal',
                                 'height': 'auto'
                             },
                             export_format='xlsx',
                             export_headers='display',
                             merge_duplicate_headers=True
                         ),

                         html.Button('Add Row', id='editing-rows-button-time-spent', n_clicks=0),
                         html.Button('Save Data', id='save-data-button-time-spent', n_clicks=0),
                         html.Div(id="output-1-time-spent", children="Press button to save changes"),
                         ])


# Callback for Resource List Table


@app.callback(
    [Output('resource-list-table', 'data'),
     Output('resource-list-table', 'page_current')],
    [Input('editing-rows-button-resource-list', 'n_clicks')],
    [State('resource-list-table', 'data'),
     State('resource-list-table', 'columns')])
def add_row(n_clicks, rows, columns):
    # print(len(rows))
    page_ct = 1
    if n_clicks > 0:
        temp = pd.read_excel(DATA_PATH.joinpath('01_Resource_List.xlsx'), engine='openpyxl')
        rows = temp.to_dict('records')
        rows.append({c['id']: '' for c in columns})
        page_ct = math.ceil(len(rows) / 10)
        return rows, page_ct - 1
    else:
        temp = pd.read_excel(DATA_PATH.joinpath('01_Resource_List.xlsx'), engine='openpyxl')
        rows = temp.to_dict('records')
        return rows, page_ct - 1


@app.callback(
    [Output('output-1-resource-list', 'children')],
    [Input('save-data-button-resource-list', 'n_clicks')],
    [State('resource-list-table', 'data')])
def add_row(n_clicks, rows):
    # print(len(rows))
    if n_clicks == 0:
        raise PreventUpdate
    else:
        continue_loop = True
        while (continue_loop):
            # pd.DataFrame(rows).to_excel(DATA_PATH.joinpath('01_Resource_List.xlsx'), index=False)
            try:
                temp = pd.read_excel(DATA_PATH.joinpath('01_Resource_List.xlsx'), engine='openpyxl')
                temp2 = pd.DataFrame(rows)
                temp = temp[~(temp.Emp_ID.isin(temp2.Emp_ID))]
                temp = pd.concat([temp, pd.DataFrame(rows)], ignore_index=True)
                temp = temp.drop_duplicates()
                temp = temp.reset_index(drop=True)
                temp.to_excel(DATA_PATH.joinpath('01_Resource_List.xlsx'), index=False)
                continue_loop = False
                return ['Data Submitted']
            except:
                # print((pd.DataFrame(rows)))
                time.sleep(2)
                continue_loop = True
                return ["Data Save In Progress"]


# Callback for Project List


@app.callback(
    [Output('project-list-table', 'data'),
     Output('project-list-table', 'page_current')],
    [Input('editing-rows-button-project-list', 'n_clicks')],
    [State('project-list-table', 'data'),
     State('project-list-table', 'columns')])
def add_row(n_clicks, rows, columns):
    # print(len(rows))
    page_ct = 1
    if n_clicks > 0:
        temp = pd.read_excel(DATA_PATH.joinpath('02_Project_List.xlsx'), engine='openpyxl')
        rows = temp.to_dict('records')
        rows.append({c['id']: '' for c in columns})
        page_ct = math.ceil(len(rows) / 10)
        return rows, page_ct - 1
    else:
        temp = pd.read_excel(DATA_PATH.joinpath('02_Project_List.xlsx'), engine='openpyxl')
        rows = temp.to_dict('records')
        return rows, page_ct - 1


@app.callback(
    [Output('output-1-project-list', 'children')],
    [Input('save-data-button-project-list', 'n_clicks')],
    [State('project-list-table', 'data')])
def add_row(n_clicks, rows):
    # print(len(rows))
    if n_clicks == 0:
        raise PreventUpdate
    else:
        continue_loop = True
        while (continue_loop):
            # pd.DataFrame(rows).to_excel(DATA_PATH.joinpath('01_Resource_List.xlsx'), index=False)
            try:
                temp = pd.read_excel(DATA_PATH.joinpath('02_Project_List.xlsx'), engine='openpyxl')
                temp2 = pd.DataFrame(rows)
                temp = temp[~(temp.Emp_ID.isin(temp2.Emp_ID))]
                temp = pd.concat([temp, pd.DataFrame(rows)], ignore_index=True)
                temp = temp.drop_duplicates()
                temp = temp.reset_index(drop=True)
                temp.to_excel(DATA_PATH.joinpath('02_Project_List.xlsx'), index=False)
                continue_loop = False
                return ['Data Submitted']
            except:
                # print((pd.DataFrame(rows)))
                time.sleep(2)
                continue_loop = True
                return ["Data Save In Progress"]


# Callback for Resource to Project Allocation


@app.callback(
    [Output('resource-project-table', 'data'),
     Output('resource-project-table', 'page_current')],
    Input('editing-rows-button-resource-project', 'n_clicks'),
    [State('resource-project-table', 'data'),
     State('resource-project-table', 'columns')])
def add_row(n_clicks, rows, columns):
    # print(len(rows))
    page_ct = 1
    if n_clicks > 0:
        temp = pd.read_excel(DATA_PATH.joinpath('04_Resource_Capacity.xlsx'), engine='openpyxl')
        rows = temp.to_dict('records')
        rows.append({c['id']: '' for c in columns})
        page_ct = math.ceil(len(rows) / 10)
        return rows, page_ct - 1
    else:
        temp = pd.read_excel(DATA_PATH.joinpath('04_Resource_Capacity.xlsx'), engine='openpyxl')
        rows = temp.to_dict('records')
        return rows, page_ct - 1


@app.callback(
    [Output('output-1-resource-project', 'children')],
    [Input('save-data-button-resource-project', 'n_clicks')],
    [State('resource-project-table', 'data')])
def add_row(n_clicks, rows):
    # print(len(rows))
    if n_clicks == 0:
        raise PreventUpdate
    else:
        continue_loop = True
        while (continue_loop):
            # pd.DataFrame(rows).to_excel(DATA_PATH.joinpath('01_Resource_List.xlsx'), index=False)
            try:
                temp = pd.read_excel(DATA_PATH.joinpath('04_Resource_Capacity.xlsx'), engine='openpyxl')
                temp2 = pd.DataFrame(rows)
                temp = temp[~(temp.Emp_ID.isin(temp2.Emp_ID)) & (temp.Client.isin(
                    temp2.Client) & (temp.Engagement.isin(temp2.Engagement)))]
                temp = pd.concat([temp, pd.DataFrame(rows)], ignore_index=True)
                temp = temp.drop_duplicates()
                temp = temp.reset_index(drop=True)
                temp.to_excel(DATA_PATH.joinpath('04_Resource_Capacity.xlsx'), index=False)
                continue_loop = False
                return ['Data Submitted']
            except:
                time.sleep(2)
                continue_loop = True
                return ["Data Save In Progress"]


# Callback for Task List


@app.callback(Output('hidden-data-entry', 'children'),
              Input('backend-data-refresh-button', 'n_clicks'))
def refresh_backend(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        script_fn = 'datasets//Resource Capacity Planner Input Data Creation.py'
        exec(open(script_fn).read())
    return ["Data Refreshed"]


@app.callback(
    [Output('task-list-table', 'data'),
     Output('task-list-table', 'page_current')],
    Input('editing-rows-button-task-list', 'n_clicks'),
    [State('task-list-table', 'data'),
     State('task-list-table', 'columns')])
def add_row(n_clicks, rows, columns):
    # print(len(rows))
    page_ct = 1
    if n_clicks > 0:
        temp = pd.read_excel(DATA_PATH.joinpath('03_Task_List.xlsx'), engine='openpyxl')
        rows = temp.to_dict('records')
        rows.append({c['id']: '' for c in columns})
        page_ct = math.ceil(len(rows) / 10)
        return rows, page_ct - 1
    else:
        temp = pd.read_excel(DATA_PATH.joinpath('03_Task_List.xlsx'), engine='openpyxl')
        rows = temp.to_dict('records')
        return rows, page_ct - 1


@app.callback(
    [Output('output-1-task-list', 'children')],
    [Input('save-data-button-task-list', 'n_clicks')],
    [State('task-list-table', 'data')])
def add_row(n_clicks, rows):
    # print(len(rows))
    if n_clicks == 0:
        raise PreventUpdate
    else:
        continue_loop = True
        while (continue_loop):
            # pd.DataFrame(rows).to_excel(DATA_PATH.joinpath('01_Resource_List.xlsx'), index=False)
            try:
                temp = pd.read_excel(DATA_PATH.joinpath('03_Task_List.xlsx'), engine='openpyxl')
                temp2 = pd.DataFrame(rows)
                temp = temp[~(temp.Emp_ID.isin(temp2.Emp_ID)) & (temp.Client.isin(
                    temp2.Client) & (temp.Engagement.isin(temp2.Engagement)))]
                temp = pd.concat([temp, pd.DataFrame(rows)], ignore_index=True)
                temp = temp.drop_duplicates()
                temp = temp.reset_index(drop=True)
                temp.to_excel(DATA_PATH.joinpath('03_Task_List.xlsx'), index=False)
                continue_loop = False
                return ['Data Submitted']
            except:
                time.sleep(2)
                continue_loop = True
                return ["Data Save In Progress"]


# Call back for leave table


@app.callback(
    [Output('leaves-table', 'data'),
     Output('leaves-table', 'page_current')],
    Input('editing-rows-button-leaves', 'n_clicks'),
    [State('leaves-table', 'data'),
     State('leaves-table', 'columns')])
def add_row(n_clicks, rows, columns):
    # print(len(rows))
    page_ct = 1
    if n_clicks > 0:
        temp = pd.read_excel(DATA_PATH.joinpath('06_Leave_List.xlsx'), engine='openpyxl')
        rows = temp.to_dict('records')
        rows.append({c['id']: '' for c in columns})
        page_ct = math.ceil(len(rows) / 10)
        return rows, page_ct - 1
    else:
        temp = pd.read_excel(DATA_PATH.joinpath('06_Leave_List.xlsx'), engine='openpyxl')
        rows = temp.to_dict('records')
        return rows, page_ct - 1


@app.callback(
    [Output('output-1-leaves', 'children')],
    [Input('save-data-button-leaves', 'n_clicks')],
    [State('leaves-table', 'data')])
def add_row(n_clicks, rows):
    # print(len(rows))
    if n_clicks == 0:
        raise PreventUpdate
    else:
        continue_loop = True
        while (continue_loop):
            # pd.DataFrame(rows).to_excel(DATA_PATH.joinpath('01_Resource_List.xlsx'), index=False)
            try:
                temp = pd.read_excel(DATA_PATH.joinpath('06_Leave_List.xlsx'), engine='openpyxl')
                temp2 = pd.DataFrame(rows)
                temp = temp[~(temp.Emp_ID.isin(temp2.Emp_ID))]
                temp = pd.concat([temp, pd.DataFrame(rows)], ignore_index=True)
                temp = temp.drop_duplicates()
                temp = temp.reset_index(drop=True)
                temp.to_excel(DATA_PATH.joinpath('06_Leave_List.xlsx'), index=False)
                continue_loop = False
                return ['Data Submitted']
            except:
                time.sleep(2)
                continue_loop = True
                return ["Data Save In Progress"]


# Callback for holiday Table


@app.callback(
    [Output('holidays-table', 'data'),
     Output('holidays-table', 'page_current')],
    Input('editing-rows-button-holidays', 'n_clicks'),
    [State('holidays-table', 'data'),
     State('holidays-table', 'columns')])
def add_row(n_clicks, rows, columns):
    # print(len(rows))
    page_ct = 1
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
        page_ct = math.ceil(len(rows) / 10)
    return rows, page_ct - 1


@app.callback(
    [Output('output-1-holidays', 'children')],
    [Input('save-data-button-holidays', 'n_clicks')],
    [State('holidays-table', 'data')])
def add_row(n_clicks, rows):
    # print(len(rows))
    if n_clicks == 0:
        raise PreventUpdate
    else:
        pd.DataFrame(rows).to_excel(DATA_PATH.joinpath('05_Holiday_List.xlsx'), index=False)
        return ['Data Submitted']


# Callback for the actual time spent

@app.callback(
    [Output('output-1-time-spent', 'children')],
    [Input('save-data-button-time-spent', 'n_clicks')],
    [State('time-spent-table', 'data')])
def add_row(n_clicks, rows):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        continue_loop = True
        while (continue_loop):
            # pd.DataFrame(rows).to_excel(DATA_PATH.joinpath('01_Resource_List.xlsx'), index=False)
            try:
                temp = pd.read_excel(DATA_PATH.joinpath('07_Actual_Time_Spent.xlsx'), engine='openpyxl')
                temp2 = pd.DataFrame(rows)
                temp = temp[~(temp.Emp_ID.isin(temp2.Emp_ID)) & (temp.Task.isin(
                    temp2.Task) & (temp.Date.isin(temp2.Date)))]
                temp = pd.concat([temp, pd.DataFrame(rows)], ignore_index=True)
                temp = temp.drop_duplicates()
                temp = temp.reset_index(drop=True)
                temp.to_excel(DATA_PATH.joinpath('07_Actual_Time_Spent.xlsx'), index=False)
                continue_loop = False
                return ['Data Submitted']
            except:
                time.sleep(2)
                continue_loop = True
                return ["Data Save In Progress"]


@app.callback(
    [Output('time-spent-table', 'data'),
     Output('time-spent-table', 'page_current')],
    Input('editing-rows-button-time-spent', 'n_clicks'),
    [State('time-spent-table', 'data'),
     State('time-spent-table', 'columns')])
def add_row(n_clicks, rows, columns):
    # print(len(rows))
    page_ct = 1
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
        page_ct = math.ceil(len(rows) / 10)
    return rows, page_ct - 1


pd.read_excel(DATA_PATH.joinpath("07_Actual_Time_Spent.xlsx"), engine='openpyxl')


# Demand Capacity Graph
@app.callback(
    Output('demand_graph', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('client_name_dropdown', 'value'),
     Input('engagement_dropdown', 'value'),
     Input('emp_dropdown', 'value')])
def chart_data(start_date, end_date, name_client, name_engagement, name_emp):
    dff = demand_agg_total
    if start_date is not None:
        start_date_object = dt.fromisoformat(start_date)
        dff = dff[dff.Date >= start_date_object]
    if end_date is not None:
        end_date_object = dt.fromisoformat(end_date)
        dff = dff[dff.Date <= end_date_object]
    if name_client is not None:
        dff = dff[dff.Client == name_client]
    if name_engagement is not None:
        dff = dff[dff.Engagement.str.contains("|".join(name_engagement))]
    if name_emp is not None:
        dff["Emp_ID"] = dff["Emp_ID"].astype(str)
        dff = dff[dff["Emp_ID"].str.contains("|".join(map(str, name_emp)))]
    df = dff.groupby(['Day_Name']).agg({
        'Day_Demand': 'sum', 'Holiday_Demand': 'sum', 'Leave_Capacity': 'sum', 'Day_Capacity': 'sum'}, as_index=False)

    df.reset_index(inplace=True)

    df['Day_Name'] = pd.Categorical(df["Day_Name"], ["Mon", "Tue", "Wed", "Thu", "Fri",
                                                     "Sat", "Sun", "Total"])

    df["Capacity_Actual"] = df["Day_Capacity"] + df["Leave_Capacity"]
    df = df.sort_values("Day_Name")
    df = df[df["Day_Name"] != "Total"]
    colors_demand = ['#2d98da', ] * 7
    colors_capacity = ['#20bf6b', ] * 7
    trace1 = go.Bar(x=df["Day_Name"], y=df["Day_Demand"], name="Demand",
                    orientation='v', width=.8, marker_color=colors_demand)

    trace2 = go.Bar(x=df["Day_Name"], y=df["Day_Capacity"],
                    name="Capacity", orientation='v', width=.5, opacity=0.5, marker_color=colors_capacity)

    chart_data_bar = [trace1, trace2]
    layout = go.Layout(barmode='overlay',
                       xaxis=dict(
                           title="Days", showline=True, linewidth=2, linecolor='black'
                       ),
                       yaxis=dict(
                           title="Resource (Hours)", showline=True, linewidth=2, linecolor='black'
                       ),
                       title={'text': "Demand vs Capacity",
                              'y': 0.9,
                              'x': 0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                       plot_bgcolor="#ffffff",
                       legend=dict(
                           xanchor='right',
                           x=1.2,
                           orientation='h',
                           yanchor='bottom',
                           y=1.02,
                           traceorder="reversed",
                           title_font_family="Times New Roman",
                           font=dict(
                               family="Courier",
                               size=10,
                               color="black"
                           ),
                           bgcolor="#ffffff",
                           bordercolor="Black",
                           borderwidth=2
                       ))
    bar_chart = go.Figure(data=chart_data_bar, layout=layout)

    # bar_chart = px.bar(x=df["Day_Name"], y=df["Demand"])
    return bar_chart


@app.callback(
    [Output('team-total-demand', 'children'),
     Output('team-total-capacity', 'children'),
     Output('team-excess-capacity', 'children'),
     Output('team-total-leave-capacity', 'children'),
     Output('team-leave-coverage', 'children'),
     Output('team-util-status', 'children')],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('client_name_dropdown', 'value'),
     Input('engagement_dropdown', 'value'),
     Input('emp_dropdown', 'value')])
def demand_box(start_date, end_date, name_client, name_engagement, name_emp):
    dff = demand_agg_total
    if start_date is not None:
        start_date_object = dt.fromisoformat(start_date)
        dff = dff[dff.Date >= start_date_object]
    if end_date is not None:
        end_date_object = dt.fromisoformat(end_date)
        dff = dff[dff.Date <= end_date_object]
    if name_client is not None:
        dff = dff[dff.Client == name_client]
    if name_engagement is not None:
        dff = dff[dff.Engagement.str.contains("|".join(name_engagement))]
    if name_emp is not None:
        dff["Emp_ID"] = dff["Emp_ID"].astype(str)
        dff = dff[dff["Emp_ID"].str.contains("|".join(map(str, name_emp)))]
    df = dff.groupby(['Day_Name']).agg({
        'Day_Demand': 'sum', 'Holiday_Demand': 'sum', 'Leave_Capacity': 'sum', 'Day_Capacity': 'sum'}, as_index=False)
    df.reset_index(inplace=True)
    demand = sum(df.loc[df["Day_Name"] != "Total", "Day_Demand"])
    capacity = round(sum(df.loc[df["Day_Name"] != "Total", "Day_Capacity"]), 0)
    leave = sum(df.loc[df["Day_Name"] != "Total", "Leave_Capacity"])

    util_per_cent = str(round((demand / capacity) * 100, 0)) + " %"
    if capacity - demand > 0:
        util_status = "Under Utilized"
    elif capacity == demand:
        util_status = "Fully Utilized"
    else:
        util_status = "Over Utilized"
    if (capacity - demand + leave) >= 0:
        leave_coverage = 'Yes'
    else:
        leave_coverage = 'No'
    return demand, capacity, (capacity - demand), leave, leave_coverage, util_status


@app.callback(Output('engagement_dropdown', 'options'),
              Input('client_name_dropdown', 'value'))
def engagment_dropdown_list(name_client):
    df = demand_agg_total
    if name_client is not None:
        df = df[df['Client'] == name_client]
    engagement_list = [{'label': i, 'value': i} for i in df.Engagement.unique()]
    return engagement_list


@app.callback(Output('emp_dropdown', 'options'),
              [Input('client_name_dropdown', 'value'),
               Input('engagement_dropdown', 'value')])
def emp_id_dropdownlist(name_client, name_engagement):
    df = demand_agg_total
    emp_list = [{'label': i, 'value': i} for i in df.Emp_ID.unique()]
    if name_client is not None:
        df = df[df['Client'] == name_client]
        emp_list = [{'label': i, 'value': i} for i in df.Emp_ID.unique()]
    if name_engagement is not None:
        df = df[df.Engagement.str.contains("|".join(name_engagement))]
        emp_list = [{'label': i, 'value': i} for i in df.Emp_ID.unique()]
    return emp_list


@app.callback(
    [Output('emp-total-demand', 'children'),
     Output('emp-total-capacity', 'children'),
     Output('emp_excess_capacity', 'children'),
     Output('emp_leave_capacity', 'children'),
     Output('emp-util-per-cent', 'children'),
     Output('emp-util-status', 'children'),
     Output('emp_capacity_graph', 'figure')],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('client_name_dropdown', 'value'),
     Input('engagement_dropdown', 'value')])
def excess_capacity_chart(start_date, end_date, name_client, name_engagement):
    dff = demand_agg_total
    # start_date_object = dt_date.fromisoformat(start_date)
    # end_date_object = dt_date.fromisoformat(end_date)
    if start_date is not None:
        start_date_object = dt.fromisoformat(start_date)
        dff = dff.loc[dff.Date >= start_date_object,]
    if end_date is not None:
        end_date_object = dt.fromisoformat(end_date)
        print("en Dtae" + str(end_date_object))
        dff = dff.loc[dff.Date <= end_date_object]
        print(dff)
        print(sum(dff['Excess_Capacity']))

    if name_client is not None:
        dff = dff.loc[dff.Client == name_client,]
    if name_engagement is not None:
        dff = dff.loc[dff.Engagement.str.contains("|".join(name_engagement)),]
    # print(dff)
    # print("st Dtae" + str(start_date_object))
    # print("en Dtae" + str(end_date_object))
    # print("clisrnt" + name_client)

    dff = dff[dff['Day_Name'] != "Total"]
    df = dff.groupby(['Emp_ID']).agg({
        'Day_Demand': 'sum', 'Holiday_Demand': 'sum', 'Leave_Capacity': 'sum', 'Day_Capacity': 'sum',
        'Excess_Capacity': 'sum'}, as_index=False)

    df.reset_index(inplace=True)

    df["Excess_Capacity_Actual"] = df["Excess_Capacity"] + df["Leave_Capacity"]
    # df['Day_Name'] = pd.Categorical(df["Day_Name"], ["Mon", "Tue", "Wed", "Thu", "Fri",
    #                                                 "Sat", "Sun", "Total"])
    # df = df.sort_values("Day_Name")

    # dff = df[df['Day_Name'] != "Total"]
    df['Emp_ID'] = df["Emp_ID"].astype(str)
    # dff = dff.groupby(['Emp_ID']).agg({
    #   'Day_Demand': 'sum', 'Holiday_Demand': 'sum', 'Leave_Capacity': 'sum', 'Day_Capacity': 'sum', 'Excess_Capacity': 'sum', 'Excess_Capacity_Actual': 'sum'}, as_index=False)

    # dff.reset_index(inplace=True)
    df['Bar_Color'] = np.where(df["Excess_Capacity"] < 0, "#ee5253", "#10ac84")
    df['Bar_Legend'] = np.where(df["Excess_Capacity"] < 0, "Over Utilized", "Under Utilized")
    dff1 = df.loc[df['Excess_Capacity'] < 0,]
    dff2 = df.loc[df['Excess_Capacity'] >= 0,]

    fig = go.Bar(x=df["Emp_ID"], y=df["Excess_Capacity_Actual"],
                 marker_color=df['Bar_Color'])
    trace1 = go.Bar(x=dff1["Emp_ID"], y=dff1["Excess_Capacity_Actual"], name='Over Utilized',
                    orientation='v', width=.8, marker_color="#ee5253")
    trace2 = go.Bar(x=dff2["Emp_ID"], y=dff2["Excess_Capacity_Actual"], name='Under Utilized',
                    orientation='v', width=.8, marker_color="#10ac84")

    chart_data_bar = [trace1, trace2]
    layout = go.Layout(barmode='group',
                       xaxis=dict(
                           title="Employee ID",
                           showline=True, linewidth=2, linecolor='black'
                       ),
                       yaxis=dict(
                           title="Resource (Hours)", showline=True, linewidth=2, linecolor='black',
                           zeroline=True, zerolinewidth=2, zerolinecolor='red'
                       ),
                       title={'text': "Excess Capacity by Employee Considering Leaves",
                              'y': 0.9,
                              'x': 0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                       plot_bgcolor="#ffffff",
                       legend=dict(
                           xanchor='right',
                           x=1.2,
                           orientation='h',
                           yanchor='bottom',
                           y=1.02,
                           traceorder="reversed",
                           title_font_family="Times New Roman",
                           font=dict(
                               family="Courier",
                               size=10,
                               color="black"
                           ),
                           bgcolor="#ffffff",
                           bordercolor="Black",
                           borderwidth=2
                       )

                       )
    bar_chart = go.Figure(data=chart_data_bar, layout=layout)

    emp_demand = sum(df['Day_Demand'])
    emp_capacity = round(sum(df['Day_Capacity']), 0)
    emp_excess_capacity = round(sum(df['Excess_Capacity']), 0)
    emp_Atcual_availability = sum(df['Excess_Capacity']) + sum(df['Leave_Capacity'])
    emp_leave = sum(df['Leave_Capacity'])
    if emp_capacity > 0:
        emp_util_per_cent = str(round((emp_demand / emp_capacity) * 100, 0)) + " %"
    else:
        emp_util_per_cent = "--%"
    if emp_capacity - emp_demand > 0:
        emp_util_status = "Under Utilized"
    elif emp_capacity == emp_demand:
        emp_util_status = "Fully Utilized"
    else:
        emp_util_status = "Over Utilized"

    return emp_demand, emp_capacity, emp_excess_capacity, emp_leave, emp_util_per_cent, emp_util_status, bar_chart


# Callbacks for Status by Projects

@app.callback(Output('engagement_dropdown-project-status', 'options'),
              Input('client_name_dropdown-project-status', 'value'))
def engagment_dropdown_list_project_status(name_client):
    df = demand_agg_total
    if name_client is not None:
        df = df[df['Client'] == name_client]
    engagement_list = [{'label': i, 'value': i} for i in df.Engagement.unique()]
    return engagement_list


@app.callback(
    Output('status-by-project', 'figure'),
    [Input('my-date-picker-range-project-status', 'start_date'),
     Input('my-date-picker-range-project-status', 'end_date'),
     Input('client_name_dropdown-project-status', 'value'),
     Input('engagement_dropdown-project-status', 'value')])
def chart_data(start_date, end_date, name_client, name_engagement):
    dff = demand_agg_total
    if start_date is not None:
        start_date_object = dt.fromisoformat(start_date)
        dff = dff[dff.Date >= start_date_object]
    if end_date is not None:
        end_date_object = dt.fromisoformat(end_date)
        dff = dff[dff.Date <= end_date_object]
    if name_client is not None:
        dff = dff[dff.Client == name_client]
    if name_engagement is not None:
        dff = dff[dff.Engagement.str.contains("|".join(name_engagement))]

    dff = dff[dff["Day_Name"] != "Total"]
    dff['Project_Title'] = dff["Client"] + " - " + dff["Engagement"]

    df = dff.groupby(['Client', 'Engagement', "Project_Title"]).agg({
        'Day_Demand': 'sum', 'Holiday_Demand': 'sum', 'Leave_Capacity': 'sum', 'Day_Capacity': 'sum'}, as_index=False)

    df.reset_index(inplace=True)

    df["Capacity_Actual"] = df["Day_Capacity"] + df["Leave_Capacity"]
    colors_demand = ['#2d98da', ] * len(df)
    colors_capacity = ['#20bf6b', ] * len(df)
    trace1 = go.Bar(x=df["Project_Title"], y=df["Day_Demand"], name="Demand",
                    orientation='v', width=.8, marker_color=colors_demand)

    trace2 = go.Bar(x=df["Project_Title"], y=df["Day_Capacity"],
                    name="Capacity", orientation='v', width=.5, opacity=0.5, marker_color=colors_capacity)

    chart_data_bar = [trace1, trace2]
    layout = go.Layout(barmode='overlay',
                       xaxis=dict(
                           title="Engagement", showline=True, linewidth=2, linecolor='black'
                       ),
                       yaxis=dict(
                           title="Resource (Hours)", showline=True, linewidth=2, linecolor='black'
                       ),
                       title={'text': "Resource Utlization Status by Project",
                              'y': 0.9,
                              'x': 0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                       plot_bgcolor="#ffffff",
                       legend=dict(
                           xanchor='right',
                           x=1.2,
                           orientation='h',
                           yanchor='bottom',
                           y=1.02,
                           traceorder="reversed",
                           title_font_family="Times New Roman",
                           font=dict(
                               family="Courier",
                               size=10,
                               color="black"
                           ),
                           bgcolor="#ffffff",
                           bordercolor="Black",
                           borderwidth=2
                       ))
    bar_chart = go.Figure(data=chart_data_bar, layout=layout)

    # bar_chart = px.bar(x=df["Day_Name"], y=df["Demand"])
    return bar_chart


@app.callback(
    Output('status-by-project-with-resigns', 'figure'),
    [Input('my-date-picker-range-project-status', 'start_date'),
     Input('my-date-picker-range-project-status', 'end_date'),
     Input('client_name_dropdown-project-status', 'value'),
     Input('engagement_dropdown-project-status', 'value')])
def chart_data(start_date, end_date, name_client, name_engagement):
    dff = demand_capacity_resigns
    if start_date is not None:
        start_date_object = dt.fromisoformat(start_date)
        dff = dff[dff.Date >= start_date_object]
    if end_date is not None:
        end_date_object = dt.fromisoformat(end_date)
        dff = dff[dff.Date <= end_date_object]
    if name_client is not None:
        dff = dff[dff.Client == name_client]
    if name_engagement is not None:
        dff = dff[dff.Engagement.str.contains("|".join(name_engagement))]

    dff = dff[dff["Day_Name"] != "Total"]
    dff['Project_Title'] = dff["Client"] + " - " + dff["Engagement"]

    dff['Exit Date'] = np.where(dff['Exit Date'] == 0, "2030-11-28 00:00:00", dff['Exit Date'])
    dff['Exit Date'] = pd.to_datetime(dff['Exit Date'])
    dff['Resign_Status'] = np.where(dff['Exit Date'] >= dff['Date'], 1, 0)
    dff['Backup_Fullfilled_Demand'] = np.where(
        dff['Resign_Status'] == 1, dff['Excess_Capacity'] - dff['Day_Demand'], 0)

    df = dff.groupby(['Client', 'Engagement', "Project_Title", ]).agg({
        'Day_Demand': 'sum', 'Holiday_Demand': 'sum', 'Leave_Capacity': 'sum', 'Day_Capacity': 'sum',
        'Backup_Fullfilled_Demand': 'sum', 'Excess_Capacity': 'sum'}, as_index=False)

    df.reset_index(inplace=True)

    df["Capacity_Actual"] = df["Day_Capacity"] + df["Leave_Capacity"]
    df['Colors'] = np.where((df['Leave_Capacity'] < 0) & (df['Excess_Capacity'] >= 0), "#27ae60",
                            np.where((df['Leave_Capacity'] < 0) &
                                     (df['Backup_Fullfilled_Demand'] >= 0), "#27ae60", "#d63031"))
    df['Colors'] = np.where((df['Backup_Fullfilled_Demand'] < 0) & (
            df['Day_Capacity'] == 0), "#fdcb6e", df['Colors'])

    df['Status'] = np.where(df['Colors'] == "#27ae60", "Demand Met",
                            np.where(df['Colors'] == "#e67e22", "Demand Not Met - Resource Resign",
                                     "Demand Not Met"))
    # colors_demand=['#2d98da', ] * len(df)
    # colors_capacity = ['#20bf6b', ] * len(df)
    trace1 = go.Bar(x=df["Project_Title"], y=df["Excess_Capacity"],
                    orientation='v', width=.8, marker_color=df['Colors'])

    # trace2 = go.Bar(x=df["Project_Title"], y=df["Day_Capacity"],
    #                name="Capacity", orientation='v', width=.5, opacity=0.5, marker_color=colors_capacity)

    chart_data_bar = [trace1]
    layout = go.Layout(barmode='overlay',
                       xaxis=dict(
                           title="Engagement", showline=True, linewidth=2, linecolor='black'
                       ),
                       yaxis=dict(
                           title="Resource (Hours)", showline=True, linewidth=2, linecolor='black'
                       ),
                       title={'text': "Resource Utlization Status by Project",
                              'y': 0.9,
                              'x': 0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                       plot_bgcolor="#ffffff",
                       legend=dict(
                           xanchor='right',
                           x=1.2,
                           orientation='h',
                           yanchor='bottom',
                           y=1.02,
                           traceorder="reversed",
                           title_font_family="Times New Roman",
                           font=dict(
                               family="Courier",
                               size=10,
                               color="black"
                           ),
                           bgcolor="#ffffff",
                           bordercolor="Black",
                           borderwidth=2
                       ))
    bar_chart = go.Figure(data=chart_data_bar, layout=layout)

    # bar_chart = px.bar(x=df["Day_Name"], y=df["Demand"])
    return bar_chart


# Call back function for Skills most required within Tredence
@app.callback(Output('skills-most-required', 'figure'),
              [Input('skill-dropdown', 'value'),
               Input('my-date-picker-range-skill-search', 'start_date'),
               Input('my-date-picker-range-skill-search', 'end_date')])
def skill_search_chart(skills_selected, start_date, end_date):
    df = skill_demand
    if start_date is not None:
        start_date_object = dt.fromisoformat(start_date)
        df = df[df.Task_Start_Date >= start_date_object]
    if end_date is not None:
        end_date_object = dt.fromisoformat(end_date)
        df = df[df.Task_End_Date <= end_date_object]
    # if skills_selected is not None:
    #     df = df[df['Skills'].str.contains("|".join(skills_selected))]
    df = df.groupby('Skills', as_index=False).agg({'Total_Task_Effort': 'sum'})
    trace1 = go.Bar(x=df['Skills'],
                    y=df['Total_Task_Effort'],
                    orientation='v')
    chart_data_bar = [trace1]
    layout = go.Layout(
        xaxis=dict(
            title="Skills", showline=True, linewidth=2, linecolor='black'
        ),
        yaxis=dict(
            title="Demand (Hours)", showline=True, linewidth=2, linecolor='black'
        ),
        title={'text': "Skill Demand in Hours",
               'y': 0.9,
               'x': 0.5,
               'xanchor': 'center',
               'yanchor': 'top'},
        plot_bgcolor="#ffffff",
    )
    bar_chart = go.Figure(data=chart_data_bar, layout=layout)
    return bar_chart


# Call back function for the skill search chart
@app.callback(Output('skills-search-mitigation', 'figure'),
              [Input('skill-dropdown', 'value'),
               Input('my-date-picker-range-skill-search', 'start_date'),
               Input('my-date-picker-range-skill-search', 'end_date')])
def skill_search_mitigation_chart(skills_selected, start_date, end_date):
    df = skill_demand
    df2 = demand_agg_total
    df2 = df2[df2['Day_Name'] != 'Total']
    if start_date is not None:
        start_date_object = dt.fromisoformat(start_date)
        df = df[df.Task_Start_Date >= start_date_object]
        df2 = df2[df2.Date >= start_date_object]
    if end_date is not None:
        end_date_object = dt.fromisoformat(end_date)
        df = df[df.Task_End_Date <= end_date_object]
        df2 = df2[df2.Date <= end_date_object]
    if skills_selected is not None:
        df = df[df['Skills'].str.contains("|".join(skills_selected))]
    df = df.groupby(['Emp_ID', 'Skills'], as_index=False).agg({'Total_Task_Effort': 'sum'})
    df = pd.merge(resource_list,
                  df,
                  how='left',
                  on='Emp_ID')
    df['Total_Task_Effort'] = df['Total_Task_Effort'].fillna(0)

    demand_resource = df2.groupby(['Emp_ID'], as_index=False).agg({'Excess_Capacity': 'sum',
                                                                   'Day_Capacity': 'sum',
                                                                   'Day_Demand': 'sum'})
    df2 = pd.merge(demand_resource,
                   resource_list,
                   how='inner',
                   on='Emp_ID')

    if skills_selected is not None:
        df2 = df2[df2['Skill Set'].str.upper().str.contains("|".join(skills_selected))]

    trace = go.Bar(x=df2['Emp_ID'].astype(str),
                   y=df2['Excess_Capacity'],
                   orientation='v')
    layout = go.Layout(barmode='overlay',
                       xaxis=dict(
                           title="Employee ID", showline=True, linewidth=2, linecolor='black'
                       ),
                       yaxis=dict(
                           title="Excess Capacity (Hours)", showline=True, linewidth=2, linecolor='black'
                       ),
                       title={'text': "Excess Capacity by Resource",
                              'y': 0.9,
                              'x': 0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                       plot_bgcolor="#ffffff",
                       )
    chart_data_bar = [trace]

    bar_chart = go.Figure(data=chart_data_bar, layout=layout)
    return bar_chart


# This is a callback function for the infoboxes in Skill Search Tab
@app.callback([Output('selected-skill-demand', 'children'),
               Output('selected-skill-capacity', 'children'),
               Output('selected-skill-excess-capacity', 'children'),
               Output('selected-skill-mitigation-action', 'children')],
              [Input('skill-dropdown', 'value'),
               Input('my-date-picker-range-skill-search', 'start_date'),
               Input('my-date-picker-range-skill-search', 'end_date')])
def skill_search_mitigation_chart(skills_selected, start_date, end_date):
    df = skill_demand
    df2 = demand_agg_total
    df2 = df2[df2['Day_Name']!= 'Total']
    if start_date is not None:
        start_date_object = dt.fromisoformat(start_date)
        df = df[df.Task_Start_Date >= start_date_object]
        df2 = df2[df2.Date >= start_date_object]
    if end_date is not None:
        end_date_object = dt.fromisoformat(end_date)
        df = df[df.Task_End_Date <= end_date_object]
        df2 = df2[df2.Date <= end_date_object]
    if skills_selected is not None:
        df = df[df['Skills'].str.contains("|".join(skills_selected))]
    df = df.groupby(['Emp_ID', 'Skills'], as_index=False).agg({'Total_Task_Effort': 'sum'})
    df = pd.merge(resource_list,
                  df,
                  how='left',
                  on='Emp_ID')
    df['Total_Task_Effort'] = df['Total_Task_Effort'].fillna(0)

    demand_resource = df2.groupby(['Emp_ID'], as_index=False).agg({'Excess_Capacity': 'sum',
                                                                   'Day_Capacity': 'sum',
                                                                   'Day_Demand': 'sum'})
    df2 = pd.merge(demand_resource,
                   resource_list,
                   how='inner',
                   on='Emp_ID')

    if skills_selected is not None:
        df2 = df2[df2['Skill Set'].str.upper().str.contains("|".join(skills_selected))]

    # Selected Skill Demand
    selected_skill_demand = round(df2['Day_Demand'].sum(), 0)
    # Selected Skill excess capacity
    selected_skill_excess_capacity = round(df2['Excess_Capacity'].sum(), 0)
    # Selected Skill capacity
    selected_skill_capacity = round(df2['Day_Capacity'].sum(), 0)


    # Mitigation Action for selected skill
    if (selected_skill_excess_capacity > 0) & (any(df2['Excess_Capacity'] < 0)):
        mitigation_action = 'Balancing'
    elif (selected_skill_excess_capacity <= 0):
        mitigation_action = 'Hiring'
    elif (selected_skill_excess_capacity > 0) & (all(df2['Excess_Capacity'] >0 )):
        mitigation_action = 'Underutilized'
    else:
        mitigation_action = 'No Action'
    return selected_skill_demand, selected_skill_capacity, selected_skill_excess_capacity, mitigation_action
