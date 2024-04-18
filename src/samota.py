from global_search import GlobalSearch
from local_search import LocalSearch
from fitness_calculator import FitnessCalculator
from test_case import TestCase


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

    def update_archive(self, archive, population, error_thresholds, uncovered_obj, num_of_obj) -> (set[TestCase], int):
        """given a set of test cases that satisfy some objectives(archive), a set of test cases generated randomly that
        have been run on the simulator, set of error thresholds and set of objectives, this function updates the archive
        to include test cases from the input archive and the input set of test cases and calculates uncovered objectives
        by excluding objectives that are still not covered (achieved) by the input test cases with respect to the given
        error thresholds.
        Note: update archive aims to achieve the min num of test cases to cover maximum number of objectives
        :param archive:
        :param test_cases:
        :param error_thresholds:
        :param objectives:
        :return: updated set of uncovered objectives and updated archive
        """
        for objective_index in range(num_of_obj):
            for pop_index in range(len(population)):
                objective_values = population[pop_index].get_objective_values


    def samota(self, num_of_runs, map_size):
        global_search = GlobalSearch(self.population_size, self.error_threshold)
        local_search = LocalSearch(self.percentage_local, self.min_per_cluster)
        fitness_calculator = FitnessCalculator("Simulator")
        archive = []
        test_cases = global_search.initial_population()
        test_cases = fitness_calculator(test_cases)
        archive, uncovered_objectives = self.update_archive(archive, test_cases, self.error_threshold, self.objectives)
        database = self.database.update_database(self.database, test_cases)
        while(num_of_runs != 0):
            global_test_cases = global_search.global_search()
            global_test_cases = fitness_calculator.calculateFitnessSim(global_test_cases)
            archive, uncovered_objectives = self.update_archive(archive, global_test_cases, self.error_threshold, self.objectives)
            database = self.database.update_database(database, global_test_cases)
            local_test_cases = local_search.local_search()
            local_test_cases = fitness_calculator.calculateFitnessSim(local_test_cases)
            archive, uncovered_objectives = self.update_archive(archive, local_test_cases, self.error_threshold, self.objectives)
            database = self.database.update_database(database, local_test_cases)
            num_of_runs = num_of_runs - 1
        return archive, database