from matplotlib import pyplot as plt

from src.fitness_calculator import BeamngFitnessCalc
from src.test_case import TestCase
#from src import Database
import numpy as np
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import operator

if __name__ == '__main__':
    # Generate data
    np.random.seed(0)
    x = 2 - 3 * np.random.normal(0, 1, 20)
    y = x - 2 * (x ** 2) + 0.5 * (x ** 3) + np.random.normal(-3, 3, 20)
    x = x[:, np.newaxis]
    y = y[:, np.newaxis]

    # Polynomial features
    degree = 6
    poly_features = PolynomialFeatures(degree=degree)
    x_poly = poly_features.fit_transform(x)

    # Regression model
    model = LinearRegression()
    model.fit(x_poly, y)
    y_poly_pred = model.predict(x_poly)

    # Evaluation
    rmse = np.sqrt(mean_squared_error(y, y_poly_pred))
    r2 = r2_score(y, y_poly_pred)
    print(f"Root Mean Squared Error: {rmse}")
    print(f"R^2 Score: {r2}")

    # Plot
    sort_axis = operator.itemgetter(0)
    sorted_zip = sorted(zip(x, y_poly_pred), key=sort_axis)
    x, y_poly_pred = zip(*sorted_zip)

    plt.scatter(x, y, color='red')
    plt.plot(x, y_poly_pred, color='blue')
    plt.title('Polynomial Regression')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

    #fit = BeamngFitnessCalc("Beamng")
    #testcase1 = TestCase([[10, 10], [50, 50], [60, 60]], [], [], [])
    #testcase2 = TestCase([[10, 10], [50, 50], [5, 60]], [], [], [])
    #testcase3 = TestCase([[10, 10], [50, 50], [5, 150]], [], [], [])
    #test_cases = fit.calculateFitnessSim([testcase1, testcase2])
    #for test_case in test_cases:
    #    rep = str(test_case.get_representation())
    #    fit = str(test_case.get_fitness_score_sim())
    #    print("rep: "+ rep + "fit: " + fit)

    #database = Database()
    # database.setDefaultDatabase()
    #database.loadDatabase("Test")
    #database.exportDatabase("Database")