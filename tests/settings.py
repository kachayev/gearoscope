from settings import *

# List of gearman nodes connection host:port pairs,
# which will be used for stub environment running
STUB_GEARMAN_NODES = ['localhost:4730']

# High value of probability means that
# client will generate more tasks per each delay block
STUB_TASKS_PROBABILITY = {
    'reverse': 0.5,
    'sum': 0.7,
    'multiple': 0.7
}

# List of argumensts which will be given
# to sequence randomizer as params for each task processing
STUB_TASKS_ARGS = {
    'reverse': [30],
    'sum': [4],
    'multiple': [3]
}

# Time delay in seconds between to generator's tic
# Leave current value as 1.0 and tasks will be generating once per each second
STUB_TASKS_FREQUENCY = 1.0

# Time delay in seconds between gearman worker pool operations
# (for more information, look for SleepingGearmanWorker object implementation)
STUB_WORKERS_FREQUENCY = 1.0

# Setting client ID can be useful for analyzing information
# from gearman admin client, which show list of
# currently connected workers by its CLIENT ID
STUB_WORKERS_ID_FORMAT = 'Stub.worker.daemon.%(task)s'

