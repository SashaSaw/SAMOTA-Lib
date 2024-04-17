from evaluation.cps_tool_competition.code_pipeline.tests_generation import RoadTestFactory
import importlib
import traceback
import time
import os
import sys
import errno
import logging as log


OUTPUT_RESULTS_TO = 'results'
DEFAULT = object()

def get_script_path():
    # Returns the absolute path of the directory containing this script
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def setup_logging(log_to, debug):
    def log_exception(extype, value, trace):
        log.exception('Uncaught exception:', exc_info=(extype, value, trace))

    # Disable annoyng messages from matplot lib.
    # See: https://stackoverflow.com/questions/56618739/matplotlib-throws-warning-message-because-of-findfont-python
    log.getLogger('matplotlib.font_manager').disabled = True

    term_handler = log.StreamHandler()
    log_handlers = [term_handler]
    start_msg = "Started test generation"

    if log_to is not None:
        file_handler = log.FileHandler(log_to, 'a', 'utf-8')
        log_handlers.append(file_handler)
        start_msg += " ".join(["writing to file: ", str(log_to)])

    log_level = log.DEBUG if debug else log.INFO

    log.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=log_level, handlers=log_handlers)

    sys.excepthook = log_exception

    log.info(start_msg)
def runSim(testcases):
    beamng_home = 'C:\\Program Files\\BeamNG.tech.v0.26.2.0'
    beamng_user = 'C:\\cps-tool-competition\\bng-usr'
    log_to = None  # Default to None, implies logging to console if not specified
    debug = False
    module_name = 'src.FitnessCalculator'
    class_name = 'OneTestGenerator'
    executor = 'beamng'
    time_budget = 100
    map_size = 200
    oob_tolerance = 0.95
    speed_limit = 60
    # Setup logging
    setup_logging(log_to, debug)

    log.info(f"Try to import {class_name} from {module_name}")
    module = importlib.import_module(module_name)
    the_class = getattr(module, class_name)

    road_visualizer = None
    # Setup folder structure by ensuring that the basic folder structure is there.
    default_output_folder = os.path.join(get_script_path(), OUTPUT_RESULTS_TO)
    try:
        os.makedirs(default_output_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    timestamp_id = int(time.time() * 100000000 // 1000000)
    result_folder = os.path.join(default_output_folder,
                                 "_".join([str(module_name), str(class_name), str(timestamp_id)]))

    try:
        os.makedirs(result_folder)
    except OSError:
        log.fatal("An error occurred during test generation")
        traceback.print_exc()
        sys.exit(2)

    log.info("Outputting results to " + result_folder)

    # Setup executor. All the executor must output the execution data into the result_folder
    if executor == "mock":
        from evaluation.cps_tool_competition.code_pipeline.executors import MockExecutor
        the_executor = MockExecutor(result_folder, map_size,
                                    time_budget=time_budget,
                                    road_visualizer=road_visualizer)
    elif executor == "beamng":
        from evaluation.cps_tool_competition.code_pipeline.beamng_executor import BeamngExecutor
        the_executor = BeamngExecutor(result_folder, map_size,
                                      time_budget=time_budget,
                                      oob_tolerance=oob_tolerance, max_speed_in_kmh=speed_limit,
                                      beamng_home=beamng_home, beamng_user=beamng_user,
                                      road_visualizer=road_visualizer)

    try:
        # Instantiate the test generator
        test_generator = the_class(executor=the_executor, map_size=map_size, test_case=testcases)
        # Start the generation
        output = test_generator.start()
    except Exception:
        log.fatal("An error occurred during test generation")
        traceback.print_exc()
        sys.exit(2)
    finally:
        # Ensure the executor is stopped no matter what.
        the_executor.close()
        return output
class OneTestGenerator():
    """
        Generates a single test to show how to control the shape of the road by controlling the positio of the
        road points. We assume a map of 200x200
    """

    def __init__(self, executor=None, map_size=None, test_case=None):
        self.executor = executor
        self.map_size = map_size
        self.test_case = test_case

    def start(self):
        print ("Starting test generation")
        print ("self.test_case")
        road_points = self.test_case

        log.info("Generated test using: %s", road_points)

        # Creating the RoadTest from the points
        the_test = RoadTestFactory.create_road_test(road_points)
        # Send the test for execution
        test_outcome, description, execution_data = self.executor.execute_test(the_test)

        output = 1
        if test_outcome != "INVALID":
        # Plot the OOB_Percentage: How much the car is outside the road?
            oob_percentage = [state.oob_percentage for state in execution_data]
            log.info("Collected %d states information. Max is %.3f", len(oob_percentage), max(oob_percentage))
            output = max(oob_percentage)

        # Print test outcome
        log.info("test_outcome %s", test_outcome)
        log.info("description %s", description)

        #import time
        #time.sleep(10)
        return output

class FitnessCalculator:

    def __init__(self, simulator_name):
        self.simulator_name = simulator_name

    def calculateFitnessSim(self, test_cases):
        """Takes the input test cases and computes the fitness scores by running the simulator.
        Then updates the fitness scores of the test cases and returns the updated test cases
        :param test_cases:
        :return: set of TestCases with updated fitness scores
        """
        #for test_case in test_cases
        print(runSim(test_cases))
        #use one test generator and fitness score = max(oob_percentage)


