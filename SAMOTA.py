from GlobalSearch import GlobalSearch
from LocalSearch import LocalSearch
from FitnessCalculator import FitnessCalculator
from TestCase import TestCase


class SAMOTA:

    def __init__(self, objectives, population_size, error_threshold, global_max_iter, local_max_iter, percentage_local,
                 min_per_cluster, database):
        self.objectives = objectives
        self.population_size = population_size
        self.error_threshold = error_threshold
        self.global_max_iter = global_max_iter
        self.local_max_iter = local_max_iter
        self.percentage_local = percentage_local
        self.min_per_cluster = min_per_cluster
        self.database = database

    def updateArchive(self, archive, test_cases, error_threshold, objectives) -> TestCase:

    def samota(self, num_of_runs):
        global_search = GlobalSearch(self.population_size, self.error_threshold)
        local_search = LocalSearch(self.percentage_local, self.min_per_cluster)
        fitness_calculator = FitnessCalculator("Simulator")
        archive = [] #TODO
        uncovered_objectives = 3 #TODO
        test_cases = global_search.initialPopulation()
        test_cases = fitness_calculator(test_cases)
        archive, uncovered_objectives = self.updateArchive(archive, test_cases, self.error_threshold, self.objectives)
        database = self.database.updateDatabase(self.database, test_cases)
        while(num_of_runs != 0):
            global_test_cases = global_search.globalSearch()
            global_test_cases = fitness_calculator.calculateFitnessSim(global_test_cases)
            archive, uncovered_objectives = self.updateArchive(archive, global_test_cases, self.error_threshold, self.objectives)
            database = self.database.updateDatabase(database, global_test_cases)
            local_test_cases = local_search.localSearch()
            local_test_cases = fitness_calculator.calculateFitnessSim(local_test_cases)
            archive, uncovered_objectives = self.updateArchive(archive, local_test_cases, self.error_threshold, self.objectives)
            database = self.database.updateDatabase(database, local_test_cases)
        return archive, database