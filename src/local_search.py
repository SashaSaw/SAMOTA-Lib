from typing import List
import heapq
from sklearn.cluster import HDBSCAN
from src.search import Search
from src.test_case import TestCase

class LocalSearch(Search):

    def __init__(self, map_size, surrogate):
        super().__init__(map_size, surrogate)

    def generate_clusters(self, database, percentage_local, objective, index, min_per_cluster):
        """given a database, a percentage for training surrogate models, an objective and a minimum number of test
        cases per cluster, this function generates a set of clusters with the minimum number of test cases in each
        cluster from the top percentage_local% of test cases in the database for the specified objective
        note: percentage local must be a decimal. e.g. 50% = 0.5
        :param database:
        :param percentage_local:
        :param uncovered_objectives:
        :param min_per_cluster:
        :return: a set of clusters
        """
        print("generating clusters...")
        # create a set of test_cases from the database that have the top percentage_local fitness scores
        total_num_tcs = len(database.get_database())
        num_of_top_tcs = round(total_num_tcs * percentage_local)
        top_tcs = self.top_n_test_cases(database.get_database(), num_of_top_tcs, index)

        # get the test cases flattened representation and fit them to the clustering algorithm
        hdb = HDBSCAN(min_cluster_size=min_per_cluster)
        top_tcs_representations = []
        for tc in top_tcs:
            top_tcs_representations.append(tc.flatten_representation())
        hdb.fit(top_tcs_representations)

        # create sets of test cases (clusters) based on their labels in the labels list (doesn't include outliers)
        labels = hdb.labels_
        clusters = []
        for i in range(max(labels)):
            cluster = self.create_cluster(labels, top_tcs, i)
            clusters.append(cluster)
        return clusters


        #take database - for each objective select the top (percentage_local- user provided) test cases highest fitness scores for that objective
        # do clustering sklearn.cluster.hdbscan - in python library (look at SAMOTA package) takes in min number per cluster
        # hsbdscan needs to take database of test cases as [[x1,x2,x3,...,x6],...] and the function for calc distnace between test cases needs to be defined (or just use euclidean and see

    def create_cluster(self, labels, test_cases, label):
        cluster = []
        for i in range(len(labels)):
            if labels[i] == label:
                cluster.append(test_cases[i])
        return cluster

    def top_n_test_cases(self, test_cases, n, index):
        return heapq.nlargest(n, test_cases, key=lambda test_case: test_case.get_fitness_score_sim()[index])

    def train_local(self, test_cases):
        """trains a surrogate model for the given cluster (set of test cases) and returns it
        :param test_cases:
        :return: a surrogate model
        """
        print("training local surrogate model...")
        surrogate_model = self.surrogate
        surrogate_model.train(test_cases)
        return surrogate_model


    def calc_fitness_ls(self, test_cases, local_surrogate, index):
        """this function calculates the (predicted) fitness scores of the given test cases using the give surrogate
        model
        :param test_cases:
        :param local_surrogate:
        :return: updated_test_cases
        """
        print("calculating fitnesses...")
        updated_test_cases = []
        for test_case in test_cases:
            new_fit_score_predicted = local_surrogate.predict(test_case.flatten_representation())
            predicted_fit_scores = test_case.get_fitness_score_predicted()
            if len(predicted_fit_scores) < index+1:
                predicted_fit_scores.append(new_fit_score_predicted)
            else:
                predicted_fit_scores[index] = new_fit_score_predicted
            updated_tc = TestCase(test_case.get_representation(),
                                  test_case.get_fitness_score_sim(),
                                  predicted_fit_scores,
                                  test_case.get_uncertainty())
            updated_test_cases.append(updated_tc)
        return updated_test_cases

    def update_best_predicted(self, best_predicted_testcase, test_cases, index):
        """compares the fitness scores of the test cases in the set of test cases with the best predicted test case and
        returns the best test case.
        :param best_predicted_testcase:
        :param test_cases:
        :return: the best test case
        """
        print("updating best predicted test case...")
        best_fit_score = 0
        all_test_cases = [best_predicted_testcase] + test_cases
        for test_case in all_test_cases:
            if test_case is not None:
                if test_case.get_fitness_score_predicted()[index] > best_fit_score:
                    best_predicted_testcase = test_case
        return best_predicted_testcase


    def local_search(self, database, uncovered_obj, max_iteration, percentage_local, min_per_cluster):
        print(" *** starting local search ***")
        test_cases = []
        for i in range(len(uncovered_obj)):
            objective = uncovered_obj[i]
            clusters = self.generate_clusters(database, percentage_local, objective, i, min_per_cluster)
            for cluster in clusters:
                surrogate_model = self.train_local(cluster)
                best_predicted_testcase = None
                counter = 0
                while counter < max_iteration:
                    offspring = self.gen_offspring(cluster)
                    updated_tcs = self.calc_fitness_ls(cluster + offspring, surrogate_model, i)
                    best_predicted_testcase = self.update_best_predicted(best_predicted_testcase, updated_tcs, i)
                    cluster = self.generate_next_gen(updated_tcs, uncovered_obj)
                    counter = counter + 1
                test_cases.append(best_predicted_testcase)
        print(" *** local search concluded ***")
        return test_cases