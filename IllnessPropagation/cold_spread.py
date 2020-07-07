import random
import numpy as np
import json

from ReadParams import read_dict
'''
    An experiment that stimulates the spread of an illness through a population.

    Over a k day episode, a small number of the population is initially sick. Each day
    members in the population choose to interact with other members at random. For any
    interactions with a sick member, and individual has a small chance to we become sick.

    Once sick, an individual continues to be sick for a certain number of days before recovering.

    TODO:
    C Add probabilities for getting sick, spreading with interaction,
    C Add recovery system.
    C Add means of interaction between individuals
    
    - Add method for tracking statistics of episode.
'''

class Individual:

    __slots__ = '_isSick',\
                '_status',\
                '_sickAtTime',\
                '_recoveredAtTime',\
                '_timeToRecover',\
                '_interactionSicknessProb',\
                '_numOfInteractions'

    """
        _status: 
            0: not sick, 
            1:  is sick,
            2:  is recovered.        
    """

    def __init__(self,
                 interaction_sickness_prob=0.3,
                 time_to_recover = 5):
        self._isSick = False
        self._status = 0
        self._interactionSicknessProb = interaction_sickness_prob
        self._timeToRecover = time_to_recover
        self._numOfInteractions = 3

    def make_sick(self, timestep):
        self._sickAtTime = timestep
        self._status = 1
        self._isSick = True

    def make_recover(self, timestep):
        self._recoveredAtTime = timestep
        self._status = 2
        self._isSick = False

class Population:

    __slots__ = '_population',\
                '_sickPopulation'

    def __init__(self, numOfIndividuals, numOfSickIndividuals):

        # Create population of individuals.
        self._population = []
        for index in range(numOfIndividuals):
            self._population.append(Individual())

        sickInds = random.sample(self._population, numOfSickIndividuals)
        self._sickPopulation = []
        for sickInd in sickInds:
            sickInd.make_sick(0)
            self._sickPopulation.append(sickInd)

    def size(self):
        # The number of individuals in the population.
        return len(self._population)

    def population_status(self):
        # The status of each individual in the population
        return [ind._status for ind in self._population]

    def population_status_count(self):
        # The count of not sick, sick, and recovered individuals currently
        # in population.
        not_sick = 0
        sick = 0
        recovered = 0

        for ind in self._population:
            if ind._status == 0: not_sick += 1
            if ind._status == 1: sick += 1
            if ind._status == 2: recovered += 1

        return [not_sick, sick, recovered]

    def make_interactions(self):
        # For each individual, choose interaction with other individuals at random.
        # Store as 2-tuple (A,B)
        interactions = []
        for ind in self._population:
            for idx in range(ind._numOfInteractions):
                interact_with_ind = self.get_random_individual()
                # Only add if one is sick.
                if interact_with_ind._isSick or ind._isSick:
                    interactions.append((ind, interact_with_ind))

        return interactions

    def play_out_interaction(self, timestep, ind1, ind2):
        """
            Compute probability that sickness spreads between
            two individuals using random number.
        """
        if ind1._isSick and ind2._status != 2:
            r = random.random()
            if r < ind2._interactionSicknessProb:
                if ind2 not in self._sickPopulation:
                    ind2.make_sick(timestep)
                    self._sickPopulation.append(ind2)

        if ind1._status != 2 and ind2._isSick:
            r = random.random()
            if r < ind1._interactionSicknessProb:
                if ind1 not in self._sickPopulation:
                    ind1.make_sick(timestep)
                    self._sickPopulation.append(ind1)


    def get_random_individual(self):
        return random.choice(self._population)

    def runExperiment(self, horizon=100, display_status_count=False):

        for timestep in range(horizon):
            # Have interactions between individuals, make sick if needed.
            interactions = self.make_interactions()
            for ind1, ind2 in interactions:
                self.play_out_interaction(timestep, ind1, ind2)

            # Recover individuals
            for ind in self._sickPopulation:
                if timestep - (ind._sickAtTime + ind._timeToRecover) >= 0:
                    ind.make_recover(timestep)
                    self._sickPopulation.remove(ind)

            if display_status_count:
                print(str(timestep) + ": " + str(self.population_status_count()))



if __name__ == '__main__':
    pop = Population(100, 1)

    params = json.load(open('cold_spread.json'))
    print(params["recover_time"][0])
