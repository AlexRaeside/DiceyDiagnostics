import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

# function that turns the roll freq table into a bar chart


def freq_bar_chart(dice_freq_pd, print_plot=False, png_name="dice_freq.png"):
    # sort the different faces
    dice_freq_pd = dice_freq_pd.sort_values(by='Face', ascending=True)
    dice_freq_pd["Face"] = dice_freq_pd["Face"].astype(str)
    fig = px.bar(dice_freq_pd, x="Face", y="Freq", template="seaborn")
    fig.update_yaxes(tickmode='linear')  # Ensure ticks are in linear mode
    fig.update_yaxes(dtick=1)

    if print_plot is True:
        pio.write_image(fig, png_name, format="png")
    return fig

def dice_prob_graph(prob_pb, print_plot=False, png_name="dice_prob.png"):

    # restructure the table
    prob_pb_long = prob_pb.melt(id_vars=["roll"], var_name="dice", value_name="probability")

    # Plot with Plotly Express
    prob_fig = px.line(
        prob_pb_long,
        x="roll",
        y="probability",
        color="dice",
        markers=True,
        title="Probability Distribution Across Dice Rolls"
    )
    # the last point should be a little bigger

    for trace in prob_fig.data:
        dice_type = trace.name
        final_roll = prob_pb_long['roll'].max()

        # Get the final point's index
        final_index = (prob_pb_long['dice'] == int(dice_type)) & (prob_pb_long['roll'] == final_roll)
        final_probability = prob_pb_long.loc[final_index, 'probability'].values[0]

        # Add the larger final point with the same color
        prob_fig.add_trace(
            go.Scatter(
                x=[final_roll],
                y=[final_probability],
                mode='markers',
                marker=dict(size=10, color=trace.line.color),
                name=dice_type,
                showlegend=False
            )
        )

    if print_plot is True:
        pio.write_image(prob_fig, png_name, format="png")
    return prob_fig



