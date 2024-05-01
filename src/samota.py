import time


def check_if_obj_covered(uncovered_obj):
    output = True
    # for all objs if one is False then not all objectives are covered
    for obj in uncovered_obj:
        if not obj:
            output = False
    return output


def init_uncovered_obj(num_of_obj):
    return [False] * num_of_obj


def check_if_time_up(start_time, time_limit):
    if time.time() - start_time > time_limit:
        print("Time is up - concluding samota")
        return True
    else:
        return False


class SAMOTA:

    def __init__(self, fit_calc, gs, ls, db):
        self.fit_calc = fit_calc
        self.gs = gs
        self.ls = ls
        self.db = db


    def update_archive(self, archive, test_cases, error_thresholds, uncovered_obj):
        """given a set of test cases that satisfy some objectives(archive), a set of test cases generated randomly that
        have been run on the simulator, set of error thresholds and set of objectives, this function updates the archive
        to include test cases from the input archive and the input set of test cases and calculates uncovered objectives
        by excluding objectives that are still not covered (achieved) by the input test cases with respect to the given
        error thresholds.
        Note: update archive aims to achieve the min num of test cases to cover maximum number of objectives
        :param archive:
        :param test_cases:
        :param error_thresholds:
        :param uncovered_obj:
        :return: updated set of uncovered objectives and updated archive
        """
        output_archive = [None] * len(uncovered_obj)
        all_test_cases = archive + test_cases
        for i in range(len(uncovered_obj)):
            highest_fitness = 0
            for test_case in all_test_cases:
                if test_case is not None:
                    fitness = test_case.get_fitness_score_sim()[i]
                    if fitness > error_thresholds[i] and fitness > highest_fitness:
                        uncovered_obj[i] = True
                        highest_fitness = fitness
                        output_archive[i] = test_case
        return output_archive, uncovered_obj

    def samota(self, num_of_runs, pop_size, error_thresholds, time_limit):
        start_time = time.time()
        archive = []
        uncovered_obj = init_uncovered_obj(len(error_thresholds))
        test_cases = self.gs.initial_population(pop_size)
        test_cases = self.fit_calc.calculate_fitness_sim(test_cases)
        archive, uncovered_objs = self.update_archive(archive, test_cases, error_thresholds, uncovered_obj)
        self.db.update_database(test_cases)
        if check_if_time_up(start_time, time_limit):
            return archive, self.db
        while(num_of_runs > 0):
            global_test_cases = self.gs.global_search(self.db, uncovered_objs, pop_size, error_thresholds)
            global_test_cases = self.fit_calc.calculate_fitness_sim(global_test_cases)
            archive, uncovered_objs = self.update_archive(archive, global_test_cases, error_thresholds, uncovered_obj)
            self.db.update_database(global_test_cases)
            if check_if_time_up(start_time, time_limit):
                break
            local_test_cases = self.ls.local_search(self.db, uncovered_objs)
            local_test_cases = self.fit_calc.calculate_fitness_sim(local_test_cases)
            archive, uncovered_objs = self.update_archive(archive, local_test_cases, error_thresholds, uncovered_obj)
            self.db.update_database(global_test_cases)
            if check_if_obj_covered(uncovered_obj) or check_if_time_up(start_time, time_limit):
                break
            num_of_runs = num_of_runs - 1
        return archive, self.db
