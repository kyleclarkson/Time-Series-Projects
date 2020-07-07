import random
import numpy as np
import json
'''
    An experiment that stimulates the spread of an illness through a population.

    Over a k day episode, a small number of the population is initially sick. Each day
    members in the population choose to interact with other members at random. For any
    interactions with a sick member, and individual has a small chance to we become sick.

    Once sick, an individual continues to be sick for a certain number of days before recovering.

    TODO:
    - Add probabilities for getting sick, spreading with interaction,
    - Add recovery system.
    - Add means of interaction between individuals
    - Add method for tracking statistics of episode.

'''

class Individual:

    __slots__ = '_status', \
                '_age',\
                '_sick_at_time', \
                '_recovered_at_time', \
                '_dead_at_time', \
                '_time_to_recover', \
                '_prob_death',\
                '_prob_sick_from_interaction', \
                '_interaction_amount'

    """
        _status: 
            0: not sick, 
            1: is sick,
            2: is recovered.  
            3: is dead      
    """

    def __init__(self,
                 age=0,
                 prob_death=0.00,
                 prob_sick_from_interaction=0.05,
                 time_to_recover = 10,
                 interaction_amount=5):

        self._status = 0
        self._prob_death = prob_death
        self._prob_sick_from_interaction = prob_sick_from_interaction
        # The number of timesteps to recover.
        self._time_to_recover = time_to_recover
        # Number of interactions per time step.
        self._interaction_amount = interaction_amount

    def is_sick(self):
        return self._status == 1

    def is_recovered(self):
        return self._status == 2

    def is_dead(self):
        return self._status == 3

    def make_sick(self, timestep):
        self._sick_at_time = timestep
        self._status = 1

    def make_recover(self, timestep):
        self._recovered_at_time = timestep
        self._status = 2

    def make_dead(self, timestep):
        self._dead_at_time = timestep
        self._status = 3

class Population:

    __slots__ = '_population',\
                '_sickPopulation'

    def __init__(self, params):

        # TODO read params from file, craete population and individuals.
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
        pop_status_count = np.zeros(4,)

        for ind in self._population:
            pop_status_count[ind._status] += 1

        return pop_status_count.tolist()


    def make_interactions(self):
        # For each individual, choose interaction with other individuals at random.
        # Store as 2-tuple (A,B)
        interactions = []
        for ind in self._population:
            for idx in range(ind._interaction_amount):
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
        if ind1._isSick and not ind2._isSick:
            r = random.random()

            if r < ind2._interactionSicknessProb:
                ind2.make_sick(timestep)
                self._sickPopulation.append(ind2)
            if r < ind2._prob_sick_from_interaction:
                if ind2 not in self._sickPopulation:
                    ind2.make_sick(timestep)
                    self._sickPopulation.append(ind2)

        if not ind1._isSick and ind2._isSick:
            r = random.random()

            if r < ind1._interactionSicknessProb:
                ind1.make_sick(timestep)
                self._sickPopulation.append(ind1)

            if r < ind1._prob_sick_from_interaction:
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
                if timestep - (ind._sick_at_time + ind._time_to_recover) >= 0:
                    ind.make_recover(timestep)
                    self._sickPopulation.remove(ind)

            # Death of individuals
            for ind in self._sickPopulation:
                r = random.random()
                if r < ind._prob_death:
                    ind.make_dead(timestep)

            if display_status_count:
                print(str(timestep) + ": " + str(self.population_status_count()))


if __name__ == '__main__':

    # Read parameters from file into dict, pass to Population constructor.
    params = json.load(open('cold_spread.json'))
    population = Population(params)

