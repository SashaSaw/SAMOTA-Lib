from src.FitnessCalculator import FitnessCalculator
from src.TestCase import TestCase
#from src import Database

if __name__ == '__main__':
    fit = FitnessCalculator("Beamng")
    testcase1 = TestCase([[10, 10], [50, 50], [60, 60]], [], [], [])
    testcase2 = TestCase([[10, 10], [50, 50], [5, 60]], [], [], [])
    testcase3 = TestCase([[10, 10], [50, 50], [5, 150]], [], [], [])
    test_cases = fit.calculateFitnessSim([testcase1, testcase2])
    for test_case in test_cases:
        rep = str(test_case.get_representation())
        fit = str(test_case.get_fitness_score_sim())
        print("rep: "+ rep + "fit: " + fit)

    #database = Database()
    # database.setDefaultDatabase()
    #database.loadDatabase("Test")
    #database.exportDatabase("Database")