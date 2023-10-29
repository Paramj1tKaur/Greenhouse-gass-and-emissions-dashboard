# Greenhouse-gass-and-emissions-interactive dashboard

## Description
<p>This code creates interactive web-based application using dash which is a python framework by plotly. The interactive application build is viewed on the web browser. </p>
<p>The data for this application has been sourced from National Greenhouse and Energy Reporting scheme data file https://www.cleanenergyregulator.gov.au/DocumentAssets/Documents/Greenhouse%20and%20energy%20information%20by%20registered%20corporation%202021-22.csv <br></p>

### The application show:
- Five cards
- Interactive figure for the greenhouse and energy distribution by user selected option 
- Interactive table reporting top 100 emitters or consumers by user selected option. 


## Code
The code is divided into following components:
1.	The layout of the dashboard (main.py) 
2.	Functions for creating Plotly graphs and data card contents (Relevant_functions.py)
3.	 Functions for navigating Top 100 emitters and consumers to different pages (Total_page.py)
4.	The navigation bar of the dashboard (main.py).
5.	Callback for adding interactivity to the dashboard(main.py)

## Installation
### Prerequisites
- Python 3.8.10
- dash
- dash_bootstrap_components
- pandas
- plotly.graph_objects  

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/Paramj1tKaur/Greenhouse-gass-and-emissions-dashboard.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Greenhouse-gass-and-emissions-dashboard
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
### Usage:	
1. Run the Dash app:
    ```bash
    python main.py
    
    This will start the application and you would see output similiar to the following
    Running on `http://127.0.0.1:8050/`.
    ```
2. Open your web browser and go to `http://127.0.0.1:8050/`.

