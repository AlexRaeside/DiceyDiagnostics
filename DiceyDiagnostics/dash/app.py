from dash import Dash, html, dcc, Input, Output, State, callback
from dice_class import WeirdDice
from roller_class import RollerBot
from dice_plots import dice_prob_graph, freq_bar_chart
import dash_bootstrap_components as dbc
import uuid
import logging
import json

logging.basicConfig(
    filename="DiceDiagnostics_app.log",
    encoding="utf-8",
    filemode="w",
    format="{asctime} - {levelname} - {message}",
    style="{",datefmt="%Y-%m-%d %H:%M")

logging.info(" -- Setting up the Dash app layout. --")

app = Dash(external_stylesheets=[dbc.themes.COSMO])

app.layout = dbc.Container(
    [
        html.H1("Dicey Diagnostics"),
        dcc.Markdown(
            """
            Hello and welcome to my little dice rolling Bayesian statistics dice app.
            The app is really just a quick mess-around to better my of understanding of Dash Apps 
            since as a bioinformatician I am all in on Dash apps and the nice [biological figures]() they make. 
            
            I'm also going to have to chuck in some API and SQL bits as I need to add those if I want 
            python developer work. 
            
            So first of let get some FastAPI junk out of the way with a event that occurred on this day of 
            {date} courtesy of the nice Wikiepedia API endpoints. 
            
            Ta-Da! And you can reload this page and see how it changes. 
            
            Now let me explain this dice thing. Click the 'Generate Dice' button to generate a random DnD 
            dice (d4, 46, d8, d10, d12, d20) with a unique id. Then click 'Roll Dice' to roll that same 
            dice and get a number. Bayesian stats is used to predict what type of dice you are rolling.
            
            Once you have your dice prediction and you just abosultly need to what dice it actually was 
            
            """),
        dbc.Button("Reset dice", id="create-dice-btn", n_clicks=0, className="me-2"),
        dbc.Button("Roll dice", id="roll-dice-btn", n_clicks=0),
        html.Br(),
        html.Div(id="dice-id-txt"),
        html.Div(id="output-text"),
        dcc.Store(id='user-roller-id')
    ],
)

# The Global variable contains a dict with dice rollers
# every time a user clicks 'create_dice' a dice is set in dict
# with an uid key -

roller_dict = {}

# Storing the unique RollerBot ID in dcc.Store
@app.callback(
    [
        Output("user-roller-id", "data"),
        Output(component_id="dice-id-txt", component_property="children")],
    Input("create-dice-btn", "n_clicks"),
    prevent_initial_call=True)
def instantiate_roller(n_clicks):
    logging.info("Making a new dice and roller.")
    # Generate a unique ID
    new_roller = RollerBot()
    # adding a dice
    new_dice = WeirdDice()
    new_roller.add_dice(new_dice)
    roller_id = new_roller.uid
    global roller_dict
    roller_dict[roller_id] = new_roller
    logging.info(f"Roller {roller_id} add to roller_dict. Roller_dict now contains {len(roller_dict)} objects.")
    return json.dumps(roller_id),roller_id

@callback(
    Output(component_id="output-text", component_property='children'),
    [Input("roll-dice-btn", "n_clicks"),
    Input("user-roller-id", "data")])
def roll_dice(n_clicks, roller_id):
    if n_clicks:
        edit_id = str(roller_id).strip('""')
        logging.info(f"looking for roller: {edit_id}")
        global roller_dict
        roll_output = roller_dict[edit_id].roll_dice()
        return roll_output




if __name__ == '__main__':
    app.run(debug=True)