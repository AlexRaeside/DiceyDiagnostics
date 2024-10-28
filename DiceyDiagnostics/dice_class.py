import random
import pandas as pd

class WeirdDice:

    def __init__(
            self, d = None, bias_highest=0.00, extra_dimension=False, label=None):

        if label is None:
            self.label = "unnamed_dice"
        else:
            self.label = label

        self.d_set = [4,6,8,10,12,20]
        # select a dice
        if d is None:
            self.d_pick = self.d_set[random.randint(0, len(self.d_set))]
        elif d not in self.d_set:
            raise Exception(f"{d} not in recognised dice set of {self.d_set}")
        else:
            self.d_pick = d

        self.face_range = list(range(1,self.d_pick))

        base_face_freq = 1000 / self.d_pick

        face_freq = {}
        for n in self.face_range:
            face_freq[n] = base_face_freq

        self.bias_highest = bias_highest
        self.extra_dimension = extra_dimension

        if bias_highest != 0.00:
            new_bias_freq = base_face_freq + (base_face_freq * bias_highest)
            face_freq[self.d_pick] = new_bias_freq

        if extra_dimension is True:
            extra_dimension_face = self.d_pick + 1
            self.face_range.append(extra_dimension_face)
            face_freq[extra_dimension_face] = base_face_freq


        total_freq = sum(face_freq.values())
        self.face_props = {}
        for n,f in face_freq.items():
            self.face_props[n] = f / total_freq

        self.roll_history = []


    def roll(self, k=1):

        faces = list(self.face_props.keys())
        probabilities = list(self.face_props.values())
        roll_results = random.choices(faces, probabilities)

        self.roll_history.append(roll_results)

        return roll_results

    def give_params(self):
        return {
            "Label": self.label,
            "Dice": self.d_pick,
            "Highest_Bias": self.bias_highest,
            "Extra_Dimension": self.extra_dimension
        }

    def __str__(self):
        return (
            f""" A in-silico mystic dice.
            This dice could potentially be any off 
            the six typical dice used in DnD 5e. So 
            could be a d4, d6, d8, d10, d12 or d20.
            
            This could also potentially be biased 
            for the highest number in the dice.
            A d20 with highest_bias of 0.1 would have 
            a 5.5% chance to land of 20, which is 10% 
            higher then the usual 5%.
            
            Due to dimensional irregularity some dice have 
            gained an extra dimension so a d6 would have gained
            a 7th. Even if there a highest_bias in the dice 
            it does not affect the face gained through the 
            to dimensional irregularity. 
            
            The roll() method can be used to simulate a dice roll 
            and the roll_history variable tracks all dice rolls.
            The idea is to use a series of rolls and some 
            Bayesian inference to infer to parameters around this 
            dice. 
            
            But you can use give_params() to just show what the 
            params are but that is not the point.
            """)






