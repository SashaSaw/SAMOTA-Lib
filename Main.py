import click
import importlib
import traceback
import time
import os
import sys
import errno
import logging as log

from random import randint

from evaluation.cps_tool_competition.code_pipeline.tests_generation import RoadTestFactory



OUTPUT_RESULTS_TO = 'results'
DEFAULT = object()

def get_script_path():
    # Returns the absolute path of the directory containing this script
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def validate_map_size(ctx, param, value):
    """
    The size of the map is defined by its edge. The edge can be any (integer) value between 100 and 1000
    """
    if int(value) < 100 or int(value) > 1000:
        raise click.BadParameter(
            'The provided value for ' + str(param) + ' is invalid. Choose an integer between 100 and 1000')
    else:
        return int(value)


def validate_optional_time_budget(ctx, param, value):
    """
    A valid time budget is a positive integer of 'seconds' or it should not be set, i.e., set to str(DEFAULT).
    Note we need str(DEFAULT) because click works only with strings
    """
    if value != str(DEFAULT) and int(value) < 1:
        raise click.BadParameter('The provided value for ' + str(param) + ' is invalid. Choose any positive integer')

    # Transform the default value to None after checking the condition
    return int(value) if value != str(DEFAULT) else None


def validate_speed_limit(ctx, param, value):
    """
    The speed limit must be a positive integer greater than 10 km/h (lower values might trigger the
    car-not-moving oracle
    """
    if int(value) < 10:
        raise click.BadParameter(
            'The provided value for ' + str(param) + ' is invalid. Choose a value greater than 10')
    else:
        return int(value)


def validate_oob_tolerance(ctx, param, value):
    """
    OOB tolerance must be a value between 0.0 and 1.0
    """
    if value < 0.0 or value > 1.0:
        raise click.BadParameter(
            'The provided value for ' + str(param) + ' is invalid. Choose a value between 0.0 and 1.0')
    else:
        return value

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
@click.option('--executor', type=click.Choice(['mock', 'beamng'], case_sensitive=False), default="mock",
              show_default='Mock Executor (meant for debugging)',
              help="The name of the executor to use. Currently we have 'mock', 'beamng' or 'dave2'.")
@click.option('--dave2-model', required=False, type=click.Path(exists=True),
              default='C:\\cps-tool-competition\\dave2\\beamng-dave2.h5',
              help="Path of the pre-trained Dave2 driving AI model (in .h5 format). Mandatory if the executor is dave2")
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
# Budgeting options
@click.option('--time-budget', required=False, default=DEFAULT, callback=validate_optional_time_budget,
              help="Overall budget for the generation and execution. Expressed in 'real-time'"
                   "seconds.")
@click.option('--map-size', type=int, default=200, callback=validate_map_size,
              show_default='200m, which leads to a 200x200m^2 squared map',
              help="The lenght of the size of the squared map where the road must fit."
                   "Expressed in meters.")
@click.option('--oob-tolerance', type=float, default=0.3, callback=validate_oob_tolerance,
              show_default='0.95',
              help="The tolerance value that defines how much of the vehicle should be outside the lane to "
                   "trigger a failed test. Must be a value between 0.0 (all oob) and 1.0 (no oob)")
@click.option('--speed-limit', type=int, default=25, callback=validate_speed_limit,
              show_default='70 Km/h',
              help="The max speed of the ego-vehicle"
                   "Expressed in Kilometers per hours")
@click.option('--module-name', required=True, type=str,
              help="Name of the module where your test generator is located.")
@click.option('--module-path', required=False, type=click.Path(exists=True),
              help="Path of the module where your test generator is located.")
@click.option('--class-name', required=True, type=str,
              help="Name of the class implementing your test generator.")
# Visual Debugging
@click.option('--visualize-tests', required=False, is_flag=True, default=False,
              show_default='Disabled',
              help="Visualize the last generated test, i.e., the test sent for the execution. "
                   "Invalid tests are also visualized.")
# Logging options
@click.option('--log-to', required=False, type=click.Path(exists=False),
              help="Location of the log file. If not specified logs appear on the console")
@click.option('--debug', required=False, is_flag=True, default=False,
              show_default='Disabled',
              help="Activate debugging (results in more logging)")
@click.pass_context
def generate(ctx, executor, dave2_model, beamng_home, beamng_user,
             time_budget,
             map_size, oob_tolerance, speed_limit,
             module_name, module_path, class_name,
             visualize_tests, log_to, debug):
    ctx.ensure_object(dict)

    # TODO Refactor by adding a create summary command and forwarding the output of this run to that command

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
    # Setup visualization TODO can implement the visualiser code from cps-tool-competition for debugging
    #if visualize_tests:
    #    road_visualizer = RoadTestVisualizer(map_size=map_size)

    # Setup folder structure by ensuring that the basic folder structure is there.
    default_output_folder = os.path.join(get_script_path(), OUTPUT_RESULTS_TO)
    try:
        os.makedirs(default_output_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Create the unique folder that will host the results of this execution using the test generator data and
    # a timestamp as id
    # TODO Allow to specify a location for this folder and the run id
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

    # Register the shutdown hook for post processing results
    # register_exit_fun(create_post_processing_hook(ctx, result_folder, the_executor))

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
        # TODO Consider using a ContextManager: With executor ... do
        the_executor.close()

    # We still need this here to post process the results if the execution takes the regular flow
    # post_process(ctx, result_folder, the_executor)


if __name__ == '__main__':
    generate()