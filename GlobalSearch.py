from Search import Search
from SurrogateModel import SurrogateModel
from TestCase import TestCase

class GlobalSearch(Search):

    def __init__(self, database, objectives, max_iteration, population_size, error_threshold):
        super().__init__(database, objectives, max_iteration)
        self.population_size = population_size
        self.error_threshold = error_threshold

    def initialPopulation(self, population_size) -> set[TestCase]:
        """generates a set of random test cases with an amount equal to population size
        :param population_size:
        :return: set of random test cases
        """

    def trainGlobal(self, database, uncovered_objectives) -> SurrogateModel:
        """trains a set of global surrogate models using all the test cases in D with the number of surrogate machines
        being equal to the number of uncovered objectives (one per uncovered objective)
        :param database:
        :param uncovered_objectives:
        :return: set of Global surrogates
        """

    def calcFitnessGS(self, test_cases, surrogates) -> set[TestCase]:
        """given a set of test cases this function calculates the predicted fitness scores and uncertainty of
        individual predictions then returning the resulting test cases.
        note: size of fitness scores list should be same as size of list of objectives.
        :param test_cases:
        :param surrogates:
        :return: set of test cases with updated fitness scores and uncertainty values
        """

    def update(self, best_tc, most_uncertain_tc, test_cases, uncovered_objectives, error_thresholds) -> (set[TestCase],set[TestCase],int):
        """updates best_tc so that it includes the best test case from the given set of test cases for each objective in
        uncovered_objectives, updates most_uncertain_tc so that it includes the most uncertain test case from the given
        set of test cases for each objective in uncovered_objectives and updates uncovered_objectives such that it
        excludes the objectives covered (achieved) by the test cases in the best_tc set.
        then returns the updated best_tc, most_uncertain_tc, and uncovered_objectives.
        :param best_tc:
        :param most_uncertain_tc:
        :param test_cases:
        :param uncovered_objectives:
        :param error_thresholds:
        :return: updated set of best test cases, set of most uncertain test cases, and uncovered objectives
        """

    def globalSearch(self):
