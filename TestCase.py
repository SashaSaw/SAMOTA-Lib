from abc import ABC, abstractmethod

class TestCase(ABC):

    def __init__(self, representation, fitness_score_sim=-1, fitness_score_predicted=-1, uncertainty=-1):
        self.representation = representation
        self.fitness_score_sim = fitness_score_sim
        self.fitness_score_predicted = fitness_score_predicted
        self.uncertainty = uncertainty

    @abstractmethod
    def getTestCase(self):

    @abstractmethod
    def setTestCase(self):