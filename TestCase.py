from abc import ABC, abstractmethod

class TestCase(ABC):

    def __init__(self, representation, fitnessScore):
        self.representation = representation
        self.fitnessScore = fitnessScore

    @abstractmethod
    def getTestCase(self):

    @abstractmethod
    def setTestCase(self):