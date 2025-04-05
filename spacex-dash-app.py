import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get the min and max payload values for the RangeSlider
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create the Dash application
app = dash.Dash(__name__)

# Create the layout of the app
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Task 1: Dropdown for selecting Launch Site
    html.Br(),
    dcc.Dropdown(id='site-dropdown',
                 options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                         [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),

    # Task 2: Pie chart for success/failure rate
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # Task 3: Payload range slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={i: f'{i}' for i in range(0, 10001, 2000)},
                    value=[min_payload, max_payload]),

    # Task 4: Scatter chart for payload vs success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Task 2: Callback function for the success-pie-chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(selected_site):
    # If 'ALL' sites are selected, show the total success vs failure for all sites
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='class', title='Total Success vs Failed Launches')
        return fig
    else:
        # Filter the dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', title=f'Success vs Failed Launches for {selected_site}')
        return fig

# Task 4: Callback function for success-payload-scatter-chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def render_scatter_chart(selected_site, selected_payload):
    min_payload, max_payload = selected_payload

    # Filter by the selected payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & 
                            (spacex_df['Payload Mass (kg)'] <= max_payload)]

    # If a specific site is selected, filter by that site as well
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    # Generate the scatter plot
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                     color='Booster Version Category', title='Payload vs Launch Success')
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
