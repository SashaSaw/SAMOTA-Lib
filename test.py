import unittest
from src.fitness_calculator import BeamngFitnessCalc
from src.test_case import TestCase
from src.surrogate_model import PolynomialRegression
import random


class TestFitnessCalc(unittest.TestCase):

    def setUp(self):
        self.fitness_calc = BeamngFitnessCalc("Beamng")
        self.testcase1 = TestCase([[20, 20], [20, 50], [23, 100]], [], [], [])
        self.testcase2 = TestCase([[20, 20], [20, 80], [100, 100]], [], [], [])
        self.testcase3 = TestCase([[20, 20], [20, 80], [20, 100]], [], [], [])
        self.testcases = [self.testcase1, self.testcase2, self.testcase3]

    def test_straightvscurve(self):
        testcases_updated = self.fitness_calc.calculate_fitness_sim(self.testcases)
        fitness1 = testcases_updated[2].get_fitness_score_sim()[0]
        fitness2 = testcases_updated[1].get_fitness_score_sim()[0]
        print("straight: "+ str(fitness1))
        print("curve: "+ str(fitness2))
        self.assertGreater(fitness1, fitness2, "fitness score for a straight test case should be higher than that of a curved test case")

    def test_bigvssmallcurve(self):
        testcases_updated = self.fitness_calc.calculate_fitness_sim(self.testcases)
        fitness1 = testcases_updated[1].get_fitness_score_sim()[0]
        fitness2 = testcases_updated[0].get_fitness_score_sim()[0]
        print("big curve: "+ str(fitness1))
        print("small curve: "+ str(fitness2))
        self.assertGreater(fitness1, fitness2, "fitness score for smaller curve test case should be higher")


class TestSurrogateModel(unittest.TestCase):

    def setUp(self):
        self.test_cases = []
        for i in range(0,20):
            testcase = TestCase([[random.randint(1,199), random.randint(1,199)],
                                 [random.randint(1,199), random.randint(1,199)],
                                 [random.randint(1,199), random.randint(1,199)]], [], [], [])
            self.test_cases.append(testcase)
        self.fit = BeamngFitnessCalc("beamng")
        self.test_cases = self.fit.calculate_fitness_sim(self.test_cases)

    def test_surrogate_mse(self):
        self.surrogate = PolynomialRegression(3)
        self.surrogate.train(self.test_cases)
        mse = self.surrogate.test()
        print (mse)
        self.assertLess(mse, 0.5, "mse should be small")



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSurrogateModel)
    unittest.TextTestRunner().run(suite)