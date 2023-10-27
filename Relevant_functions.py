import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.graph_objects as go

def get_card_component(title, value):
# Check if title contains unit information separated by a forward slash
    if ' / ' in title:
        desc, unit = title.split(' / ')
        complete_title = [html.Span(desc.strip(), style={'line-height': '1.2','fontSize': '1.0em'}),
            html.Br(),
            html.Span(f"{unit.strip()}", style={'fontSize': '0.6em', 'line-height': '0.8'})
        ]
    else:
        complete_title = title

    component = dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5(complete_title, className="card-title" , style={'line-height': '1.0'}),
                            html.P(value, className="card-text")
                        ]), 
                        # color="dark", 
                        outline=False,
                        className = 'text-dark',
                        style={'textAlign': 'center', 'margin-bottom': '20px', 'background': '#ADD8E6'}
                    ),
                )
    return component

def get_score_list(scores, counter, unit_text):

    table_header = [
        html.Thead(
            html.Tr([
                html.Th("No."), 
                html.Th("Name"),
                html.Th([f"Total Emission" , html.Br(), f"({unit_text.get('Total emissions', '')})"]),
                html.Th([f"Scope 1 Emission" , html.Br(), f"({unit_text.get('Scope 1 emissions', '')})"]),
                html.Th([f"Scope 2 Emission" , html.Br(), f"({unit_text.get('Scope 2 emissions', '')})"]),
                html.Th([f"Net Energy Consumed", html.Br(), f"({unit_text.get('Net energy consumed', '')})"]),
            ])  
        )
    ]

    table_rows = []
    for score in scores:
        table_row = html.Tr([
            html.Td(counter),
            html.Td(score.get('Organisation name', '')),  
            html.Td(f"{score.get('Total emissions', 0):,.0f}"),
            html.Td(f"{score.get('Scope 1 emissions', 0):,.0f}"),  
            html.Td(f"{score.get('Scope 2 emissions', 0):,.0f}"), 
            html.Td(f"{score.get('Net energy consumed', 0):,.0f}"), 
        ])
        table_rows.append(table_row)
        counter += 1

    table_body = [html.Tbody(table_rows)]

    table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True, className='p-3 my-table')

    return table

def prepare_data(df, column_name):
    """Scale 1 to 100"""
    a = 1
    b = 100
    min_val =  df[column_name].min()
    max_val =  df[column_name].max()
    scaled = a + ((df[column_name] - min_val) * (b - a)) / (max_val - min_val)
        
    """Sort the data and calculate the cumulative percentage."""
    sorted_data = scaled.sort_values(ascending=True).reset_index(drop=True)
    cumulative_percent = 100 * sorted_data.cumsum() / sorted_data.sum()
    return sorted_data, cumulative_percent, column_name

def create_fig(sorted_data, cumulative_percent, column_name):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(range(len(sorted_data))),
        y=sorted_data,
        name=column_name,
        marker_color='blue'
    ))
    fig.add_trace(go.Scatter(
        x=list(range(len(cumulative_percent))),
        y=cumulative_percent,
        mode='lines+markers',
        name='Cumulative Percentage',
        yaxis='y2',
        marker_color='green'
    ))
    return fig

def fig_layout(fig, column_name):
    fig.update_layout(
       # title=f"2021-22 - Distribution of {column_name} (scaled 1 to 100)",
        xaxis_title='Controlling Entities',
        yaxis_title=f"{column_name} (scaled 1 to 100)",
        yaxis=dict(titlefont=dict(color='blue')),
        yaxis2=dict(
            title='Cumulative Percentage (%)',
            titlefont=dict(color='green'),
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        legend=dict (
            x=0.5,  # Horizontal position (80% from the left)
            y=0.95,  # Vertical position (95% from the bottom, close to the top)
            xanchor='center',  # Anchor point for x is center of the legend
            yanchor='top',  # Anchor point for y is top of the legend
            bgcolor='rgba(0,0,0,0)'  # Sets background to transparent
        )
    )
    return fig

