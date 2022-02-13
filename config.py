import logging
from dataclasses import fields

from simulation import SimulationResult

N_USERS = 100
N_SIMULATIONS = 50
TRAINING_INTERVAL_DAYS = 7
DEFAULT_TABLE = "training_result"
# each entry in the dataset consists of a SimulationResult
TABLE_COLUMNS = [field.name for field in fields(SimulationResult)]


LOGGING_FORMAT = "\n%(name)s: [%(levelname)s] %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
logger = logging.getLogger("Summer Hunter Logger")
