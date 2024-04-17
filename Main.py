import src.FitnessCalculator

if __name__ == '__main__':
    fit = src.FitnessCalculator.FitnessCalculator("Beamng")
    fit.calculateFitnessSim(test_cases=[[10, 10], [50, 50], [5, 150]])