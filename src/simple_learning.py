from urllib.error import URLError

from brian2 import *
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from src.equations.simple_stdp import *
from src.input_from_csv import csv_input_neurons


NUM_NEURONS = 8
OUTPUT_NEURONS = 2
SAMPLE_DURATION = 100 * ms
NUM_EXPOSURES = 2
OUTPUT_NEURON_PARAMS['refractory'] = SAMPLE_DURATION * 0.9
epochs = 4
weight_coef = 0.5

input_neurons, input_dim, simulation_duration = csv_input_neurons(
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

input_synapse = Synapses(input_neurons, neurons, **SYNAPSE_PARAMS)
# connect input to 2 of the "main" neurons
for i in range(input_dim):
    input_synapse.connect(i=i, j=[2 * i, 2 * i + 1])
input_synapse.s = 1
input_synapse_monitor = StateMonitor(input_synapse, ['s'], record=True)

# randomized all to all weights in the "main" neurons
main_synapse = Synapses(neurons, output_neurons, **SYNAPSE_PARAMS)
main_synapse.connect()  # All-to-all connectivity

main_synapse.s = 'weight_coef * rand()'
main_synapse_monitor = StateMonitor(main_synapse, ['s'], record=True)

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

completed = 0
while completed < simulation_duration:
    run(SAMPLE_DURATION)
    completed += SAMPLE_DURATION
    output_neurons.rate = 0
    output_neurons.v = OEl

# Visualisation
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = [15, 12]  # Made figure taller to accommodate new plot

# Create figure with custom layout
fig = plt.figure(constrained_layout=True, dpi=100)
gs = fig.add_gridspec(5, 1, height_ratios=[1, 1, 1, 1, 2])


def plot_neuron_potential(ax, state_monitor, neuron_idx=0):
    # Plot potential on the left y-axis
    sns.lineplot(x=state_monitor.t / ms,
                 y=state_monitor.v[neuron_idx] / mV,
                 color='black', ax=ax, label='Potential')
    ax.axhline(vt / mV, linestyle='dashed', color='gray', label='Threshold')
    ax.set_xlim([0, simulation_duration / ms])
    ax.set_ylabel('Post-neuron\npotential v(t) (mV)')
    ax.set_ylim([-80, -40])

    # Check if rate is available in state_monitor
    if hasattr(state_monitor, 'rate'):
        # Create twin axis for rate
        ax2 = ax.twinx()

        # Plot rate on the right y-axis
        sns.lineplot(x=state_monitor.t / ms,
                     y=state_monitor.rate[neuron_idx] / (mV / second),
                     color='blue', ax=ax2, label='Rate')
        ax2.set_ylabel('Rate (mV/s)', color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')

        # Combine legends from both axes
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

        # Remove the original legend if it exists
        if ax.get_legend():
            ax.get_legend().remove()
    else:
        # If no rate data, just show legend for potential
        ax.legend(loc='upper right')

    return ax

plot_neuron_potential(fig.add_subplot(gs[0]), state_monitor, neuron_idx=0)
plot_neuron_potential(fig.add_subplot(gs[1]), state_monitor, neuron_idx=1)

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
main_synapse_data = main_synapse_monitor.s[:]
times_main = main_synapse_monitor.t/ms

# Create heatmap for main synapses
sns.heatmap(main_synapse_data,
            ax=ax_main,
            cmap='viridis',
            xticklabels=False,
            cbar_kws={'label': 'Strength'},
            robust=True)
ax_main.set_ylabel('Main synapse index')
ax_main.set_title('Main synaptic strengths over time')

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

try:
    plt.show()
except Exception as e:
    print(f'Error during plotting: {e}')
    try:
        time.sleep(2)
        plt.show()
    except Exception as e:
        plt.savefig('simple_learning.png')
