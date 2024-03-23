from typing import List

from Search import Search
from SurrogateModel import SurrogateModel
from TestCase import TestCase

class LocalSearch(Search):

    def __init__(self, database, objectives, max_iteration, percentage_local, min_per_cluster):
        super().__init__(database, objectives, max_iteration)
        self.percentage_local = percentage_local
        self.min_per_cluster = min_per_cluster

    def generateClusters(self, database, percentage_local, objective, min_per_cluster) -> set[set[TestCase]]:
        """given a database, a percentage for training surrogate models, an objective and a minimum number of test
        cases per cluster, this function generates a set of clusters with the minimum number of test cases in each
        cluster from the top percentage_local% of test cases in the database for the specified objective
        :param database:
        :param percentage_local:
        :param objective:
        :param min_per_cluster:
        :return: a set of clusters
        """


    def trainLocal(self, test_cases) -> SurrogateModel:
        """trains a surrogate model for the given cluster (set of test cases) and returns it
        :param test_cases:
        :return: a surrogate model
        """

    def calcFitnessLS(self, test_cases, local_surrogate) -> set[TestCase]:
        """this function calculates the (predicted) fitness scores of the given test cases using the give surrogate
        model
        :param test_cases:
        :param local_surrogate:
        :return:
        """



    def updateBestPredicted(self, best_predicted_testcase, test_cases) -> TestCase:
        """compares the fitness scores of the test cases in the set of test cases with the best predicted test case and
        returns the best test case.
        :param best_predicted_testcase:
        :param test_cases:
        :return: the best test case
        """


    def localSearch(self) -> list[TestCase]:
        test_cases = []
        for objective in range(self.objectives):
            clusters = self.generateClusters(self.database, self.percentage_local, objective, self.min_per_cluster)
            for cluster in clusters:
                surrogate_model = self.trainLocal(cluster)
                best_predicted_testcase = TestCase([])
                counter = 0
                while counter < self.max_iteration:
                    offspring = self.genOffspring(cluster)
                    updated_test_cases = self.calcFitnessLS(cluster+offspring, surrogate_model)
                    best_predicted_testcase = self.updateBestPredicted(best_predicted_testcase, updated_test_cases)
                    cluster = self.generateNextGen(updated_test_cases, self.objectives)
                    counter = counter + 1
                test_cases.append(best_predicted_testcase)
        return test_cases