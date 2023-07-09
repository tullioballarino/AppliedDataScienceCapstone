# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
spacex_df['Result'] = np.where(spacex_df['class'] == 0, 'Failure', 'Success')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            ],
            value='ALL',
            placeholder="Select a launch site",
            searchable=True
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),
        # TASK 3: Add a range slider to select payload range
        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=500,
            marks={i:str(i) for i in range(0, 10001, 1000)},
            value=[min_payload, max_payload]
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df
        fig = px.pie(
            data_frame=filtered_df,
            values='class', 
            names='Launch Site', 
            title='Overall launch results from all sites'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            data_frame=filtered_df,
            names = 'Result',
            color_discrete_sequence=px.colors.qualitative.Light24,
            title= 'Launch results from site ' + entered_site
        )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, selected_range):
    if entered_site == 'ALL':      
        filtered_df = spacex_df
        graph_title = 'Overall launch results from all sites depending on Payload Mass'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        graph_title = 'Launch results from site ' + entered_site + ' depending on Payload Mass'
    inf = selected_range[0]
    sup = selected_range[1]
    fig = px.scatter(
        data_frame=filtered_df[filtered_df['Payload Mass (kg)'].between(inf, sup)],
        x='Payload Mass (kg)',
        y='Result',
        color="Booster Version Category",
        title=graph_title
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
