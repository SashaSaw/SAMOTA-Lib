from TestCase import TestCase

class Search:

    def __init__(self, database, objectives, max_iteration):
        self.database = database
        self.objectives = objectives
        self.max_iteration = max_iteration

    def genOffspring(self, test_cases) -> set[TestCase]:
        """Takes a set of test cases and generates offspring (applies algorithm to the testcases)
        then returns the resulting offspring test_cases
        :param test_cases:
        :return: offspring test cases
        """

    def generateNextGen(self, test_cases, uncovered_objectives) -> set[TestCase]:
        """Implements tournament selection in order to select the next generation of test cases in the genetic algorithm
        note: the function aims to reduce the population size (num of test cases in next gen) to |U|
        :param test_cases:
        :param uncovered_objectives:
        :return: the next generation of test cases
        """

