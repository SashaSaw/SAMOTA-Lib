from typing import List

from search import Search
from src.surrogate_model import polynomial_regression
from test_case import TestCase

class LocalSearch(Search):

    def __init__(self, database, objectives, max_iteration, percentage_local, min_per_cluster):
        super().__init__(database, objectives, max_iteration)
        self.percentage_local = percentage_local
        self.min_per_cluster = min_per_cluster

    def generate_clusters(self, database, percentage_local, objective, min_per_cluster) -> set[set[TestCase]]:
        """given a database, a percentage for training surrogate models, an objective and a minimum number of test
        cases per cluster, this function generates a set of clusters with the minimum number of test cases in each
        cluster from the top percentage_local% of test cases in the database for the specified objective
        :param database:
        :param percentage_local:
        :param objective:
        :param min_per_cluster:
        :return: a set of clusters
        """
        #take database - for each objective select the top (percentage_local- user provided) test cases highest fitness scores for that objective
        # do clustering sklearn.cluster.hdbscan - in python library (look at SAMOTA package) takes in min number per cluster
        # hsbdscan needs to take database of test cases as [[x1,x2,x3,...,x6],...] and the function for calc distnace between test cases needs to be defined (or just use euclidean and see

    def train_local(self, test_cases):
        """trains a surrogate model for the given cluster (set of test cases) and returns it
        :param test_cases:
        :return: a surrogate model
        """

    def calc_fitness_ls(self, test_cases, local_surrogate) -> set[TestCase]:
        """this function calculates the (predicted) fitness scores of the given test cases using the give surrogate
        model
        :param test_cases:
        :param local_surrogate:
        :return:
        """

    def update_best_predicted(self, best_predicted_testcase, test_cases) -> TestCase:
        """compares the fitness scores of the test cases in the set of test cases with the best predicted test case and
        returns the best test case.
        :param best_predicted_testcase:
        :param test_cases:
        :return: the best test case
        """


    def local_search(self):
        test_cases = []
        for objective in range(self.objectives):
            clusters = self.generate_clusters(self.database, self.percentage_local, objective, self.min_per_cluster)
            for cluster in clusters:
                surrogate_model = self.train_local(cluster)
                best_predicted_testcase = TestCase([])
                counter = 0
                while counter < self.max_iteration:
                    offspring = self.gen_offspring(cluster)
                    updated_test_cases = self.calc_fitness_ls(cluster + offspring, surrogate_model)
                    best_predicted_testcase = self.update_best_predicted(best_predicted_testcase, updated_test_cases)
                    cluster = self.generate_next_gen(updated_test_cases, self.objectives)
                    counter = counter + 1
                test_cases.append(best_predicted_testcase)
        return test_cases