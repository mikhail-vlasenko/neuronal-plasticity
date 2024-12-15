from brian2 import NeuronGroup, Synapses, PoissonGroup, SpikeMonitor, Network, ms, defaultclock, StateMonitor
from matplotlib import pyplot as plt

from Original_model.utils.utils import setup_loggers
from src.equations.layer23_eqs import *
from src.input_from_csv import csv_input_neurons
from src.plotting import spike_raster, get_plots_iterator, PLOTTING_PARAMS, plot_heatmaps

# todo: remove
defaultclock.dt = 0.1 * ms  # Time resolution of the simulation


class Simulation:
    def __init__(self, net_dict, neuron_dict, log):
        self.net_dict = net_dict
        self.neuron_dict = neuron_dict
        self.sample_duration = 100 * ms
        self.epochs = 8
        self.num_exposures = 10
        self.wait_durations = 2
        self.data_path = '../data/mini_sample.csv'
        self.in_connection_avg = 32

        self.log = log
        self.net = None
        self.num_populations = 4
        self.spike_monitors = []
        self.weight_monitors = []
        self.dopamine_monitors = []
        self.net_params = [self.spike_monitors, self.weight_monitors, self.dopamine_monitors]

        self.__create_neurons()
        self.__connect_populations()
        # self.__connect_poisson_bg_input()
        self.__connect_training_input()
        log.info('Initialization complete')

    def __create_neurons(self):
        self.pops = []
        for i in range(self.num_populations):
            population = NeuronGroup(
                self.net_dict['num_neurons'][i],
                model=NEURON_MODEL,
                threshold='v > v_th',
                reset='v = v_rest',
                refractory=self.neuron_dict['tau_ref'][i],
                method='euler'
            )
            population.v_th = self.neuron_dict['V_th'][i]
            population.v_rest = self.neuron_dict['V_reset'][i]
            population.v = self.neuron_dict['V_0'][i]
            population.V_L = self.neuron_dict['V_L'][i]
            population.C_m = self.neuron_dict['C_m'][i]
            population.g_L = self.neuron_dict['g_L'][i]
            population.V_I = receptors_V_I[i]

            self.pops.append(population)
            self.spike_monitors.append(SpikeMonitor(population))
        self.net_params.append(self.pops)

    def __connect_populations(self):
        self.synapses = []
        models = [get_ampa_model(), PV_MODEL, SST_MODEL, VIP_MODEL]
        on_pres = [ampa_on_pre, gaba_on_pre, gaba_on_pre, gaba_on_pre]
        on_posts = [ampa_on_post, gaba_on_post, gaba_on_post, gaba_on_post]
        for n, target_pop in enumerate(self.pops):
            for m, source_pop in enumerate(self.pops):
                connect_prob = self.net_dict['connect_probs'][n][m]
                if connect_prob == 0:
                    continue
                strength = self.net_dict['synaptic_strength'][n][m]

                synapse = Synapses(
                    source_pop, target_pop,
                    model=models[m],
                    on_pre=on_pres[m],
                    on_post=on_posts[m],
                    method='euler',
                    delay=self.net_dict['delay']
                )
                connect_kwargs = {'p': connect_prob}
                if m == n: connect_kwargs['condition'] = 'i != j'
                synapse.connect(**connect_kwargs)

                synapse.w = self.net_dict['global_g'] * strength / (connect_prob * self.net_dict['num_neurons'][m])
                if m == 0:
                    state_monitor = StateMonitor(synapse, ['w', 'c'], record=[_i for _i in range(128)])
                    self.weight_monitors.append(state_monitor)
                self.synapses.append(synapse)
        self.net_params.append(self.synapses)

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
            num_exposures=self.num_exposures, wait_durations=self.wait_durations, blasting=False
        )
        self.input_monitor = SpikeMonitor(self.input_neurons)
        # connect to excitatory neurons
        synapse = Synapses(self.input_neurons, self.pops[0], model=get_ampa_model(), **AMPA_PARAMS)
        synapse.connect(p=self.in_connection_avg / self.net_dict['num_neurons'][0])
        synapse.w = self.net_dict['global_g'] * 10000
        self.synapses.append(synapse)
        self.net_params.append(self.input_neurons)
        self.net_params.append(self.input_monitor)


    def run(self):
        self.net = Network(*self.net_params)
        self.net.run(self.duration)


def main(seed=0):
    np.random.seed(seed)
    log = setup_loggers('')

    simulation = Simulation(NET_DICT, NEURON_DICT, log)
    simulation.run()

    PLOTTING_PARAMS.simulation_duration = simulation.duration
    PLOTTING_PARAMS.plot_from = max(0, simulation.duration / ms - 2000)
    PLOTTING_PARAMS.update()

    fig, gs = get_plots_iterator()
    fig.add_subplot(gs.__next__())  # Skip the first subplot
    # fig.add_subplot(gs.__next__())
    # ax_input = fig.add_subplot(gs.__next__())
    # ax_output = fig.add_subplot(gs.__next__())
    # plot_heatmaps(ax_input, ax_output, None, simulation.weight_monitors[0])
    spike_raster(
        fig.add_subplot(gs.__next__()),
        simulation.input_monitor if hasattr(simulation, 'input_monitor') else None,
        simulation.spike_monitors[0], simulation.spike_monitors[1:],
        None
    )

    plt.savefig('cortical_column_learning.png')
    plt.show()


if __name__ == '__main__':
    main()
