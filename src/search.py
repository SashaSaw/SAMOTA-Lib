import numpy as np
from src.test_case import TestCase
import random

class Search:

    def __init__(self, map_size):
        self.map_size = map_size

    def gen_offspring(self, test_cases):
        """Takes a set of test cases and generates offspring (applies algorithm to the testcases)
        then returns the resulting offspring test_cases
        :param test_cases:
        :return: offspring test cases
        """
        # initialise the set of mutated test cases
        mutated_test_cases = []
        for test_case in test_cases:
            mutated_representation = []
            # get the representation of the test case as a 1D list
            representation = test_case.flatten_representation()
            # for each element there is a 50% chance it is mutated
            for element in representation:
                mutated_representation.append(self.mutate(element, 0, 200, 5, 0.5))
            # mutated representation is turned back into its original form
            unflattened_rep = np.array(mutated_representation).reshape(-1, 2)
            # create a test case that represents the mutated version of original test case
            temp_tc = TestCase(unflattened_rep,
                               test_case.get_fitness_score_sim,
                               test_case.get_fitness_score_predicted,
                               test_case.get_uncertainty)
            mutated_test_cases.append(temp_tc)

        # initialise the set of test cases that have been crossed over
        crossed_test_cases = []
        # for each two test cases in the mutated test cases list perform crossover
        for i in range(0, len(mutated_test_cases), 2):
            if i+1 < len(mutated_test_cases):
                first_tc = mutated_test_cases[i]
                second_tc = mutated_test_cases[i+1]
                first_tc_crossed, second_tc_crossed = self.uniform_crossover(first_tc, second_tc, 0.7)
                crossed_test_cases.append(first_tc_crossed)
                crossed_test_cases.append(second_tc_crossed)
            else:
                crossed_test_cases.append(mutated_test_cases[i])
        return crossed_test_cases

    def generate_next_gen(self, test_cases, uncovered_objectives):
        """Implements tournament selection in order to select the next generation of test cases in the genetic algorithm
        note: the function aims to reduce the population size (num of test cases in next gen) to |U|
        :param test_cases:
        :param uncovered_objectives:
        :return: the next generation of test cases
        """
        output_test_cases = []
        # count number of uncovered_objectives there are
        num_uncovered_obj = uncovered_objectives.count(False)
        if num_uncovered_obj > 0:
            # for each uncovered_objective use tournament selection to select a good test case that covers it
            for i in range(len(uncovered_objectives)):
                if not uncovered_objectives[i]:
                    test_case = self.tournament_selection(test_cases, 1, i)
                    output_test_cases.append(test_case)
        else:
            output_test_cases = test_cases
        return output_test_cases

    def tournament_selection(self, population, tournament_size, index):
        best = random.choice(population)
        population.remove(best)
        for i in range (2, tournament_size):
            next = random.choice(population)
            population.remove(next)
            if best.get_fitness_predicted()[index] < next.get_fitness_predicted()[index]:
                best = next
        return best

    def mutate(self, number, lower_boundary, upper_boundary, percentage_mutation, probability):
        percentage_mutation = percentage_mutation/100
        mutation_amount = round(percentage_mutation * number)
        random_num = random.random()
        output = number
        if random_num > probability or (number + mutation_amount) >= upper_boundary:
            output = number - mutation_amount
        elif random_num <= probability or (number - mutation_amount) <= lower_boundary:
            output = number + mutation_amount
        return output

    def uniform_crossover(self, first_tc, second_tc, probability):
        first_representation = first_tc.flatten_representation()
        second_representation = second_tc.flatten_representation()
        for i in range(len(first_representation)):
            if probability >= random.random():
                temp = first_representation[i]
                first_representation[i] = second_representation[i]
                second_representation[i] = temp
        output_tc_1 = TestCase(np.array(first_representation).reshape(-1, 2),
                               first_tc.get_fitness_score_sim(),
                               first_tc.get_fitness_score_predicted(),
                               first_tc.get_uncertainty())
        output_tc_2 = TestCase(np.array(second_representation).reshape(-1, 2),
                               second_tc.get_fitness_score_sim(),
                               second_tc.get_fitness_score_predicted(),
                               second_tc.get_uncertainty())
        return output_tc_1, output_tc_2