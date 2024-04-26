
class SAMOTA:

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
            uncovered_obj[i] = False
            for test_case in all_test_cases:
                if test_case is not None:
                    fitness = test_case.get_fitness_score_sim()[i]
                    if fitness > error_thresholds[i] and fitness > highest_fitness:
                        uncovered_obj[i] = True
                        highest_fitness = fitness
                        output_archive[i] = test_case
        return output_archive, uncovered_obj

    def init_uncovered_obj(self, num_of_obj):
        return [False] * num_of_obj

    def samota(self, num_of_runs, pop_size, error_thresholds, fit_calc, gs, gmax, ls, lmax, percent_local, min_per_cluster, db):
        archive = []
        uncovered_obj = self.init_uncovered_obj(len(error_thresholds))
        test_cases = gs.initial_population(pop_size)
        test_cases = fit_calc.calculate_fitness_sim(test_cases)
        archive, uncovered_objs = self.update_archive(archive, test_cases, error_thresholds, uncovered_obj)
        db.update_database(test_cases)
        while(num_of_runs > 0):
            global_test_cases = gs.global_search(db, uncovered_objs, pop_size, gmax, error_thresholds)
            global_test_cases = fit_calc.calculate_fitness_sim(global_test_cases)
            archive, uncovered_objs = self.update_archive(archive, global_test_cases, error_thresholds, uncovered_obj)
            db.update_database(global_test_cases)
            local_test_cases = ls.local_search(db, uncovered_objs, lmax, percent_local, min_per_cluster)
            local_test_cases = fit_calc.calculate_fitness_sim(local_test_cases)
            archive, uncovered_objs = self.update_archive(archive, local_test_cases, error_thresholds, uncovered_obj)
            db.update_database(global_test_cases)
            if self.check_if_obj_covered(uncovered_obj):
                print("objective covered - stopping algorithm early...")
                num_of_runs = 0
            num_of_runs = num_of_runs - 1
        return archive, db

    def check_if_obj_covered(self, uncovered_obj):
        output = True
        # for all objs if one is False then not all objectives are covered
        for obj in uncovered_obj:
            if not obj:
                output = False
        return output
