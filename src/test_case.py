from random import randint
def create_tc():
    representation = []
    for index in range(0, 3):
        representation.append([randint(5, 195),
                               randint(5, 195)])
    test_case = TestCase(representation, [], [], [])
    return test_case

class TestCase():

    def __init__(self, representation=[], fitness_scores_sim=[], fitness_scores_predicted=[], uncertainties=[]):
        self.representation = representation
        self.fitness_score_sim = fitness_scores_sim
        self.fitness_score_predicted = fitness_scores_predicted
        self.uncertainty = uncertainties

    def __str__(self):
        return f"rep: {self.representation}, fit_sim: {self.fitness_score_sim}, fit_pred: {self.fitness_score_predicted}, uncert: {self.uncertainty}"

    def get_representation(self):
        return self.representation

    def flatten_representation(self):
        representation = self.get_representation()
        flat_rep = []
        for i in range(len(representation)):
            for j in range(len(representation[i])):
                flat_rep.append(representation[i][j])
        return flat_rep

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