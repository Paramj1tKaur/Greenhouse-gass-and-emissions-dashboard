import dash_bootstrap_components as dbc
import pandas as pd

from dash import Dash, html, dcc, callback, Output, Input
from Total_page import get_total_page
from Relevant_functions import get_card_component, get_score_list, prepare_data, create_fig ,fig_layout
PAGE_SIZE =10

# Define a function to handle the renaming and storing of text within parentheses
def rename_and_store_units(df):
    renamed_columns = {}
    unit_text = {}
    
    for col in df.columns:
        parts = col.split('(')
        if len(parts) > 1:
            new_col_name = parts[0].strip().replace('Total s', 'S')
            unit_text[new_col_name] = parts[1].replace(')', '')
            renamed_columns[col] = new_col_name
    
    return df.rename(columns=renamed_columns), unit_text

# columns to change from object to numeric
columns_to_convert = ['Total scope 1 emissions (t CO2-e)',
       'Total scope 2 emissions (t CO2-e)', 
       'Net energy consumed (GJ)']  # Replace with the actual indices or names of the columns you want to convert

# Get data
CE_Controlling_corporations = "https://www.cleanenergyregulator.gov.au/DocumentAssets/Documents/Greenhouse%20and%20energy%20information%20by%20registered%20corporation%202021-22.csv"

# Read the CSV file and clean data
data = (
    pd.read_csv(CE_Controlling_corporations)
    .iloc[:, [0, 2, 3, 4]]
    .apply(lambda col: pd.to_numeric(col.str.replace(',', ''), errors='coerce') if col.name in columns_to_convert else col)
    .assign(**{'Total emissions (t CO2-e)': lambda x: x['Total scope 1 emissions (t CO2-e)'] + x['Total scope 2 emissions (t CO2-e)']},
            id = lambda x: x.index           
           )
)

# Rename the columns and store text within parentheses for later use
df, unit_text = rename_and_store_units(data)

# Get aggregates for Cards
Emitters = f"{df['Total emissions'].count():,.0f}"
Avg_emission =  f"{df['Total emissions'].mean():,.0f}"
Avg_scop1_emission = f"{df['Scope 1 emissions'].mean():,.0f}"
Avg_scop2_emission = f"{df['Scope 2 emissions'].mean():,.0f}"
Avg_net_energy_consumed =  f"{df['Net energy consumed'].mean():,.0f}"


#initialize app        
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#  app layout
app.layout = html.Div(
 [    
   html.H1(children='Greenhouse and energy - 2021-22 reported data', style={'textAlign':'center', 'padding-bottom': '10px'}),
    # to display measurement unit added them in the card labels 

    dbc.Row([
        get_card_component('Total Emitters / (No.)', Emitters),
        get_card_component('Average Emission / (t CO2-e)', Avg_emission),
        get_card_component('Average Scope 1 emissions / (t CO2-e)', Avg_scop1_emission),
        get_card_component('Average Scope 2 emissions / (t CO2-e)', Avg_scop2_emission),
        get_card_component('Average Net Energy Consumed / (GJ)', Avg_net_energy_consumed),
    ]),
    html.Br(), html.Br(), # to give some space between rows
    dbc.Row(
        dbc.Col([
            html.H3(children="Greenhouse and energy distribution by.."),
            html.Div(
                dbc.RadioItems(
                    id="energy-distribution-radios",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-dark",
                    labelCheckedClassName="active",
                    options=[
                        {'label': 'Scope 1 emissions', 'value':'Scope 1 emissions'},
                        {'label': 'Scope 2 emissions', 'value': 'Scope 2 emissions'},
                        {'label': 'Net energy consumed', 'value': 'Net energy consumed'},
                    ],
                    value='Scope 1 emissions',
                ),
                className ="radio-group",
                style = {'margin-top': '20px','textAlign': 'center', 'color': 'white', 'background':'#77aaff', 'border': 'none'}
            ),
            dcc.Graph(figure ={}, id="Energy-distribution")
        ])
    ),

    html.Br(), html.Br(), # to give some space between rows
    dbc.Row(
     [
        html.H3(id='table-title'),
        html.Div(
        dcc.Dropdown(
            id='sort-by-dropdown',
            options=[
                        {'label':'Total emissions', 'value':'Total emissions'},
                        {'label': 'Scope 1 emissions', 'value':'Scope 1 emissions'},
                        {'label': 'Scope 2 emissions', 'value': 'Scope 2 emissions'},
                        {'label': 'Net energy consumed', 'value': 'Net energy consumed'},
                    ],
                    value='Total emissions',  # default value
                    style={'background':'#77aaff', 'border': 'none'}
            ), 
            style = { 'border': 'none'}
              
          ),

        dbc.Table(id="score-list"),
        dbc.Pagination(id="pagination", max_value=get_total_page(PAGE_SIZE, 100), fully_expanded=False),
     ],                 
        
   )   
], style= {"margin": "50px 50px 50px 50px"})


#--- Call backs
@callback(
    Output("Energy-distribution", "figure"), 
    Input("energy-distribution-radios", "value")
)

def update_histogram(value):
    sorted_data, cumulative_percent, column_name = prepare_data(df, value)
    fig = create_fig(sorted_data, cumulative_percent, column_name)
    updated_fig = fig_layout(fig, column_name)
    return updated_fig

@callback(
    Output('table-title', 'children'),
    [Input('sort-by-dropdown', 'value')]
)

def update_table_title(selected_value):
    return f"Top 100 emitters and consumers by {selected_value.lower()}"


@callback(
    Output('score-list', 'children'),  # ID of the table to update
    [Input('sort-by-dropdown', 'value'), # ID of the dropdown
     Input('pagination', 'active_page')]  # ID of the pagination
)

def update_list_scores(selected_value, page):

    # Sort the DataFrame by the selected_value
    sorted_df = (df
                 .sort_values(by=selected_value, ascending=False)
                 .head(100)
                  .to_dict('records') )
    
    # convert active_page data to integer and set default value to 1
    int_page = 1 if not page else int(page)
    
    # define filter index range based on active page
    filter_index_1 = (int_page-1) * PAGE_SIZE
    filter_index_2 = (int_page) * PAGE_SIZE

    # get data by filter range based on active page number 
    filtered_scores = sorted_df[filter_index_1:filter_index_2]
    
      # Now convert this filtered DataFrame to a list of dictionaries
    # filtered_scores_dict = filtered_scores.to_dict('records')

    # load data to dash bootstrap table component
    table = get_score_list(filtered_scores, (filter_index_1 + 1), unit_text)
     
    return table

# Run the app
app.run_server(debug=True)  


