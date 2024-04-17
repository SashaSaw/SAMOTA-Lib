from abc import ABC, abstractmethod


class TestCase(ABC):

    def __init__(self, representation, fitness_scores_sim, fitness_scores_predicted, uncertainties):
        self.representation = representation
        self.fitness_score_sim = fitness_scores_sim
        self.fitness_score_predicted = fitness_scores_predicted
        self.uncertainty = uncertainties

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