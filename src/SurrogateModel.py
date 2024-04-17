from abc import ABC, abstractmethod

class SurrogateModel(ABC):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def train(self, x, y):
        pass

    @abstractmethod
    def predict(self, x):
        pass

