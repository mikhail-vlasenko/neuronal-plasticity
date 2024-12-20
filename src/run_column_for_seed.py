import numpy as np
import math

from matplotlib import pyplot as plt

from Original_model.utils.utils import setup_loggers
from src.cortical_column_learning import Simulation
from src.equations.layer23_eqs import *
from src.plotting import PLOTTING_PARAMS, get_plots_iterator, plot_dopamine, plot_output_potentials, plot_heatmaps, \
    spike_raster


def run_for_seed(
        seed, params, log,
        initial_iters=16, success_threshold=0.925,
        kill_threshold=-0.8, trial=None, return_simulation=False
):
    def _print(*args):
        if trial is not None:
            print(f"Trial {trial.number}, seed {seed}: ", *args)
        else:
            print(f"Seed {seed}: ", *args)

    np.random.seed(seed)
    simulation = Simulation(
        NET_DICT, NEURON_DICT, log, **params
    )
    simulation.create_network()
    total_iters = math.floor(simulation.duration / simulation.sample_duration)
    for sample_i in range(initial_iters):
        simulation.set_reward(sample_i)
        simulation.net.run(simulation.sample_duration)
        simulation.update_expected_reward()
        simulation.end_time = (sample_i + 1) * simulation.sample_duration

    num_spikes = simulation.count_out_spikes()
    if num_spikes > initial_iters * 1.25 or num_spikes < initial_iters / 2:
        _print(f'Killed at initial num spikes: {num_spikes}')
        if return_simulation:
            return simulation
        return 3  # optuna needs to minimize the objective

    exp_reward = simulation.expected_reward / simulation.epsilon_dopa
    if exp_reward > success_threshold:
        _print(f'Well-trained at initial stage. Expected reward: {exp_reward}')
        if return_simulation:
            return simulation
        return 0.5

    for sample_i in range(initial_iters, total_iters):
        simulation.set_reward(sample_i)
        simulation.net.run(simulation.sample_duration)
        simulation.update_expected_reward()
        simulation.end_time = (sample_i + 1) * simulation.sample_duration

        exp_reward = simulation.expected_reward / simulation.epsilon_dopa
        if exp_reward > success_threshold:
            _print(f'Well-trained at iteration {sample_i}')
            if return_simulation:
                return simulation
            return sample_i / total_iters

        if exp_reward < kill_threshold or simulation.count_out_spikes() < sample_i / 2:
            _print(f'Killed at iteration {sample_i}. Expected reward: {exp_reward}. Num spikes: {simulation.count_out_spikes()}')
            if return_simulation:
                return simulation
            return 3

    _print(f'Final expected reward: {exp_reward}')
    if return_simulation:
        return simulation
    return 2 - exp_reward  # larger than any well-trained value


def main(seed=0):
    params = {'in_connection_avg': 51.338810560257805, 'out_connection_avg': 29.865152512012735, 'weight_coef': 0.1940955736697889, 'in_out_max_strength': 0.40852078693779903, 'post_prediction_inhib_value': 0.26911541583357784, 'epsilon_dopa': 0.0646988016329517, 'hom_add_coef': 14.560935611024547, 'hom_subtract_coef': 4.293059584704207, 'gmax_coef': 0.27555080107464347, 'dA_coef': 0.23152478813141367}
    params['epochs'] = 64
    params['data_path'] = '../data/sample.csv'
    log = setup_loggers('')

    # # call the constructor once to mitigate the effect on the random state effect from that one synapse.connect() call
    # np.random.seed(0)
    # temp = Simulation(NET_DICT, NEURON_DICT, log)
    # temp.create_network()
    # temp.net.run(1 * ms)  # to avoid brain2 warnings
    # del temp

    # the previous method for mitigating the random state effect was somehow not enough, so i have to do this.
    # This is only for exact reproducibility with optuna optimization, where many simulations happen in the same process
    temp_params = params.copy()
    temp_params['epochs'] = 1
    _ = run_for_seed(
        0, temp_params, log,
        initial_iters=1, return_simulation=True
    )

    simulation: Simulation = run_for_seed(
        seed, params, log,
        initial_iters=8,
        success_threshold=0.95,
        return_simulation=True
    )

    PLOTTING_PARAMS.simulation_duration = simulation.end_time
    PLOTTING_PARAMS.plot_from = max(0, PLOTTING_PARAMS.simulation_duration / ms - 800)
    PLOTTING_PARAMS.update()

    fig, gs = get_plots_iterator()

    plot_dopamine(fig.add_subplot(gs.__next__()), simulation.dopamine_monitor)
    if not PLOTTING_PARAMS.minimal_reporting:
        plot_output_potentials(fig.add_subplot(gs.__next__()),
                               simulation.output_state_monitor, simulation.neuron_dict['V_th'][0])

    if PLOTTING_PARAMS.plot_heatmaps and not PLOTTING_PARAMS.minimal_reporting:
        ax_input = fig.add_subplot(gs.__next__())
        ax_output = fig.add_subplot(gs.__next__())
        plot_heatmaps(ax_input, ax_output, None, simulation.weight_monitors[0])

    spike_raster(
        fig.add_subplot(gs.__next__()),
        simulation.input_monitor if hasattr(simulation, 'input_monitor') else None,
        simulation.spike_monitors[0], simulation.spike_monitors[1:],
        simulation.output_monitor if hasattr(simulation, 'output_monitor') else None,
    )

    plt.savefig('cortical_column_learning.png')
    plt.show()


if __name__ == '__main__':
    main(1)
