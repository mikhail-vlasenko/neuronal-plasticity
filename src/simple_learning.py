import math

from brian2 import *
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from src.equations.simple_stdp import *
from src.input_from_csv import csv_input_neurons


np.random.seed(1)

NUM_NEURONS = 32
OUTPUT_NEURONS = 2
SAMPLE_DURATION = 100 * ms
NUM_EXPOSURES = 4
OUTPUT_NEURON_PARAMS['refractory'] = SAMPLE_DURATION * 0.9
epochs = 4
weight_coef = 0.3
reward_value = epsilon_dopa

input_neurons, targets, input_dim, simulation_duration = csv_input_neurons(
    '../data/mini_sample.csv', duration=SAMPLE_DURATION, repeat_for=epochs, num_exposures=NUM_EXPOSURES
)
input_monitor = SpikeMonitor(input_neurons)

neurons = NeuronGroup(NUM_NEURONS, **NEURON_PARAMS)
neuron_monitor = SpikeMonitor(neurons)
neurons.v = El

output_neurons = NeuronGroup(OUTPUT_NEURONS, **OUTPUT_NEURON_PARAMS)
output_neurons.v = OEl

output_monitor = SpikeMonitor(output_neurons)
state_monitor = StateMonitor(output_neurons, ['v', 'rate'], record=[0, 1])
monitors = [input_monitor, neuron_monitor, output_monitor, state_monitor]

input_synapse = Synapses(input_neurons, neurons, **SYNAPSE_PARAMS)
# connect input to 2 of the "main" neurons
for input_idx in range(input_dim):
    input_synapse.connect(i=input_idx, j=[2 * input_idx, 2 * input_idx + 1])

input_synapse.s = 1
input_synapse_monitor = StateMonitor(input_synapse, ['s'], record=True)

main_synapse = Synapses(neurons, neurons, **SYNAPSE_PARAMS)
main_synapse.connect(condition='i!=j', p=0.5)
main_synapse.s = 'weight_coef * rand()'

output_synapse = Synapses(neurons, output_neurons, **SYNAPSE_PARAMS)
output_synapse.connect(p=0.25)

output_synapse.s = 'weight_coef * rand()'
output_synapse_monitor = StateMonitor(output_synapse, ['s'], record=True)
monitors += [input_synapse_monitor, output_synapse_monitor]

expected_reward = 0
reward_synapses = []
for target in [input_synapse, main_synapse, output_synapse]:
    # + reward because 0 spiked (reward is negative for samples with answer 1)
    reward_synapses.append(Synapses(output_neurons[0], target, model='''''',
                               on_pre='''d_post += reward_value''',
                               method='exact'))
    reward_synapses[-1].connect()

    # - reward because 1 spiked
    reward_synapses.append(Synapses(output_neurons[1], target, model='''''',
                               on_pre='''d_post -= reward_value''',
                               method='exact'))
    reward_synapses[-1].connect()

dopamine_monitor = StateMonitor(input_synapse, ['d'], record=[0])
monitors.append(dopamine_monitor)

post_prediction_inhibitors = []
for target in [neurons, output_neurons]:
    post_prediction_inhibitors.append(Synapses(output_neurons, target, model='''''',
                                        on_pre='''
                                        v_post = El
                                        ge = 0
                                        ''',
                                        method='exact'))
    post_prediction_inhibitors[-1].connect()

net = Network(input_neurons, neurons, output_neurons, input_synapse, main_synapse, output_synapse,
              *monitors, *reward_synapses, *post_prediction_inhibitors)


for sample_i in range(math.floor(simulation_duration/SAMPLE_DURATION)):
    reward_value = abs(reward_value) if targets[sample_i] == 0 else -abs(reward_value)
    net.run(SAMPLE_DURATION)
    output_neurons.rate = 0
    output_neurons.v = OEl

# Visualisation
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = [15, 12]  # Made figure taller to accommodate new plot

# Create figure with custom layout
fig = plt.figure(constrained_layout=True, dpi=100)
gs = fig.add_gridspec(5, 1, height_ratios=[1, 1, 1, 1, 2])

ax0 = fig.add_subplot(gs[0])
ax0.plot(dopamine_monitor.t / ms, dopamine_monitor.d[0])
ax0.set_ylabel('Dopamine level')
ax0.set_title('Dopamine level over time')


ax1 = fig.add_subplot(gs[1])
ax12 = ax1.twinx()

# Plot potential on the left y-axis
for neuron_idx in range(2):
    sns.lineplot(x=state_monitor.t / ms,
                 y=state_monitor.v[neuron_idx] / mV,
                 ax=ax1, label='Potential')
    sns.lineplot(x=state_monitor.t / ms,
                 y=state_monitor.rate[neuron_idx] / (mV / second),
                 color='blue', ax=ax12, label='Rate')
ax1.axhline(vt / mV, linestyle='dashed', color='gray', label='Threshold')
ax1.set_xlim([0, simulation_duration / ms])
ax1.set_ylabel('Output neuron\npotential v(t) (mV)')
ax1.set_ylim([-80, -40])
ax12.set_ylabel('Rate (mV/s)', color='blue')
ax12.tick_params(axis='y', labelcolor='blue')
ax12.legend(loc='upper right')
ax1.legend(loc='upper left')

# Plot synaptic strengths as heatmaps
ax_input = fig.add_subplot(gs[2])
ax_main = fig.add_subplot(gs[3])

# Process input synapse data
input_synapse_data = input_synapse_monitor.s[:]
times_input = input_synapse_monitor.t/ms

# Create heatmap for input synapses
sns.heatmap(input_synapse_data,
            ax=ax_input,
            cmap='viridis',
            xticklabels=False,
            cbar_kws={'label': 'Strength'},
            robust=True)
ax_input.set_ylabel('Input synapse index')
ax_input.set_title('Input synaptic strengths over time')

# Process main synapse data
out_synapse_data = output_synapse_monitor.s[:]
times_main = output_synapse_monitor.t / ms

print(f'Weight delta:\n{(out_synapse_data.T[-1] - out_synapse_data.T[0])}')

# Create heatmap for main synapses
sns.heatmap(out_synapse_data,
            ax=ax_main,
            cmap='viridis',
            xticklabels=False,
            cbar_kws={'label': 'Strength'},
            robust=True)
ax_main.set_ylabel('Output synapse index')
ax_main.set_title('Output synaptic strengths over time')

# Add spike raster plot
ax3 = fig.add_subplot(gs[4:])
ax3.scatter(input_monitor.t/ms, input_monitor.i, c='blue', label='Input neurons', s=20)

# Plot spikes for middle layer neurons
ax3.scatter(neuron_monitor.t/ms, neuron_monitor.i + input_dim, c='green', label='Hidden neurons', s=20)

# Plot spikes for output neurons
ax3.scatter(output_monitor.t/ms, output_monitor.i + input_dim + NUM_NEURONS, c='red', label='Output neurons', s=20)

ax3.set_xlabel('Time (ms)')
ax3.set_ylabel('Neuron index')
ax3.legend()
ax3.set_xlim([-0.02, simulation_duration/ms])
ax3.set_ylim([-1, input_dim + NUM_NEURONS + OUTPUT_NEURONS])

plt.savefig('simple_learning.png')
plt.show()
