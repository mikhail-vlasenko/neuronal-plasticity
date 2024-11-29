from brian2 import *
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from src.equations.simple_stdp import *
from src.input_from_csv import csv_input_neurons


NUM_NEURONS = 8
OUTPUT_NEURONS = 2
SAMPLE_DURATION = 1. * second
input_neurons, input_dim, simulation_duration = csv_input_neurons('../data/mini_sample.csv', duration=SAMPLE_DURATION)

neurons = NeuronGroup(NUM_NEURONS, **NEURON_PARAMS)
neurons.v = vr

output_neurons = NeuronGroup(OUTPUT_NEURONS, **OUTPUT_NEURON_PARAMS)
output_neurons.v = vr

output_monitor = SpikeMonitor(output_neurons)
state_monitor = StateMonitor(neurons, 'v', record=[0, 1])

input_synapse = Synapses(input_neurons, neurons, **SYNAPSE_PARAMS)
# connect input to 2 "main" neurons
for i in range(input_dim):
    input_synapse.connect(i=i, j=[2 * i, 2 * i + 1])
input_synapse.s = 1

# randomized all to all weights in the "main" neurons
main_synapse = Synapses(neurons, output_neurons, **SYNAPSE_PARAMS)
main_synapse.connect()  # All-to-all connectivity

main_synapse.s = '-0.1 + 0.6*rand()'

reward_value = 5e-3  # epsilon_dopa
expected_reward = 0
# + reward because correct answer is 0, and 0 spiked
reward_synapse0 = Synapses(output_neurons[0], main_synapse, model='''''',
                            on_pre='''d_post += reward_value''',
                            method='exact')
# - reward because correct answer is 0, while 1 spiked
reward_synapse1 = Synapses(output_neurons[1], main_synapse, model='''''',
                            on_pre='''d_post -= reward_value''',
                            method='exact')
reward_synapse0.connect()
reward_synapse1.connect()

run(simulation_duration)

# Visualisation
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = [15, 8]

# Create figure with custom layout
fig = plt.figure(constrained_layout=True, dpi=100)
gs = fig.add_gridspec(5, 1, height_ratios=[1, 1, 1, 1, 1])

# potential of the first output neuron
ax1 = fig.add_subplot(gs[0])
sns.lineplot(x=state_monitor.t / ms,
            y=state_monitor.v[0] / mV,
            color='black', ax=ax1)
ax1.axhline(vt/mV, linestyle='dashed', color='gray', label='Threshold')
ax1.set_xlim([0, simulation_duration/second])
ax1.set_ylabel('Post-neuron\npotential v(t)')
ax1.set_ylim([-80, -40])

# potential of the second output neuron
ax2 = fig.add_subplot(gs[1])
sns.lineplot(x=state_monitor.t / ms,
            y=state_monitor.v[1] / mV,
            color='black', ax=ax2)
ax2.axhline(vt/mV, linestyle='dashed', color='gray', label='Threshold')
ax2.set_xlim([0, simulation_duration/second])
ax2.set_ylabel('Post-neuron\npotential v(t)')
ax2.set_ylim([-80, -40])

try:
    plt.show()
except ConnectionResetError:
    try:
        time.sleep(2)
        plt.show()
    except ConnectionResetError:
        plt.savefig('simple_learning.png')

