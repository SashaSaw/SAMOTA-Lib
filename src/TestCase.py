from abc import ABC, abstractmethod


class TestCase(ABC):

    def __init__(self, representation=[(), (), ()], fitness_score_sim=-1, fitness_score_predicted=-1, uncertainty=-1):
        self.representation = representation
        self.fitness_score_sim = fitness_score_sim
        self.fitness_score_predicted = fitness_score_predicted
        self.uncertainty = uncertainty

    def get_representation(self):
        return self.representation

    def get_fitness_score_sim(self):
        return self.fitness_score_sim

    def set_fitness_score_sim(self, new_fitness_score):
        self.fitness_score_sim = new_fitness_score

    def get_fitness_score_predicted(self):
        return self.fitness_score_predicted

    def set_fitness_score_predicted(self, new_fitness_score):
        self.fitness_score_predicted = new_fitness_score
    def get_uncertainty(self):
        return self.uncertainty

    def set_uncertainty(self, new_uncertainty):
        self.uncertainty = new_uncertainty