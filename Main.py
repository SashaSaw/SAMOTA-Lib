from matplotlib import pyplot as plt
from src.samota import SAMOTA
from src.fitness_calculator import BeamngFitnessCalc
from src.global_search import GlobalSearch
from src.local_search import LocalSearch
from src.database import DatabaseManager
from src.test_case import TestCase
#from src import Database
from src.surrogate_model import PolynomialRegression

if __name__ == '__main__':


    samota = SAMOTA()
    fit = BeamngFitnessCalc("beamng")
    gs = GlobalSearch(200, PolynomialRegression(3))
    ls = LocalSearch(200, PolynomialRegression(3))
    db = DatabaseManager()
    archive, database = samota.samota(2, 10, [0.1], fit, gs, 2, ls, 2, 0.6, 2, db)
    database.export_database("database")
    for tc in archive:
        print(tc.__str__())

    #testcase2 = TestCase([[20, 20], [20, 80], [100, 100]], [], [], [])
    #testcase3 = TestCase([[20, 20], [20, 80], [20, 100]], [], [], [])
    #test_cases = [testcase1,testcase2,testcase3]
    #fit = BeamngFitnessCalc("beamng")
    #test_cases = fit.calculate_fitness_sim(test_cases)
    #surrogate = polynomial_regression(3)
    #surrogate.train(test_cases)
    #surrogate.test()

    #fit = BeamngFitnessCalc("Beamng")
    #testcase1 = TestCase([[10, 10], [50, 50], [60, 60]], [], [], [])
    #testcase2 = TestCase([[10, 10], [50, 50], [5, 60]], [], [], [])
    #testcase3 = TestCase([[10, 10], [50, 50], [5, 150]], [], [], [])
    #test_cases = fit.calculateFitnessSim([testcase1, testcase2, testcase3])
    #for test_case in test_cases:
     #   rep = str(test_case.get_representation())
      #  fit = str(test_case.get_fitness_score_sim())
       # print("rep: "+ rep + "fit: " + fit)

    #database = Database()
    # database.setDefaultDatabase()
    #database.loadDatabase("Test")
    #database.exportDatabase("Database")