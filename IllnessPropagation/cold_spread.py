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
    C Add probabilities for getting sick, spreading with interaction,
    C Add recovery system.
    C Add means of interaction between individuals
    
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

    def can_contract(self):
        return self._status == 0

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

    '''
    Lists contain individuals depending on their status. _population contains all individuals,
    where the 4 remaining list are a partition of _population.
    '''

    __slots__ = '_population',\
                '_not_exposed',\
                '_sick',\
                '_recovered',\
                '_dead'

    def __init__(self, params):

        # Create population of individuals.
        # TODO change datastructures to allow for indexing by individual key. 
        self._population = []
        self._not_exposed = []
        self._sick = []
        self._recovered = []
        self._dead = []

        for index in range(params['pop_init_size']):

            recover_time = round(np.random.normal(params['recover_time'][0],
                                                  params['recover_time'][1]))
            if recover_time < 0: recover_time = 1

            interaction_amount = round(np.random.normal(params['interaction_amount'][0],
                                                        params['interaction_amount'][1]))
            if interaction_amount < 0: interaction_amount = 0

            ind = Individual(
                prob_death=params['prob_death'],
                time_to_recover=recover_time,
                interaction_amount=interaction_amount
            )
            self._population.append(ind)
            self._not_exposed.append(ind)

        # Create sub population of sick individuals.
        sick_inds = random.sample(self._not_exposed, params['pop_init_sick_size'])

        for sick_ind in sick_inds:
            sick_ind.make_sick(0)
            self._sick.append(self._not_exposed.pop(sick_ind))

    def population_status(self):
        # The status of each individual in the population
        return [ind._status for ind in self._not_exposed]

    def population_status_count(self):
        # The number of individuals in each sub population.


        return [len(self._not_exposed),
                len(self._sick),
                len(self._recovered),
                len(self._dead)]

    def make_interactions(self):
        # For each individual, choose interaction with other individuals at random.
        # Store as 2-tuple (A,B)
        interactions = []
        for ind in self._population:
            for idx in range(ind._interaction_amount):
                interact_with_ind = self.get_random_individual()
                # Only add if one is sick.
                if interact_with_ind.is_sick() or ind.is_sick():
                    interactions.append((ind, interact_with_ind))

        return interactions

    def play_out_interaction(self, timestep, ind1, ind2):
        """
            Compute probability that sickness spreads between
            two individuals using random number.
        """
        if ind1 in self._sick and ind2 in self._not_exposed:
            r = random.random()

            if r < ind2._prob_sick_from_interaction:
                ind2.make_sick(timestep)
                self._sick.append(self._not_exposed.remove(ind2))

        if ind1 in self._not_exposed and ind2 in self._sick:
            r = random.random()

            if r < ind1._prob_sick_from_interaction:
                ind1.make_sick(timestep)
                self._sick.append(self._not_exposed.remove(ind1))


    def get_random_individual(self):
        return random.choice(self._population)

    def runExperiment(self, horizon=100, display_status_count=False):

        for timestep in range(horizon):
            # Have interactions between individuals, make sick if needed.
            interactions = self.make_interactions()
            for ind1, ind2 in interactions:
                self.play_out_interaction(timestep, ind1, ind2)

            # Recover individuals
            for ind in self._sick:
                if timestep - (ind._sick_at_time + ind._time_to_recover) >= 0:
                    ind.make_recover(timestep)
                    self._sick.remove(ind)

            # Death of individuals
            for ind in self._sick:
                r = random.random()
                if r < ind._prob_death:
                    self._dead.append(self._sick.remove(ind))
                    ind.make_dead(timestep)

            if display_status_count:
                print(str(timestep) + ": " + str(self.population_status_count()))


if __name__ == '__main__':

    params = json.load(open('cold_spread.json'))

    pop = Population(params)

    pop.runExperiment(100, True)