from abc import ABC, abstractmethod
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import operator

class AbstractSurrogateModel(ABC):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def train(self, x, y):
        pass

    @abstractmethod
    def predict(self, x):
        pass

class polynomial_regression(AbstractSurrogateModel):

    def train(self, x, y):

    def predict(self, x):

