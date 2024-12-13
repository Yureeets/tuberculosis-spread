import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from model import VirusModel
from graph import all_nodes
from agent import Person
from settings import config_colors

initial_city = 'Lviv, Ukraine'
model = VirusModel(initial_city, all_nodes[initial_city]['gdf_nodes'])

iteration_count = 0

infected_counts = []
latent_counts = []
deceased_counts = []

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(children='Spread of Tuberculosis Simulation'),
    # html.H2(children=f"Simulation for {model.current_city}"),
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in all_nodes.keys()],
        value=initial_city,
        style={'width': '50%'}
    ),
    dcc.Graph(
        id='map-plot',
        config={'displayModeBar': False},
        style={'height': '75vh', 'display': 'inline-block'},
    ),
    dcc.Graph(
        id='infected-count-plot',
        config={'displayModeBar': False},
        style={'height': '40vh', 'display': 'inline-block'}
    ),
    html.Button("Start Simulation", id="toggle-simulation", n_clicks=0),
    html.Button("Restart Simulation", id="restart-simulation", n_clicks=0),
    dcc.Interval(id='simulation-interval', interval=400, n_intervals=0, disabled=True),
    html.Div(id='iteration-count', children='Iteration: 0')
])


@app.callback(
    Output('simulation-interval', 'disabled'),
    Output('toggle-simulation', 'children'),
    Input('toggle-simulation', 'n_clicks'),
    State('simulation-interval', 'disabled')
)
def toggle_simulation(n_clicks, is_paused):
    if n_clicks > 0:
        return not is_paused, "Pause Simulation" if is_paused else "Start Simulation"
    return is_paused, "Start Simulation"


@app.callback(
    [Output('map-plot', 'figure'),
     Output('infected-count-plot', 'figure'),
     Output('iteration-count', 'children'),
     Output('restart-simulation', 'n_clicks')],  # Reset restart button click count
    [Input('simulation-interval', 'n_intervals'),
     Input('city-dropdown', 'value'),
     Input('restart-simulation', 'n_clicks')]  # New input for restarting
)
def update_map(n_intervals, selected_city, restart_clicks):
    global model, infected_counts, latent_counts, iteration_count, deceased_counts

    if restart_clicks > 0:
        model = VirusModel(selected_city, all_nodes[selected_city]['gdf_nodes'])
        infected_counts = []
        latent_counts = []
        deceased_counts = []
        iteration_count = 0

    if model.current_city != selected_city:
        model = VirusModel(selected_city, all_nodes[selected_city]['gdf_nodes'])
        infected_counts = []
        latent_counts = []
        deceased_counts = []

    model.step()

    x_data, y_data, colors, sizes, opacity = model.get_agent_data()

    scatter_map = go.Scattermapbox(
        lat=y_data,
        lon=x_data,
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            opacity=opacity,
            symbol='circle',
        ),
    )

    layout_map = go.Layout(
        mapbox=dict(
            style="open-street-map",
            center={"lat": all_nodes[selected_city]['lat'], "lon": all_nodes[selected_city]['lon']},
            zoom=10,
            layers=[
                {
                    'sourcetype': 'raster',
                    'source': [
                        "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
                        "https://b.tile.openstreetmap.org/{z}/{x}/{y}.png",
                        "https://c.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    ],
                    'opacity': 0.5
                }
            ]
        ),
        showlegend=True
    )

    infected_count = model.count_state(Person.INFECTED)
    infected_counts.append(infected_count)

    latent_count = model.count_state(Person.LATENT)
    latent_counts.append(latent_count)

    deceased_count = model.count_state(Person.DECEASED)
    deceased_counts.append(deceased_count)

    infected_count_plot = go.Figure()
    infected_count_plot.add_trace(go.Scatter(
        x=list(range(len(infected_counts))),
        y=infected_counts,
        mode='lines+markers',
        name='Infected',
        line=dict(shape='linear', color=config_colors[Person.INFECTED])
    ))

    infected_count_plot.add_trace(go.Scatter(
        x=list(range(len(latent_counts))),
        y=latent_counts,
        mode='lines+markers',
        name='Latent',
        line=dict(color=config_colors[Person.LATENT]),
    ))

    infected_count_plot.add_trace(go.Scatter(
        x=list(range(len(deceased_counts))),
        y=deceased_counts,
        mode='lines+markers',
        name='Deceased',
        line=dict(shape='linear', color=config_colors[Person.DECEASED])
    ))

    infected_count_layout = go.Layout(
        title='Count of Infected Individuals Over Time',
        xaxis=dict(title='Iterations'),
        yaxis=dict(title='Number of Infected'),
        showlegend=True
    )

    iteration_count += 1
    iteration_display = f'Iteration: {iteration_count}'

    return {'data': [scatter_map], 'layout': layout_map}, \
        infected_count_plot.update_layout(infected_count_layout), \
        iteration_display, 0


if __name__ == '__main__':
    app.run_server()
