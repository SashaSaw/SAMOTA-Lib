import unittest
from src.fitness_calculator import BeamngFitnessCalc
from src.test_case import TestCase

class TestFitnessCalc(unittest.TestCase):

    def setUp(self):
        self.fitness_calc = BeamngFitnessCalc("Beamng")
        self.testcase1 = TestCase([[20, 20], [20, 50], [23, 100]], [], [], [])
        self.testcase2 = TestCase([[20, 20], [20, 80], [100, 100]], [], [], [])
        self.testcase2 = TestCase([[20, 20], [20, 80], [20, 100]], [], [], [])
        self.testcases = [self.testcase1, self.testcase2]

    def test_straightvscurve(self):
        testcases_updated = self.fitness_calc.calculateFitnessSim(self.testcases)
        fitness1 = testcases_updated[2].get_fitness_score_sim()[0]
        fitness2 = testcases_updated[1].get_fitness_score_sim()[0]
        print("straight: "+ str(fitness1))
        print("curve: "+ str(fitness2))
        self.assertGreater(fitness1, fitness2, "fitness score for a straight test case should be higher than that of a curved test case")

    def test_bigvssmallcurve(self):
        testcases_updated = self.fitness_calc.calculateFitnessSim(self.testcases)
        fitness1 = testcases_updated[1].get_fitness_score_sim()[0]
        fitness2 = testcases_updated[0].get_fitness_score_sim()[0]
        print("big curve: "+ str(fitness1))
        print("small curve: "+ str(fitness2))
        self.assertGreater(fitness1, fitness2, "fitness score for smaller curve test case should be higher")

if __name__ == '__main__':
    unittest.main()