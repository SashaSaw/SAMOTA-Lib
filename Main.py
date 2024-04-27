from src.samota import SAMOTA
from src.fitness_calculator import BeamngFitnessCalc
from src.global_search import GlobalSearch
from src.local_search import LocalSearch
from src.database import DatabaseManager
from src.surrogate_model import PolynomialRegression
from src.test_case import TestCase

if __name__ == '__main__':


    # samota = SAMOTA()
    fit = BeamngFitnessCalc("beamng")
    # fitness calculator = fit
    gs = GlobalSearch(PolynomialRegression(3), 2, [5, 5, 5], [195, 195, 195])
    # global search = gs, max iterations for global search = 2, lower boundaries are 5 and upper boundaries are 195
    ls = LocalSearch(PolynomialRegression(3), 2, 0.6, 2)
    # local search = ls, max iterations for local search = 2, percentage for training surrogate models is 0.6 (60%)
    # minimum number of test cases in cluster = 2
    db = DatabaseManager()
    # database = db
    samota = SAMOTA(fit, gs, ls, db)
    # max number of runs = 2, population size = 10, list of error thresholds is [0.1]
    archive, database = samota.samota(2, 10, [0.1])
    database.export_database("database")
    for tc in archive:
        tc = fit.calculate_fitness_sim([tc])
        print(tc[0].__str__())
