import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

# Load the Excel data into a pandas DataFrame
df = pd.read_excel(r'C:\Users\hammonn\Documents\Etown_College-04_04_23-05_17_23-_Countermovement_Jump.xlsx')

# Create a Dash app
app = dash.Dash(__name__)
server = app.server

# Define the dropdown menu options for y-axis selection
y_options = [
    'System Weight', 'Jump Height', 'Jump Momentum', 'Countermovement Depth',
    'Braking RFD', 'Stiffness', 'Force at Min Displacement',
    'Relative Force at Min Displacement', 'Avg. Braking Force',
    'Avg. Relative Braking Force', 'Peak Braking Force',
    'Peak Relative Braking Force', 'Avg. Propulsive Force',
    'Avg. Relative Propulsive Force', 'Peak Propulsive Force',
    'Peak Relative Propulsive Force', 'Unweighting Phase',
    'Unweighting Phase %', 'Braking Phase', 'Braking Phase %',
    'Propulsive Phase', 'Propulsive Phase %', 'Flight Time',
    'Time To Takeoff', 'Braking Net Impulse', 'Propulsive Net Impulse',
    'Positive Impulse', 'Positive Net Impulse', 'Impulse Ratio',
    'Avg. Braking Velocity', 'Peak Braking Velocity',
    'Avg. Propulsive Velocity', 'Takeoff Velocity', 'Peak Velocity',
    'Avg. Braking Power', 'Avg. Relative Braking Power',
    'Peak Braking Power', 'Peak Relative Braking Power',
    'Avg. Propulsive Power', 'Avg. Relative Propulsive Power',
    'Peak Relative Propulsive Power', 'Peak Propulsive Power',
    'Landing Stiffness', 'Peak Landing Force', 'Avg. Landing Force',
    'Relative Peak Landing Force', 'RSI', 'mRSI', 'Braking Impulse',
    'Relative Braking Impulse', 'Relative Braking Net Impulse',
    'Propulsive Impulse', 'Relative Propulsive Impulse',
    'Relative Propulsive Net Impulse'
]

# Define the dropdown menu options for sport selection
sport_options = df['Sport'].unique()

# Set up the app layout
app.layout = html.Div([
    dcc.Dropdown(
        id='y-dropdown',
        options=[{'label': metric, 'value': metric} for metric in y_options],
        value=y_options[0],
        placeholder='Select Y-Axis Metric'
    ),
    dcc.Dropdown(
        id='gender-dropdown',
        options=[
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Female', 'value': 'Female'}
        ],
        value=None,
        placeholder='Select Gender',
        multi=True
    ),
    dcc.Dropdown(
        id='sport-dropdown',
        options=[{'label': sport, 'value': sport} for sport in sport_options],
        value=None,
        placeholder='Select Sport',
        multi=True
    ),
    dcc.Graph(id='data-graph')
])

# Define the callback function to update the graph based on the selected y-axis metric, gender, and sport
@app.callback(
    dash.dependencies.Output('data-graph', 'figure'),
    [dash.dependencies.Input('y-dropdown', 'value'),
     dash.dependencies.Input('gender-dropdown', 'value'),
     dash.dependencies.Input('sport-dropdown', 'value')]
)
def update_graph(selected_y, selected_gender, selected_sport):
    filtered_df = df[df['Gender'].isin(selected_gender)] if selected_gender else df
    filtered_df = filtered_df[filtered_df['Sport'].isin(selected_sport)] if selected_sport else filtered_df
    
    # Calculate the average y-axis metric value for each athlete
    avg_df = filtered_df.groupby('Athlete')[selected_y].mean().reset_index()
    
    # Merge with filtered_df to include the 'Gender' and 'Sport' columns
    avg_df = avg_df.merge(filtered_df[['Athlete', 'Gender', 'Sport']], on='Athlete', how='left')
    
    fig = px.scatter(avg_df, x='Athlete', y=selected_y, color='Sport', symbol='Gender')
    fig.update_traces(marker=dict(size=10))  # Increase the dot size
    
    # Add a dotted line for the average of the y-axis values
    avg_line = go.Scatter(
        x=avg_df['Athlete'],
        y=[avg_df[selected_y].mean()] * len(avg_df),
        mode='lines',
        name='Average',
        line=dict(dash='dash')
    )
    fig.add_trace(avg_line)
    
    fig.update_layout(title=f'Average {selected_y} by Athlete')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
