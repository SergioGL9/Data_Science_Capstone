# Import required libraries
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Initialize the Dash app
app = Dash(__name__)

# Assume you have a spacex_df dataframe ready to use
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# TASK 1: Add a Launch Site Drop-down Input Component
app.layout = html.Div(children=[
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'}] +
                     [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                 ),
    html.Br(),

    # TASK 2: Add a pie chart to render success-pie-chart based on selected site dropdown
    dcc.Graph(id='success-pie-chart'),

    # TASK 3: Add a Range Slider to Select Payload
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: '{} Kg'.format(i) for i in range(0, 10001, 1000)},
                    value=[min(spacex_df['Payload Mass (kg)']), max(spacex_df['Payload Mass (kg)'])]
                    ),
    html.Br(),

    # TASK 4: Add a scatter plot to render the success-payload-scatter-chart
    dcc.Graph(id='success-payload-scatter-chart')
])


# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f'Total Success Launches for site {entered_site}')
    return fig


# TASK 4: Add a callback function to render success-payload-scatter-chart scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_plot(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version Category")
    else:
        fig = px.scatter(filtered_df[filtered_df['Launch Site'] == entered_site],
                         x='Payload Mass (kg)', y='class', color="Booster Version Category")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
