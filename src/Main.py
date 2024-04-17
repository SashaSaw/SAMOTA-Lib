import click
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

@click.command()
@click.option('--beamng-home', required=False, default='C:\\Program Files\\BeamNG.tech.v0.26.2.0',
              type=click.Path(exists=True),
              show_default='None',
              help="Customize BeamNG executor by specifying the home of the simulator.")
@click.option('--beamng-user', required=False, default='C:\\cps-tool-competition\\bng-usr',
              type=click.Path(exists=True),
              show_default='Currently Active User (~/BeamNG.tech/)',
              help="Customize BeamNG executor by specifying the location of the folder "
                   "where levels, props, and other BeamNG-related data will be copied."
                   "** Use this to avoid spaces in URL/PATHS! **")
@click.option('--module-path', required=False, type=click.Path(exists=True),
              help="Path of the module where your test generator is located.")
# Logging options
@click.option('--log-to', required=False, type=click.Path(exists=False),
              help="Location of the log file. If not specified logs appear on the console")
@click.option('--debug', required=False, is_flag=True, default=False,
              show_default='Disabled',
              help="Activate debugging (results in more logging)")
@click.pass_context
def generate(ctx, beamng_home, beamng_user, module_path, log_to, debug):
    module_name = 'FitnessCalculator'
    class_name = 'OneTestGenerator'
    executor = 'beamng'
    time_budget = 100
    map_size = 200
    oob_tolerance = 0.95
    speed_limit = 60
    # Setup logging
    setup_logging(log_to, debug)

    # Setup test generator by dynamically loading it
    if module_path:
        log.info(f"Loading module from {module_path}")
        sys.path.append(module_path)
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
        test_generator = the_class(executor=the_executor, map_size=map_size)
        # Start the generation
        test_generator.start()
    except Exception:
        log.fatal("An error occurred during test generation")
        traceback.print_exc()
        sys.exit(2)
    finally:
        # Ensure the executor is stopped no matter what.
        the_executor.close()

if __name__ == '__main__':
    generate()