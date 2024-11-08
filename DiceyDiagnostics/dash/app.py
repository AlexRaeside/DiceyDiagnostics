from dash import Dash, html, dcc, Input, Output, State
from dice_class import WeirdDice
from roller_class import RollerBot
from dice_plots import dice_prob_graph, freq_bar_chart
import dash_bootstrap_components as dbc
import uuid


app = Dash()

app.layout = dbc.Container(
    [
        html.H2("Dash App with Object Creation and Method Call"),
        dbc.Button("Reset dice", id="create-dice-btn", n_clicks=0, className="me-2"),
        dbc.Button("Roll dice", id="roll-dice-btn", n_clicks=0),
        html.Br(),
        html.Div(id="output-text", children="Output will be displayed here."),
    ],
    fluid=True,
    className="p-4",
)

# Global variable to store the created object
# roll the dice and add it to the roller
unknown_dice = WeirdDice()
roller = RollerBot()
roller.add_dice(unknown_dice)


# this master function handles what do for the
# the different buttons that can be pressed


if __name__ == '__main__':
    app.run(debug=True)