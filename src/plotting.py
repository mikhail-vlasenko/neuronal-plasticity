from dataclasses import dataclass
import seaborn as sns
from brian2 import ms, mV, second
from matplotlib import pyplot as plt


@dataclass
class PlottingParams:
    simulation_duration: int = 0 * ms
    plot_from: int = 0
    plot_heatmaps: bool = True
    plot_adaptation: bool = True
    minimal_reporting: bool = True
    xlim: list = None

    def update(self):
        self.xlim = [self.plot_from, self.simulation_duration / ms]


PLOTTING_PARAMS = PlottingParams()
PLOTTING_PARAMS.update()


def get_plots_iterator():
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = [15, 12]

    fig = plt.figure(constrained_layout=True, dpi=100)
    if PLOTTING_PARAMS.minimal_reporting:
        height_ratios = [1, 3]
    elif PLOTTING_PARAMS.plot_heatmaps:
        height_ratios = [1, 1, 1, 1, 2]
    else:
        height_ratios = [1, 1, 2]
    return fig, iter(fig.add_gridspec(len(height_ratios), 1, height_ratios=height_ratios))

def plot_dopamine(ax, dopamine_monitor):
    ax.plot(dopamine_monitor.t / ms, dopamine_monitor.d[0])
    ax.set_xlim(PLOTTING_PARAMS.xlim)
    ax.set_xticklabels([])
    ax.set_ylabel('Dopamine level')
    ax.set_title('Dopamine level over time')

def plot_output_potentials(ax, output_state_monitor, vt):
    if PLOTTING_PARAMS.plot_adaptation:
        ax12 = ax.twinx()

    # Plot potential on the left y-axis
    for neuron_idx in range(2):
        sns.lineplot(x=output_state_monitor.t / ms,
                     y=output_state_monitor.v[neuron_idx] / mV,
                     ax=ax, label=f'Neuron {neuron_idx}')
        if PLOTTING_PARAMS.plot_adaptation:
            sns.lineplot(x=output_state_monitor.t / ms,
                         y=output_state_monitor.adaptation[neuron_idx] / (mV / second),
                         color='blue', ax=ax12)
    ax.axhline(vt / mV, linestyle='dashed', color='gray', label='Threshold')
    ax.set_xlim(PLOTTING_PARAMS.xlim)
    ax.set_ylabel('Output neuron\npotential v(t) (mV)')
    ax.set_ylim([-90, -50])
    if PLOTTING_PARAMS.plot_adaptation:
        ax12.set_ylabel('Adaptation (mV)', color='blue')
        ax12.tick_params(axis='y', labelcolor='blue')
    ax.legend(loc='upper left')

def plot_heatmaps(ax_input, ax_output, input_synapse_monitor, output_synapse_monitor, eligibility_trace=False):
    if eligibility_trace:
        input_synapse_data = output_synapse_monitor.c[:]
        sns.heatmap(input_synapse_data,
                    ax=ax_input,
                    cmap='viridis',
                    xticklabels=False,
                    cbar_kws={'label': 'Eligibility trace'})
        ax_input.set_ylabel('Output synapse index')
        ax_input.set_title('Output eligibility traces over time')
    else:
        input_synapse_data = input_synapse_monitor.s[:]
        sns.heatmap(input_synapse_data,
                    ax=ax_input,
                    cmap='viridis',
                    xticklabels=False,
                    cbar_kws={'label': 'Strength'})
        ax_input.set_ylabel('Input synapse index')
        ax_input.set_title('Input synaptic strengths over time')

    out_synapse_data = output_synapse_monitor.s[:]
    sns.heatmap(out_synapse_data,
                ax=ax_output,
                cmap='viridis',
                xticklabels=False,
                cbar_kws={'label': 'Strength'})
    ax_output.set_ylabel('Output synapse index')
    ax_output.set_title('Output synaptic strengths over time')


def spike_raster(ax, input_monitor, neuron_monitor, inhibitory_monitor, output_monitor):
    ax.scatter(input_monitor.t / ms, input_monitor.i,
               c='blue', label='Input', s=20)
    ax.scatter(neuron_monitor.t / ms, neuron_monitor.i + (offset := len(input_monitor.source)),
               c='green', label='Hidden', s=20)
    ax.scatter(inhibitory_monitor.t / ms, inhibitory_monitor.i + (offset := offset + len(neuron_monitor.source)),
               c='orange', label='Inhibitory', s=20)
    ax.scatter(output_monitor.t / ms, output_monitor.i + (offset := offset + len(inhibitory_monitor.source)),
               c='red', label='Output', s=20)

    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Neuron index')
    ax.legend()
    ax.set_xlim(PLOTTING_PARAMS.xlim)
    ax.set_ylim([-1, offset + len(output_monitor.source)])
