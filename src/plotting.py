from dataclasses import dataclass
from typing import Union, List

import seaborn as sns
from brian2 import ms, mV, second, SpikeMonitor
from matplotlib import pyplot as plt


@dataclass
class PlottingParams:
    simulation_duration: int = 0 * ms
    plot_from: int = 0
    spike_raster_gaps: int = 10
    plot_heatmaps: bool = False
    plot_adaptation: bool = False
    plot_currents: bool = False
    minimal_reporting: bool = False
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
        height_ratios = [1, 1, 4]
    return fig, iter(fig.add_gridspec(len(height_ratios), 1, height_ratios=height_ratios))

def plot_dopamine(ax, dopamine_monitor):
    mask = (dopamine_monitor.t / ms >= PLOTTING_PARAMS.plot_from)
    ax.plot(dopamine_monitor.t[mask] / ms, dopamine_monitor.d[0][mask])
    ax.set_xlim(PLOTTING_PARAMS.xlim)
    ax.set_xticklabels([])
    ax.set_ylabel('Dopamine level')
    ax.set_title('Dopamine level over time')

def plot_output_potentials(ax, output_state_monitor, vt):
    if PLOTTING_PARAMS.plot_adaptation or PLOTTING_PARAMS.plot_currents:
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
        if PLOTTING_PARAMS.plot_currents:
            sns.lineplot(x=output_state_monitor.t / ms,
                         y=output_state_monitor.s_gaba_prediction[neuron_idx],
                         color='red', ax=ax12)
    ax.axhline(vt / mV, linestyle='dashed', color='gray', label='Threshold')
    ax.set_xlim(PLOTTING_PARAMS.xlim)
    ax.set_ylabel('Output neuron\npotential v(t) (mV)')
    ax.set_ylim([-90, vt / mV + 5])
    if PLOTTING_PARAMS.plot_adaptation:
        ax12.set_ylabel('Adaptation (mV)', color='blue')
        ax12.tick_params(axis='y', labelcolor='blue')
    if PLOTTING_PARAMS.plot_currents:
        ax12.set_ylabel('GABA current (nA)', color='red')
        ax12.tick_params(axis='y', labelcolor='red')
    ax.legend(loc='upper left')

def plot_heatmaps(ax_input, ax_output, input_synapse_monitor, output_synapse_monitor, eligibility_trace=False):
    xlim = [PLOTTING_PARAMS.xlim[0] * ms / output_synapse_monitor.clock.dt,
            PLOTTING_PARAMS.xlim[1] * ms / output_synapse_monitor.clock.dt]
    if eligibility_trace or input_synapse_monitor is None:
        eligibility_trace_data = output_synapse_monitor.c[:]
        sns.heatmap(eligibility_trace_data,
                    ax=ax_input,
                    cmap='viridis',
                    xticklabels=False,
                    cbar_kws={'label': 'Eligibility trace'})
        ax_input.set_ylabel('Output synapse index')
        ax_input.set_title('Output eligibility traces over time')
    else:
        if hasattr(input_synapse_monitor, 's'):
            input_synapse_data = input_synapse_monitor.s[:]
        else:
            input_synapse_data = input_synapse_monitor.w[:]
        sns.heatmap(input_synapse_data,
                    ax=ax_input,
                    cmap='viridis',
                    xticklabels=False,
                    cbar_kws={'label': 'Strength'})
        ax_input.set_ylabel('Input synapse index')
        ax_input.set_title('Input synaptic strengths over time')
    ax_input.set_xlim(xlim)

    if hasattr(output_synapse_monitor, 's'):
        out_synapse_data = output_synapse_monitor.s[:]
    else:
        out_synapse_data = output_synapse_monitor.w[:]
    sns.heatmap(out_synapse_data,
                ax=ax_output,
                cmap='viridis',
                xticklabels=False,
                cbar_kws={'label': 'Strength'})
    ax_output.set_ylabel('Output synapse index')
    ax_output.set_title('Output synaptic strengths over time')
    ax_output.set_xlim(xlim)


def spike_raster(
        ax,
        input_monitor,
        neuron_monitor: SpikeMonitor,
        inhibitory_monitor: Union[SpikeMonitor, List[SpikeMonitor]],
        output_monitor
):
    def crop_data(monitor, offset=0):
        mask = ((monitor.t / ms) >= PLOTTING_PARAMS.plot_from)
        return monitor.t[mask] / ms, monitor.i[mask] + offset

    colors = ['blue', 'green', 'orange', 'red']
    labels = ['Input', 'Excitatory', 'Inhibitory', 'Output']
    if isinstance(inhibitory_monitor, list):
        monitors = [input_monitor, neuron_monitor, *inhibitory_monitor, output_monitor]
        colors = ['blue', 'green', 'orange', 'peru', 'yellow', 'red']
        labels = ['Input', 'Excitatory', 'PV', 'SST', 'VIP', 'Output']
    else:
        monitors = [input_monitor, neuron_monitor, inhibitory_monitor, output_monitor]

    offset = PLOTTING_PARAMS.spike_raster_gaps
    for monitor, color, label in zip(monitors, colors, labels):
        if monitor is None:
            continue
        ax.scatter(*crop_data(monitor, offset),
                   c=color, label=label, s=20)
        offset += len(monitor.source) + PLOTTING_PARAMS.spike_raster_gaps

    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Neuron index')
    ax.legend()
    ax.set_xlim(PLOTTING_PARAMS.xlim)
    ax.set_ylim([-1, offset])
