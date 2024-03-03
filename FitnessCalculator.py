from TestCase import TestCase

class FitnessCalculator:

    def __init__(self, simulator_name):
        self.simulator_name = simulator_name

    def calculateFitnessSim(self, test_cases) -> set[TestCase]:
        """Takes the input test cases and computes the fitness scores by running the simulator.
        Then updates the fitness scores of the test cases and returns the updated test cases
        :param test_cases:
        :return: set of TestCases with updated fitness scores
        """