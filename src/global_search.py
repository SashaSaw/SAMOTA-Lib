from src.search import Search
from random import randint
from src.test_case import TestCase

class GlobalSearch(Search):

    def __init__(self, map_size, surrogate):
        super().__init__(map_size, surrogate)

    def initial_population(self, population_size):
        """generates a set of random test cases with an amount equal to population size
        :param population_size:
        :return: set of random test cases
        """
        print("creating initial population...")
        population = []
        for i in range(population_size):
            road_points = []
            for i in range(0, 3):
                road_points.append([randint(0, self.map_size), randint(0, self.map_size)])
            test_case = TestCase(road_points, [], [], [])
            population.append(test_case)
        return population

    def train_globals(self, database, uncovered_objectives):
        """trains a set of global surrogate models using all the test cases in D with the number of surrogate machines
        being equal to the number of uncovered objectives (one per uncovered objective)
        :param database:
        :param uncovered_objectives:
        :param surrogate_model:
        :return: set of Global surrogates
        """
        print("training global surrogate models...")
        test_cases = database.get_database()
        test_cases_per_objective = []
        # for each objective get a set of test cases that satisfy that objective
        for i in range (len(uncovered_objectives)):
            test_cases_singleobj = []
            for test_case in test_cases:
                temp_test_case = TestCase(test_case.get_representation(),
                                          [test_case.get_fitness_score_sim()[i]],
                                          test_case.get_fitness_score_predicted(),
                                          test_case.get_uncertainty())
                test_cases_singleobj.append(temp_test_case)
            # append each set of test cases with only the fitness score for a specific objective
            test_cases_per_objective.append(test_cases_singleobj)

        surrogate_models = []
        # for each set of test cases that satisfy an uncovered objective train a surrogate model
        for test_cases_singleobj in test_cases_per_objective:
            temp_surrogate = self.surrogate
            temp_surrogate.train(test_cases_singleobj)
            surrogate_models.append(temp_surrogate)
        return surrogate_models

    def calc_fitness_gs(self, test_cases, surrogates):
        """given a set of test cases this function calculates the predicted fitness scores and uncertainty of
        individual predictions then returning the resulting test cases.
        note: size of fitness scores list should be same as size of list of objectives.
        :param test_cases:
        :param surrogates:
        :return: set of test cases with updated fitness scores and uncertainty values
        """
        print("predicting fitness scores...")
        output = []
        for test_case in test_cases:
            fit_scores_predicted = []
            for surrogate in surrogates:
                fit_score_predicted = surrogate.predict(test_case.flatten_representation())
                fit_scores_predicted.append(fit_score_predicted)
            test_case.set_fitness_score_predicted(fit_scores_predicted)
            output.append(test_case)
        return output
        #for most_uncertain you can use multiple surrogate models to predict the fitness score and compare their results,
        #similar results = low uncertainty and different results = high uncertainty



    def update(self, test_cases, uncovered_objectives, error_thresholds):
        """updates best_tc so that it includes the best test case from the given set of test cases for each objective in
        uncovered_objectives, updates most_uncertain_tc so that it includes the most uncertain test case from the given
        set of test cases for each objective in uncovered_objectives and updates uncovered_objectives such that it
        excludes the objectives covered (achieved) by the test cases in the best_tc set.
        then returns the updated best_tc, most_uncertain_tc, and uncovered_objectives.
        :param test_cases:
        :param uncovered_objectives:
        :param error_thresholds:
        :return: updated set of best test cases, set of most uncertain test cases, and uncovered objectives
        """
        print("updating best test case and uncovered objectives...")
        updated_uncovered_objectives = [False] * len(uncovered_objectives)
        updated_best_tcs = [None] * len(uncovered_objectives)
        # for each objective
        for i in range(len(uncovered_objectives)):
            # if objective is already satisfied replace best test case for objective if a better objective is found
            if uncovered_objectives[i]:
                updated_uncovered_objectives[i] = True
                highest_fitness = 0
                for test_case in test_cases:
                    fitness_predicted = test_case.get_fitness_score_predicted()[i]
                    if fitness_predicted > highest_fitness:
                        highest_fitness = fitness_predicted
                        updated_best_tcs[i] = test_case
            # if objective not satisfied yet then find best test case for objective
            # if best test case fitness score is larger than threshold then set uncovered objective to satisfied
            elif not uncovered_objectives[i]:
                highest_fitness = -1
                for test_case in test_cases:
                    fitness_predicted = test_case.get_fitness_score_predicted()[i]
                    if fitness_predicted > highest_fitness:
                        highest_fitness = fitness_predicted
                        updated_best_tcs[i] = test_case
                if highest_fitness > error_thresholds[i]:
                    updated_uncovered_objectives[i] = True

        return updated_best_tcs, updated_uncovered_objectives



        #instead of acc calculating most_uncertain just return a random candidate for now

    def global_search(self, database, uncovered_obj, pop_size, max_iteration, error_thresholds):
        print(" *** starting global search ***")
        global_surrogates = self.train_globals(database, uncovered_obj)
        best_tcs = []
        counter = 0
        test_cases = self.initial_population(pop_size)
        while counter < max_iteration:
            offspring = self.gen_offspring(test_cases)
            updated_tcs = self.calc_fitness_gs(test_cases + offspring, global_surrogates)
            best_tcs, uncovered_obj = self.update(best_tcs + updated_tcs, uncovered_obj, error_thresholds)
            test_cases = self.generate_next_gen(updated_tcs, uncovered_obj)
            counter = counter + 1
        print(" *** global search concluded *** ")
        return best_tcs #+ most_uncertain_tc
