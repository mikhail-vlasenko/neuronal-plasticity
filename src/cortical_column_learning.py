from brian2 import NeuronGroup, Synapses, PoissonGroup, SpikeMonitor, Network, ms, defaultclock, StateMonitor
from matplotlib import pyplot as plt
from tqdm import tqdm
import math

from Original_model.utils.utils import setup_loggers
from src.connectivity_graph import visualize_network_connectivity
from src.equations.layer23_eqs import *
from src.equations.stdp_eqs import expected_reward_merge
from src.input_from_csv import csv_input_neurons
from src.plotting import spike_raster, get_plots_iterator, PLOTTING_PARAMS, plot_heatmaps, plot_dopamine, \
    plot_output_potentials

# todo: remove
defaultclock.dt = 0.1 * ms  # Time resolution of the simulation


class Simulation:
    def __init__(
            self, net_dict, neuron_dict, log,
            sample_duration=100 * ms,
            epochs=2,
            num_exposures=2, multiply_input=1, wait_durations=0,
            data_path='../data/sample.csv',
            in_connection_avg=32, out_connection_avg=32,
            weight_coef=0.5, weight_std_coef=0.25,
            in_out_max_strength=0.35,
            post_prediction_inhib_value=0.2,
            epsilon_dopa=1e-2,
            hom_add_coef=20, hom_subtract_coef=2, gmax_coef=0.5, dA_coef=0.1,  # ampa params
    ):
        reset_ampa_counter()
        self.net_dict = net_dict
        self.neuron_dict = neuron_dict
        self.sample_duration = sample_duration
        self.epochs = epochs
        self.num_exposures = num_exposures
        self.multiply_input = multiply_input
        self.wait_durations = wait_durations
        self.data_path = data_path
        self.in_connection_avg = in_connection_avg
        self.out_connection_avg = out_connection_avg
        self.weight_coef = weight_coef
        self.weight_std_coef = weight_std_coef
        self.in_out_max_strength = in_out_max_strength
        self.post_prediction_inhib_value = post_prediction_inhib_value
        self.epsilon_dopa = epsilon_dopa
        self.ampa_params = {
            'hom_add_coef': hom_add_coef,
            'hom_subtract_coef': hom_subtract_coef,
            'gmax_coef': gmax_coef,
            'dA_coef': dA_coef
        }

        self.log = log
        self.net = None
        self.expected_reward = 0
        self.num_populations = 4
        self.synapses = []
        self.dopamine_modulated_synapse_idx = []  # holds indices of synapses that are trained with dopamine
        self.spike_monitors = []
        self.weight_monitors = []
        self.net_params = [self.synapses,
                           self.spike_monitors, self.weight_monitors]

        self.__create_neurons()
        self.__create_output_neurons()
        self.__connect_populations()
        # self.__connect_poisson_bg_input()
        self.__connect_training_input()
        self.__connect_dopamine_synapses()
        self.__connect_post_prediction_inhibition()
        log.info('Initialization complete')

    def __post_init_population(self, population, i):
        population.v_th = self.neuron_dict['V_th'][i]
        population.v_reset = self.neuron_dict['V_reset'][i]
        population.v = self.neuron_dict['V_L'][i]
        population.V_L = self.neuron_dict['V_L'][i]
        population.C_m = self.neuron_dict['C_m'][i]
        population.g_L = self.neuron_dict['g_L'][i]
        population.V_I = receptors_V_I[i]

    def __create_neurons(self):
        self.pops = []
        for i in range(self.num_populations):
            population = NeuronGroup(
                self.net_dict['num_neurons'][i],
                model=NEURON_MODEL,
                threshold='v > v_th',
                reset='v = v_reset',
                refractory=self.neuron_dict['tau_ref'][i],
                method='euler'
            )
            self.__post_init_population(population, i)

            self.pops.append(population)
            self.spike_monitors.append(SpikeMonitor(population))
        self.net_params.append(self.pops)

    def __create_output_neurons(self):
        self.output_neurons = NeuronGroup(
            2,
            **OUTPUT_NEURON_PARAMS
        )
        self.__post_init_population(self.output_neurons, 0)
        self.output_monitor = SpikeMonitor(self.output_neurons)
        self.output_state_monitor = StateMonitor(self.output_neurons, ['v', 's_gaba_prediction', 's_ampa_tot'], record=[0, 1])
        self.net_params.append(self.output_neurons)
        self.net_params.append(self.output_monitor)
        self.net_params.append(self.output_state_monitor)

    def __connect_populations(self):
        self.synapses = []
        names = ['Excitatory', 'PV', 'SST', 'VIP']
        models = [None, PV_MODEL, SST_MODEL, VIP_MODEL]

        for n, target_pop in enumerate(self.pops):
            for m, source_pop in enumerate(self.pops):
                connect_prob = self.net_dict['connect_probs'][n][m]
                if connect_prob == 0:
                    continue
                strength = self.net_dict['synaptic_strength'][n][m]
                weight = strength / (connect_prob * self.net_dict['num_neurons'][m])

                if m == 0:
                    # ampa synapses
                    synapse_params = get_ampa_params(weight * 2, **self.ampa_params)
                else:
                    # gaba synapses
                    synapse_params = {
                        'model': models[m],
                        'on_pre': gaba_on_pre,
                        'on_post': gaba_on_post,
                        'method': 'euler',
                        'delay': NET_DICT['delay']
                    }
                synapse = Synapses(
                    source_pop, target_pop,
                    name=f'{names[m]}_{names[n]}',
                    **synapse_params,
                )
                connect_kwargs = {'p': connect_prob}
                if m == n: connect_kwargs['condition'] = 'i != j'
                synapse.connect(**connect_kwargs)

                # self.log.info(f'Weight for {m} -> {n} connection: {weight}')
                synapse.w = f"{weight} + randn() * {self.weight_std_coef * weight}"
                if m == 0:
                    self.dopamine_modulated_synapse_idx.append(len(self.synapses))
                else:
                    # inhibitory synapses, define homeostasis variables
                    synapse.baseline_inhib_w = weight
                    synapse.amplitude = 2 * weight
                    synapse.learning_rate = inhib_lr_coef * weight

                self.synapses.append(synapse)
        if hasattr(self, 'output_neurons'):
            synapse = Synapses(
                self.pops[0], self.output_neurons, name='Excitatory_Output', **get_ampa_params(self.in_out_max_strength, **self.ampa_params)
            )
            synapse.connect(p=self.out_connection_avg / self.net_dict['num_neurons'][0])
            synapse.w = f"rand() * {self.in_out_max_strength} * {self.weight_coef}"
            if PLOTTING_PARAMS.plot_heatmaps:
                state_monitor = StateMonitor(synapse, ['w', 'c'], record=[_i for _i in range(32)])
                self.weight_monitors.append(state_monitor)
            self.dopamine_modulated_synapse_idx.append(len(self.synapses))
            self.synapses.append(synapse)

        self.net_params.append(self.synapses)
        self.dopamine_monitor = StateMonitor(self.synapses[self.dopamine_modulated_synapse_idx[0]], ['d'], record=[0])
        self.net_params.append(self.dopamine_monitor)

    def __connect_poisson_bg_input(self):
        self.duration = 1000 * ms
        self.poisson_groups = []
        self.poisson_synapses = []
        for pop_idx in np.arange(self.num_populations):
            poisson_group = PoissonGroup(self.net_dict['num_neurons'][pop_idx], rates=self.net_dict['bg_rate'][pop_idx])
            self.poisson_groups.append(poisson_group)
            poisson_s = Synapses(self.poisson_groups[pop_idx], self.pops[pop_idx], on_pre='s_ampa_ext += 1', method='euler')
            self.poisson_synapses.append(poisson_s)
            self.poisson_synapses[pop_idx].connect(j='i')  # Connects Poisson one-to-one
        self.net_params.append(self.poisson_groups)
        self.net_params.append(self.poisson_synapses)

    def __connect_training_input(self):
        self.input_neurons, self.targets, self.input_dim, self.duration = csv_input_neurons(
            self.data_path, duration=self.sample_duration, repeat_for=self.epochs,
            num_exposures=self.num_exposures, wait_durations=self.wait_durations,
            blasting=False
        )
        self.input_monitor = SpikeMonitor(self.input_neurons)
        # connect to excitatory neurons
        synapse = Synapses(
            self.input_neurons, self.pops[0], name='Input_Excitatory', **get_ampa_params(self.in_out_max_strength, **self.ampa_params)
        )
        synapse.connect(p=self.in_connection_avg / self.net_dict['num_neurons'][0], n=self.multiply_input)
        synapse.w = f"rand() * {self.in_out_max_strength} * {self.weight_coef}"
        self.dopamine_modulated_synapse_idx.append(len(self.synapses))
        self.synapses.append(synapse)
        self.net_params.append(self.input_neurons)
        self.net_params.append(self.input_monitor)

    def __connect_post_prediction_inhibition(self):
        self.post_prediction_inhibitors = []
        targets = self.pops + [self.output_neurons]
        for _i in range(len(targets)):
            if _i == len(targets) - 1:
                # inhibit output way more
                self.post_prediction_inhib_value *= 5
            self.post_prediction_inhibitors.append(Synapses(
                self.output_neurons, targets[_i], model='''''',
                on_pre=f'''s_gaba_prediction += {self.post_prediction_inhib_value}''',
                # delay=2*ms,
                method='exact'
            ))
            self.post_prediction_inhibitors[-1].connect()
        self.net_params.append(self.post_prediction_inhibitors)

    def __connect_dopamine_synapses(self):
        self.reward_synapses = []
        for _i in self.dopamine_modulated_synapse_idx:
            target = self.synapses[_i]
            # + reward because 0 spiked (reward is negative for samples with answer 1)
            self.reward_synapses.append(Synapses(self.output_neurons[0], target, model='''''',
                                        on_pre='''d_post += (reward_value_pre - expected_reward_pre)''',
                                        method='exact'))
            self.reward_synapses[-1].connect()

            # - reward because 1 spiked
            self.reward_synapses.append(Synapses(self.output_neurons[1], target, model='''''',
                                        on_pre='''d_post += (reward_value_pre - expected_reward_pre)''',
                                        method='exact'))
            self.reward_synapses[-1].connect()
        self.net_params.append(self.reward_synapses)

    def create_network(self):
        self.net = Network(*self.net_params)

    def count_out_spikes(self):
        return self.output_monitor.num_spikes

    def set_reward(self, sample_i):
        # assign negative reward to the second output neuron. its synapses subtract the reward
        _reward_value = self.epsilon_dopa if self.targets[sample_i] == 0 else -self.epsilon_dopa
        self.output_neurons.reward_value[0] = _reward_value
        self.output_neurons.reward_value[1] = -_reward_value
        self.output_neurons.expected_reward = self.expected_reward
        self.output_neurons.obtained_reward = 0

    def update_expected_reward(self):
        self.expected_reward = expected_reward_merge(self.output_neurons.obtained_reward, self.expected_reward)

    def run(self):
        self.create_network()
        self.expected_reward = 0
        kill_threshold = -0.8
        pbar = tqdm(range(math.floor(self.duration / self.sample_duration)))
        for sample_i in pbar:
            self.set_reward(sample_i)
            self.net.run(self.sample_duration)

            self.update_expected_reward()
            exp_reward = self.expected_reward / self.epsilon_dopa
            pbar.set_description(f'Expected reward: {exp_reward:.3f}')

            if exp_reward > 0.8:
                print(f'Well-trained at iteration {sample_i}')

            if sample_i > 16 and (exp_reward < kill_threshold or self.count_out_spikes() < sample_i / 2):
                print(f'Bad at iteration {sample_i}. Expected reward: {exp_reward}. Num spikes: {self.count_out_spikes()}')


def main(seed=0):
    # params = {'in_connection_avg': 63.61493174793468, 'out_connection_avg': 43.5554992226015, 'weight_coef': 0.2754978971096503, 'in_out_max_strength': 0.3326309275202886, 'post_prediction_inhib_value': 0.20316439497369881, 'epsilon_dopa': 0.03861273348008514, 'hom_add_coef': 14.59113587079569, 'hom_subtract_coef': 1.7771771154755764, 'gmax_coef': 0.535232155930282, 'dA_coef': 0.08359228568155307}
    # iter 113
    params = {'in_connection_avg': 36.75938701607436, 'out_connection_avg': 38.31586841874557, 'weight_coef': 0.3478002611515175, 'in_out_max_strength': 0.3579144843925931, 'post_prediction_inhib_value': 0.0830196600114798, 'epsilon_dopa': 0.008015934444846762, 'hom_add_coef': 11.252674808682224, 'hom_subtract_coef': 4.856393272889642, 'gmax_coef': 0.2605735865010971, 'dA_coef': 0.02362831541590541}
    params['epochs'] = 16
    params['data_path'] = '../data/sample.csv'
    np.random.seed(seed)
    log = setup_loggers('')

    simulation = Simulation(NET_DICT, NEURON_DICT, log, **params)
    simulation.run()

    PLOTTING_PARAMS.simulation_duration = simulation.duration
    PLOTTING_PARAMS.plot_from = max(0, simulation.duration / ms - 2000)
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
