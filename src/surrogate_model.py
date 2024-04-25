from abc import ABC, abstractmethod
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


class AbstractSurrogateModel(ABC):

    @abstractmethod
    def train(self, test_cases):
        pass

    @abstractmethod
    def predict(self, test_cases):
        pass

class polynomial_regression(AbstractSurrogateModel):

    def __init__(self, degree=2):
        self.degree = degree
        self.model = LinearRegression()
        self.X_test = []
        self.y_test = []

    def train(self, test_cases):
        print("training PR model")
        x = []
        y = []
        for test_case in test_cases:
            sample = test_case.flatten_representation()
            x.append(sample)
            fitness_score_sim = test_case.get_fitness_score_sim()[0]
            y.append(fitness_score_sim)
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
        self.X_test = X_test
        self.y_test = y_test
        self.model = make_pipeline(PolynomialFeatures(self.degree), LinearRegression())
        self.model.fit(X_train, y_train)

    def test(self):
        predict = self.model.predict(self.X_test)
        print (predict)
        mse = mean_squared_error(self.y_test, predict)
        print(f'Mean Squared Error: {mse}')
        return mse

    def predict(self, testcase):
        print("predicting using PR model")
        prediction = self.model.predict(self.X_test)
        return prediction[0]
