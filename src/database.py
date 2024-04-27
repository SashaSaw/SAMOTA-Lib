from src.test_case import TestCase

class DatabaseManager:

    def __init__(self, initial_data=None):
        self.database = initial_data if initial_data is not None else []

    def set_default_database(self):
        test_case1 = TestCase([(0, 3), (100, 100), (150, 180)])
        test_case2 = TestCase([(0, 3), (100, 100), (150, 180)])
        test_case3 = TestCase([(0, 3), (100, 100), (150, 180)])
        test_case4 = TestCase([(0, 3), (100, 100), (150, 180)])
        testcases = []
        testcases.append(test_case1)
        testcases.append(test_case2)
        testcases.append(test_case3)
        testcases.append(test_case4)
        self.update_database(testcases)

    def get_database(self):
        """returns the database
        :return: database
        """
        return self.database.copy()

    def update_database(self, test_cases):
        """updates the database to include the given test cases
        :param test_cases:
        :return: database
        """
        for testcase in test_cases:
            self.database.append(testcase)

    def load_database(self, filename):
        """reads a text file that stores a representation of the database and sets the database in the Database object
        to that stored database
        :return: nothing
        """
        #reset database to an empty list
        self.database = []
        with open(filename+".txt", "r") as file:
            # Split the file into a list of lines
            lines = file.readlines()
            # Converts each line of file into a Test Case and then appends it to the database
            for line in lines:
                attributes = line.split("/")
                print (attributes)
                rep = attributes[0]
                representation = self.read_rep(rep)

                fitness_sim_string = attributes[1]
                fitness_sim = self.read_values(fitness_sim_string)

                fitness_predicted_string = attributes[2]
                fitness_predicted = self.read_values(fitness_predicted_string)

                uncertainty_string = attributes[3].replace('\n', '')
                uncertainty = self.read_values(uncertainty_string)

                testcase = TestCase(representation, fitness_sim, fitness_predicted, uncertainty)
                self.database.append(testcase)


    def read_rep(self, rep):
        rep_without_brackets = rep[1:-2]
        substrings = rep_without_brackets.split("], [")
        representation = []
        for substring in substrings:
            substring = substring.replace('[', '')
            substring = substring.replace(']', '')
            x, y = map(int, substring.split(","))
            representation.append([int(x), int(y)])
        return representation

    def read_values(self, string):
        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.replace(' ', '')
        substrings = string.split(",")
        value = []
        for substring in substrings:
            if len(substring) > 0:
                value.append(float(substring))
        return value

    def export_database(self, filename):
        """formats the database and saves a textfile with the formatted database
        :return: nothing
        """
        with open(filename+".txt", "w") as file:
            # Write content to the file
            for testcase in self.database:
                representation = testcase.get_representation()
                fitness_score_sim = testcase.get_fitness_score_sim()
                fitness_score_predicted = testcase.get_fitness_score_predicted()
                uncertainty = testcase.get_uncertainty()
                string = str(representation) + "/" +\
                         str(fitness_score_sim) + "/" +\
                         str(fitness_score_predicted) + "/" + \
                         str(uncertainty)
                file.write(string+"\n")
