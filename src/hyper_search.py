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
    weight_std_coef = 0.25

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

    def run_for_seed(seed):
        def _print(*args):
            print(f"Trial {trial.number}, seed {seed}: ", *args)

        np.random.seed(seed)
        simulation = Simulation(
            NET_DICT, NEURON_DICT, log,
            epochs=epochs, data_path=data_path,
            in_connection_avg=in_connection_avg, out_connection_avg=out_connection_avg,
            weight_coef=weight_coef, weight_std_coef=weight_std_coef, in_out_max_strength=in_out_max_strength,
            post_prediction_inhib_value=post_prediction_inhib_value, epsilon_dopa=epsilon_dopa, hom_add_coef=hom_add_coef,
            hom_subtract_coef=hom_subtract_coef, gmax_coef=gmax_coef, dA_coef=dA_coef
        )
        simulation.create_network()
        total_iters = math.floor(simulation.duration / simulation.sample_duration)
        for sample_i in range(initial_iters):
            simulation.set_reward(sample_i)
            simulation.net.run(simulation.sample_duration)
            simulation.update_expected_reward()

        num_spikes = simulation.count_out_spikes()
        if num_spikes > initial_iters * 1.25 or num_spikes < initial_iters / 2:
            _print(f'Killed at initial num spikes: {num_spikes}')
            return 3  # optuna needs to minimize the objective

        exp_reward = simulation.expected_reward / simulation.epsilon_dopa
        if exp_reward > success_threshold:
            _print(f'Well-trained at initial stage. Expected reward: {exp_reward}')
            return 0.5

        for sample_i in range(initial_iters, total_iters):
            simulation.set_reward(sample_i)
            simulation.net.run(simulation.sample_duration)
            simulation.update_expected_reward()

            exp_reward = simulation.expected_reward / simulation.epsilon_dopa
            if exp_reward > success_threshold:
                _print(f'Well-trained at iteration {sample_i}')
                return sample_i / total_iters

            if exp_reward < kill_threshold or simulation.count_out_spikes() < sample_i / 2:
                _print(f'Killed at iteration {sample_i}. Expected reward: {exp_reward}. Num spikes: {simulation.count_out_spikes()}')
                return 3

        _print(f'Final expected reward: {exp_reward}')
        return 2 - exp_reward  # larger than any well-trained value

    results = [run_for_seed(seed) for seed in seeds]
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
        # Create the study first
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

        # Print results
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
