# -*- coding: utf-8 -*-
'''
# MAT-tools: Tools for Multiple Aspect Trajectory Data Mining \[MAT-Tools Framework\]

The present application offers a set of tools, to support the user in the data mining and analysis tasks for multiple aspect trajectories. It integrates into a unique platform the fragmented approaches available for multiple aspects trajectories and in general for multidimensional sequence classification into a unique web-based and python library system.

Created on Dec, 2021
Copyright (C) 2021+, License GPL Version 3 or superior (see LICENSE file)

@author: Tarlis Portela
'''
import os
from pathlib import Path
#import configparser
#config = configparser.ConfigParser()
#config.read('matview/pyproject.toml')

# Server Config
#HOST = '0.0.0.0'
HOST = '127.0.0.1'
PORT = 8050
DEBUG = True

VERSION = '1.0' #config['project']['version'].replace("'", "")
PACKAGE_NAME = 'matview' #config['project']['name'].replace("'", "")

DATA_PATH = '../sample'    
EXP_PATH  = '../../results'
README    = PACKAGE_NAME+'/README.md'

ROOT = str(Path(__file__).parents[2])

ASSETS_ROUTE = os.path.join(ROOT, PACKAGE_NAME)+'/assets/'
WEB_ROUTE = os.path.join(ROOT, PACKAGE_NAME)+'/web'

RESULTS_FILE    = ASSETS_ROUTE+'data/experimental_history.csv'

# page_title = 'Tarlis\'s Multiple Aspect Trajectory Analysis'
page_title = 'MAT-Tools Framework' #PACKAGE_NAME.capitalize()

# ------------------------------------------------------------------------------
MODULES = [
    [
        'Datasets', 
        'Some quick example text to build on the card title and make up the bulk of the card\'s content.', 
        '/dataset'
    ],[
        'Methods', 
        'Some quick example text to build on the card title and make up the bulk of the card\'s content.', 
        '/method'
    ],[
        'Scripting', 
        'Some quick example text to build on the card title and make up the bulk of the card\'s content.', 
        '/scripting'
    ],[
        'Results', 
        'Some quick example text to build on the card title and make up the bulk of the card\'s content.', 
        '/result'
    ],[
        'View', 
        'Some quick example text to build on the card title and make up the bulk of the card\'s content.', 
        '/view'
    ],[
        'Pages', 
        'Some quick example text to build on the card title and make up the bulk of the card\'s content.', 
        '/pages'
    ],
]

# ------------------------------------------------------------------------------
def underDev(pathname):
    import dash_bootstrap_components as dbc
    from dash import html
    return html.Div([
            dbc.Alert('Page "{}" not found, sorry. ;/'.format(pathname), color="info", style = {'margin':10})
        ])

def alert(msg, mtype="info"):
    import dash_bootstrap_components as dbc
    return dbc.Alert(msg, color=mtype, style = {'margin':10})

def render_markdown_file(file, div=False):
    from dash import html
    from dash import dcc
    f = open(os.path.join(ROOT, file), "r")
    if div:
        return html.Div(dcc.Markdown(f.read()), style={'margin': '20px'}, className='markdown')
    else:
        return dcc.Markdown(f.read())