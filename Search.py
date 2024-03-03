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
        """generates the next generation of test cases from the input test cases for the objectives?
        :param test_cases:
        :param uncovered_objectives:
        :return: the next generation of test cases
        """

