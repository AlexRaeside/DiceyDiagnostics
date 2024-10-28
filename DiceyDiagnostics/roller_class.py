# a class that takes a WeirdDice and rolls it until it can determine
# which dice it is
# outputs tables
from logging import exception
from dice_class import WeirdDice
from DiceyDiagnostics.dice_class import WeirdDice


class RollerBot:
    def __init__(self, name=None, certainty_threshold=0.999, max_rolls=1000):
        if name is None:
            self.name = "unnamed"

        self.dice_slot = None

        self.dice_prob_initial = {
            4: 0.167,
            6: 0.167,
            8: 0.167,
            10: 0.167,
            12: 0.167,
            20: 0.167,
        }

        self.roll_history = []
        self.posterior = []
        self.roll_freq = {}

    def add_dice(self, dice: WeirdDice):
        if type(dice) is not WeirdDice:
            raise exception("You need to add a WeirdDice type")
        self.dice_slot = dice

    def roll_dice(self):

        roll_result = self.dice_slot.roll()
        self.roll_history.append(roll_result)

        if roll_result not in self.roll_freq.keys():
            self.roll_freq[roll_result] = 1
        else:
            self.roll_freq[roll_result] += 1

        return roll_result

    def update_posterior(self):

        if len(self.posterior) == 0:
            current_post = self.dice_prob_initial
        else:
            current_post = self.
