import math

from tqdm import tqdm
from brian2 import *
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from src.equations.inhibitory_homeostasis import *
from src.equations.stdp_eqs import *
from src.input_from_csv import csv_input_neurons
from src.plotting import spike_raster, PLOTTING_PARAMS, get_plots_iterator, plot_dopamine, plot_output_potentials, \
    plot_heatmaps

# prefs.codegen.target = "numpy"

np.random.seed(1)

NUM_NEURONS = 32
NUM_INHIBITORY = 8
OUTPUT_NEURONS = 2
SAMPLE_DURATION = 100 * ms
NUM_EXPOSURES = 3
epochs = 128
wait_durations = 0
weight_coef = 0.4
hidden_connection_avg = 5
inhibitory_connection_avg = 8
in_connection_avg = 4

input_neurons, targets, input_dim, simulation_duration = csv_input_neurons(
    '../data/mini_sample.csv', duration=SAMPLE_DURATION, repeat_for=epochs, num_exposures=NUM_EXPOSURES,
    wait_durations=wait_durations, blasting=False
)
input_monitor = SpikeMonitor(input_neurons)

neurons = NeuronGroup(NUM_NEURONS, **NEURON_PARAMS)
neuron_monitor = SpikeMonitor(neurons)
neurons.v = El

inhibitory_neurons = NeuronGroup(NUM_INHIBITORY, **NEURON_PARAMS)
inhibitory_monitor = SpikeMonitor(inhibitory_neurons)
inhibitory_neurons.v = El

output_neurons = NeuronGroup(OUTPUT_NEURONS, **OUTPUT_NEURON_PARAMS)
output_neurons.v = OEl

output_monitor = SpikeMonitor(output_neurons)
output_state_monitor = StateMonitor(output_neurons, ['v', 'adaptation'], record=[0, 1])

input_synapse = Synapses(input_neurons, neurons, **SYNAPSE_PARAMS)
input_synapse.connect(p=in_connection_avg / NUM_NEURONS)

input_synapse.s = 0.75
input_synapse_monitor = StateMonitor(input_synapse, ['s'], record=True)

main_synapse = Synapses(neurons, neurons, **SYNAPSE_PARAMS)
main_synapse.connect(condition='i!=j', p=hidden_connection_avg / NUM_NEURONS)
main_synapse.s = 'weight_coef * rand()'

to_inhib_synapse = Synapses(neurons, inhibitory_neurons, **SYNAPSE_PARAMS)
to_inhib_synapse.connect(p=inhibitory_connection_avg / NUM_NEURONS)
to_inhib_synapse.s = 'weight_coef * rand()'

inhib_synapse = Synapses(inhibitory_neurons, neurons, **INHIBITORY_SYNAPSE_PARAMS)
inhib_synapse.connect(p=inhibitory_connection_avg / NUM_NEURONS)
inhib_synapse.s = 'inhib_s_initial * rand()'

output_synapse = Synapses(neurons, output_neurons, **SYNAPSE_PARAMS)
output_synapse.connect(p=hidden_connection_avg / NUM_NEURONS)
output_synapse.s = 'weight_coef * rand()'
output_synapse_monitor = StateMonitor(output_synapse, ['s', 'c'], record=True)

reward_synapses = []
for target in [input_synapse, main_synapse, output_synapse]:
    # + reward because 0 spiked (reward is negative for samples with answer 1)
    reward_synapses.append(Synapses(output_neurons[0], target, model='''''',
                               on_pre='''
                               d_post += (reward_value - expected_reward_pre)
                               ''',
                               method='exact'))
    reward_synapses[-1].connect()

    # - reward because 1 spiked
    reward_synapses.append(Synapses(output_neurons[1], target, model='''''',
                               on_pre='''
                               d_post -= (reward_value - expected_reward_pre)
                               ''',
                               method='exact'))
    reward_synapses[-1].connect()

dopamine_monitor = StateMonitor(input_synapse, ['d'], record=[0])
monitors = [input_monitor, neuron_monitor, inhibitory_monitor, output_monitor, dopamine_monitor]
if not PLOTTING_PARAMS.minimal_reporting:
    monitors += [output_state_monitor, input_synapse_monitor, output_synapse_monitor]

post_prediction_inhibitors = []
for target, value in zip([neurons, output_neurons], [1, 3]):
    post_prediction_inhibitors.append(Synapses(output_neurons, target, model='''''',
                                        on_pre=f'''ge_post -= {value}''',
                                        # delay=2*ms,
                                        method='exact'))
    post_prediction_inhibitors[-1].connect()

net = Network(input_neurons, neurons, inhibitory_neurons, output_neurons,
              input_synapse, main_synapse, to_inhib_synapse, inhib_synapse, output_synapse,
              *monitors, *reward_synapses, *post_prediction_inhibitors)


for sample_i in tqdm(range(math.floor(simulation_duration/SAMPLE_DURATION))):
    # assign negative reward to the second output neuron. its synapses subtract the reward
    reward_value = epsilon_dopa if targets[sample_i] == 0 else -epsilon_dopa
    net.run(SAMPLE_DURATION)
    output_neurons.rate = 0
    output_neurons.expected_reward[0], output_neurons.expected_reward[1] = (
        expected_reward_merge(output_neurons.expected_reward))
    # for reset_neurons in [output_neurons, neurons, inhibitory_neurons]:
    #     reset_neurons.v = El
    #     reset_neurons.ge = 0


# Visualisation
PLOTTING_PARAMS.simulation_duration = simulation_duration
PLOTTING_PARAMS.plot_from = max(0, simulation_duration / ms - 4000)
PLOTTING_PARAMS.update()

fig, gs = get_plots_iterator()
plot_dopamine(fig.add_subplot(gs.__next__()), dopamine_monitor)

if not PLOTTING_PARAMS.minimal_reporting:
    plot_output_potentials(fig.add_subplot(gs.__next__()), output_state_monitor, vt)

if PLOTTING_PARAMS.plot_heatmaps and not PLOTTING_PARAMS.minimal_reporting:
    ax_input = fig.add_subplot(gs.__next__())
    ax_output = fig.add_subplot(gs.__next__())
    plot_heatmaps(ax_input, ax_output, input_synapse_monitor, output_synapse_monitor, eligibility_trace=True)

spike_raster(fig.add_subplot(gs.__next__()), input_monitor, neuron_monitor, inhibitory_monitor, output_monitor)

plt.savefig('simple_learning.png')
plt.show()
