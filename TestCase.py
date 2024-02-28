from abc import ABC, abstractmethod

class TestCase(ABC):

    def __init__(self, representation, fitness_score):
        self.representation = representation
        self.fitness_score = fitness_score

    @abstractmethod
    def getTestCase(self):

    @abstractmethod
    def setTestCase(self):