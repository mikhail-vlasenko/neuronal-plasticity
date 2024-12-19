import logging
import math
import os
from multiprocessing import Process

import optuna

import numpy as np

from src.cortical_column_learning import Simulation
from src.equations.layer23_eqs import NET_DICT, NEURON_DICT
from src.equations.layer23_eqs import *
from src.equations.stdp_eqs import expected_reward_merge
from src.run_column_for_seed import run_for_seed


def objective(trial: optuna.Trial):
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    null_handler = logging.NullHandler()
    log.addHandler(null_handler)
    log.propagate = False

    success_threshold = 0.925
    kill_threshold = -0.8
    initial_iters = 16
    epochs = 32
    seeds = [0, 1]
    data_path = '../data/sample.csv'

    # Network connectivity parameters
    in_connection_avg = trial.suggest_float("in_connection_avg", 16, 64)
    out_connection_avg = trial.suggest_float("out_connection_avg", 16, 64)

    # Weight coefficients (since these are between 0-1)
    weight_coef = trial.suggest_float("weight_coef", 0.1, 0.9)

    # Connection strength (since original is 0.35, create range around it)
    in_out_max_strength = trial.suggest_float("in_out_max_strength", 0.1, 0.6)

    # Inhibition value (create range around 0.2)
    post_prediction_inhib_value = trial.suggest_float("post_prediction_inhib_value", 0.05, 0.4)

    # Epsilon value (log scale since it's small)
    epsilon_dopa = trial.suggest_float("epsilon_dopa", 1e-4, 1e-1, log=True)

    # Homeostasis coefficients (create ranges around original values)
    hom_add_coef = trial.suggest_float("hom_add_coef", 10, 30)
    hom_subtract_coef = trial.suggest_float("hom_subtract_coef", 1, 5)

    # Other coefficients
    gmax_coef = trial.suggest_float("gmax_coef", 0.1, 0.9)
    dA_coef = trial.suggest_float("dA_coef", 0.01, 0.3)

    # params = {'in_connection_avg': 29.377815522884113, 'out_connection_avg': 35.53795706986652, 'weight_coef': 0.37619051980149176, 'in_out_max_strength': 0.5143908103162069, 'post_prediction_inhib_value': 0.2674335597095533, 'epsilon_dopa': 0.001563584110860179, 'hom_add_coef': 18.771656999020415, 'hom_subtract_coef': 3.1377985224829463, 'gmax_coef': 0.17484030554504476, 'dA_coef': 0.12410622172759984}
    # params['epochs'] = epochs
    # params['data_path'] = data_path
    params = trial.params.copy()
    params['epochs'] = epochs
    params['data_path'] = data_path

    results = [run_for_seed(
        seed, params, log,
        success_threshold=success_threshold, kill_threshold=kill_threshold, initial_iters=initial_iters,
        trial=trial
    ) for seed in seeds]
    return np.mean(results)


STUDY_NAME = "nddl"
STORAGE = "sqlite:///optuna_sqlite.db"

def run_optimization(process_id):
    print(f"Process {process_id} started")
    study = optuna.load_study(
        study_name=STUDY_NAME,
        storage=STORAGE
    )
    study.optimize(objective, n_trials=os.getenv("OPTUNA_N_TRIALS", 10))  # n_trials is for each process

if __name__ == '__main__':
    distributed = os.getenv("OPTUNA_DISTRIBUTED", False)
    if distributed:
        print("Distributed mode")
        study = optuna.create_study(
            study_name=STUDY_NAME,
            storage=STORAGE,
        )

        n_processes = os.getenv("OPTUNA_PROCESSES", 16)

        processes = []
        for i in range(n_processes):
            p = Process(target=run_optimization, args=(i,))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        final_study = optuna.load_study(
            study_name=STUDY_NAME,
            storage=STORAGE
        )
        print("Best value:", final_study.best_value)
        print("Best params:", final_study.best_params)
    else:
        study = optuna.create_study()
        study.optimize(objective, n_trials=10)
        print("Results:")
        print(study.best_value)
        print(study.best_params)
