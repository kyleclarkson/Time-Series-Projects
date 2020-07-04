
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

    __slots__ = '_isSick', '_sickAtTime'

    def __init__(self):
        self._isSick = False
        self._sickAtTime = -1

class Population:

    __slots__ = '_population'

    def __init__(self, numOfIndividuals):

        # Create population of individuals.
        self._population = []

        for index in range(numOfIndividuals):
            self._population.append(Individual())

    def runExperiment(self):
        pass

if __name__ == '__main__':
    pass
