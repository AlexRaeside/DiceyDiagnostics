# a class that takes a WeirdDice and rolls it until it can determine
# which dice it is
# outputs tables
from logging import exception
from traceback import print_tb

from dice_class import WeirdDice
import seaborn as sb
import pandas as pd

class RollerBot:
    def __init__(self, name=None, certainty_threshold=0.999, max_rolls=1000):
        if name is None:
            self.name = "unnamed"

        self.dice_slot = None

        self.dice_prior_initial = {
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
        self.prob_threshold = 0.999
        self.predicted_dice = None

    def add_dice(self, dice: WeirdDice):
        if type(dice) is not WeirdDice:
            raise exception("You need to add a WeirdDice type")
        self.dice_slot = dice

    def roll_dice(self):

        roll_result = self.dice_slot.roll()[-1]
        self.roll_history.append(roll_result)

        if roll_result not in list(self.roll_freq.keys()):
            self.roll_freq[roll_result] = 1
        else:
            self.roll_freq[roll_result] += 1

        print(roll_result)
        print(self.roll_freq)

        return roll_result

    def chance_of_dice_given_roll(self, roll):
        """ What is the chance of getting that roll for all different dice
        If you leave roll blank it will use the last roll_result

        :return: dict
        """

        if roll is None:
            roll = self.roll_history[-1]

        dice_set = list(self.dice_prior_initial.keys())
        prob_dict = {}

        for d in dice_set:
            if roll > d:
                prob = 0
            else:
                prob = 1 / d
            prob_dict[d] = prob

        return prob_dict

    def bayes_update(self):
        """ Given the current roll what is the probability of each dice


        :return:
        """

        # P(Dice_n|the rolls observed) = P(the roll seen | Dice_n) x Prior(P(Dice_n) / Data(all possible dice)

        # first work out the probability of dice given roll
        # uses the last dice roll
        roll = self.roll_history[-1]
        dice_prob_dict = self.chance_of_dice_given_roll(roll)
        # first work out the normalized posterior
        raw_posterior = {}
        for d in self.dice_prior_initial.keys():
            if len(self.posterior) == 0:
                prior_dict = self.dice_prior_initial
            else:
                prior_dict = self.posterior[-1]

            raw_posterior[d] = dice_prob_dict[d] * prior_dict[d]

        all_probs = sum(raw_posterior.values())

        normalized_posterior = {}
        for d in self.dice_prior_initial.keys():
            normalized_posterior[d] = raw_posterior[d] / all_probs

        print(normalized_posterior)

        # add the new posterior to be used as the prior in the next round
        self.posterior.append(normalized_posterior)

        for d,p in normalized_posterior.items():
            if p >= self.prob_threshold:
                self.predicted_dice = d

    def roll_update(self, stop_after_threshold=True):

        if self.predicted_dice is not None and stop_after_threshold is True:
            return

        self.roll_dice()

        self.bayes_update()

    def pd_roll_freq(self):
        """ return sea born showing roll freq


        :return:
        """

        # convert the roll freq dict to a pandas data frame
        return pd.DataFrame(list(self.roll_freq.items()), columns=['Face', 'Freq'])

    def pd_prob_posterior(self):

        # add the initial probs to the list
        prob_dict = {0: self.dice_prior_initial}
        # now add all the posterior probs
        pos = 1
        for pos_dict in self.posterior:
            prob_dict[pos] = pos_dict
            pos += 1

        # Convert to DataFrame
        prob_pd = pd.DataFrame.from_dict(prob_dict, orient='index')

        # Reset the index to create a 'roll number' column
        prob_pd.reset_index(inplace=True)

        # Rename the index column to 'roll number'
        prob_pd = prob_pd.rename(columns={'index': 'roll'})

        return  prob_pd









