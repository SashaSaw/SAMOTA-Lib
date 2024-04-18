from matplotlib import pyplot as plt

from src.fitness_calculator import BeamngFitnessCalc
from src.test_case import TestCase
#from src import Database
from src.surrogate_model import polynomial_regression

if __name__ == '__main__':
    testcase1 = TestCase([[10, 10], [50, 50], [60, 60]], [0.7], [], [])
    testcase2 = TestCase([[10, 10], [50, 50], [5, 60]], [0.3], [], [])
    testcase3 = TestCase([[10, 10], [50, 50], [5, 150]], [0.5], [], [])
    test_cases = [testcase1,testcase2,testcase3]
    surrogate = polynomial_regression()
    surrogate.train(test_cases)
    surrogate.test()

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