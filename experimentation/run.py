import sys
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from experiments.experiment_graph import experiment_graph
from experiments.experiment_filter import experiment_filter
from experiments.experiment_maximize import experiment_maximize
from experiments.experiment_minimize import experiment_minimize

''' Recomiendo ejecutar solo uno a la vez '''
experiment_graph()
# experiment_filter()
# experiment_maximize()
# experiment_minimize()