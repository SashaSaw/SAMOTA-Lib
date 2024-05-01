from src.samota import SAMOTA
from src.fitness_calculator import BeamngFitnessCalc
from src.global_search import GlobalSearch
from src.local_search import LocalSearch
from src.database import DatabaseManager
from src.surrogate_model import PolynomialRegression
from src.test_case import TestCase
from random import randint
import time


def run_random_vs_samota(num_of_runs):
    for i in range(0, num_of_runs):
        archive, database = samota.samota(100, 4, [0.1])
        samotaresultsdb.update_database(archive)
        print(samotaresultsdb.get_database())
        samotaresultsdb.export_database("samota_results")
        print("exporting samota results")
        best_tc = random(fit)
        randomresultsdb.update_database([best_tc])
        randomresultsdb.export_database("random_results")
        print("exporting random results")
    database.export_database("database")


def random(fit):
    start_time = time.time()
    time_limit = 1800
    best_tc = TestCase([[0, 0], [0, 0], [0, 0]], [0], [], [])
    while (time.time() - start_time < time_limit):
        road_points = []
        for index in range(0, 3):
            road_points.append([randint(5, 195),
                                randint(5, 195)])
        test_case = TestCase(road_points, [], [], [])
        test_case = fit.calculate_fitness_sim([test_case])[0]
        if test_case.get_fitness_score_sim()[0] > best_tc.get_fitness_score_sim()[0]:
            best_tc = test_case
    return best_tc

def create_tc():
    representation = []
    for index in range(0, 3):
        representation.append([randint(5, 195),
                               randint(5, 195)])
    test_case = TestCase(representation, [], [], [])
    return test_case


if __name__ == '__main__':

    # samota = SAMOTA()
    fit = BeamngFitnessCalc("beamng")
    # fitness calculator = fit
    gs = GlobalSearch(PolynomialRegression(3), 2, create_tc)
    # global search = gs, max iterations for global search = 2, create_tc function is create_tc
    ls = LocalSearch(PolynomialRegression(3), 2, 0.1, 2)
    # local search = ls, max iterations for local search = 2, percentage for training surrogate models is 0.6 (60%)
    # minimum number of test cases in cluster = 2
    db = DatabaseManager()
    db.load_database("database")
    # database = db

    samotaresultsdb = DatabaseManager()
    randomresultsdb = DatabaseManager()

    samota = SAMOTA(fit, gs, ls, db)
    # max number of runs = 2, population size = 10, list of error thresholds is [0.1], time limit in seconds = 1000
    archive, database = samota.samota(2, 4, [0.1], 1000)
    for tc in archive:
        print(tc.__str__())
    database.export_database("database")


