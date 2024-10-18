from datetime import datetime
from random import random

import dash
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import serial
import threading
import socket
import time

# Set up the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.178.45', 8000))

# Initialize the Dash app
#app = dash.Dash(__name__)
app = Dash(__name__)

# Layout
app.layout = html.Div([
    #html.Div(children='Jack (c)', style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),
    html.Div(id='geleverd', style={'textAlign': 'left', 'color': 'green', 'fontSize': 30}),
    html.Div(id='gebruikt', style={'textAlign': 'left', 'color': 'red', 'fontSize': 30}),
    dcc.Graph(id='live-graph',
              style={'height': '100vh', 'width': '100vw'},
              animate=True
    ),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Update every second
        n_intervals=0
    )
])

# Global lists to store data
x_data = []
geb_data = []
gel_data = []

def read_sensor_data():
    while True:
        try:
            data = client_socket.recv(1024).decode().split()
            if data:
                print('GEB: ', data[1])
                print('GEL: ', data[3])
                geb_data.append(int(data[1]))
                gel_data.append(int(data[3]))
                #current_time = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d, %H:%M:%S')
                current_time = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
                x_data.append(current_time)
                print('Time: ', current_time)
        except ValueError:
            print(f"Received non-integer data: {data}")
@app.callback([Output('live-graph','figure'), Output('geleverd','children'), Output('gebruikt','children')],
              [Input('interval-component', 'n_intervals')]
)
def update_graph_live(n):
    #x_data_scrolling = x_data[-20:]
    #value = gel_data
    fig = go.Figure(
        data=[

                # go.Scatter(x=x_data, y=y_data, mode='lines+markers'),
                # go.Scatter(x=x_data, z=z_data, mode='lines+markers')
                go.Scatter(x=x_data, y=geb_data, marker=dict(color='red')),
                go.Scatter(x=x_data, y=gel_data, marker=dict(color='green')),

            ],
            layout=go.Layout(
            title='Real-Time Sensor Data',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Sensor Value',
                    'range': [0, 3000] },
            #xaxis_rangeslider_visible = True  # Enable x-axis scrolling
        )
    )
    fig.update_layout(barmode='group', title='Real-Time Energy Graph')
    geleverd = f'GELEVERD: {gel_data}'
    gebruikt = f'GEBRUIKT: {geb_data}'
    return fig, geleverd, gebruikt

if __name__ == '__main__':
    #Start the sensor data reading thread
    threading.Thread(target=read_sensor_data, daemon=True).start()
    app.run_server(debug=True)

