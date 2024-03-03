from Search import Search
from TestCase import TestCase

class LocalSearch(Search):

    def __init__(self, percentage_local, min_per_cluster):
        self.percentage_local = percentage_local
        self.min_per_cluster = min_per_cluster

    def generateClusters(self, database, percentage_local, objective, min_per_cluster) -> set[TestCase]:
        """given a database, a percentage for training surrogate models, an objective and a minimum number of test
        cases per cluster, this function generates a set of clusters with the minimum number of test cases in each
        cluster from the top percentage_local% of test cases in the database for the specified objective
        :param database:
        :param percentage_local:
        :param objective:
        :param min_per_cluster:
        :return: a set of clusters
        """
        return


    def trainLocal(self, test_cases) -> "TODO":
        """trains a surrogate model for the given cluster (set of test cases) and returns it
        :param test_cases:
        :return: a surrogate model
        """
        return

    def calcFitnessLS(self):


    def updateBestPredicted(self, best_predicted_testcase, test_cases) -> TestCase:
        """compares the fitness scores of the test cases in the set of test cases with the best predicted test case and
        returns the best test case.
        :param best_predicted_testcase:
        :param test_cases:
        :return: the best test case
        """


    def localSearch(self):