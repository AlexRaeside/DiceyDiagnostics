from roller_class import RollerBot
from dice_class import WeirdDice
from dice_plots import freq_bar_chart, dice_prob_graph
# create a dice

unknown_dice = WeirdDice()

roller = RollerBot()

roller.add_dice(unknown_dice)

roller.roll_dice()

roller.bayes_update()

roller.roll_dice()

roller.bayes_update()

roller.roll_dice()

roller.bayes_update()

roller.roll_dice()

roller.bayes_update()

freq_pd = roller.pd_roll_freq()
print(freq_pd)
freq_bar_chart(dice_freq_pd=freq_pd, print_plot=True)
prob_pb = roller.pd_prob_posterior()
print(prob_pb)

dice_prob_graph(prob_pb=prob_pb, print_plot=True)


