from TestCase import TestCase

class FitnessCalculator:

    def __init__(self, simulator_name):
        self.simulator_name = simulator_name

    def calculateFitnessSim(self, test_cases) -> TestCase:
        """
        Takes the input testCases and computes the fitness scores by running the simulator.
        Then updates the fitness scores of the testCases.
        Returns the updated testCases
        :param testCases:
        :return set of TestCase:
        """