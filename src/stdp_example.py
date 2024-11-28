from brian2 import *
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Parameters
simulation_duration = 6 * second

## Neurons
taum = 10*ms
Ee = 0*mV
vt = -58.5*mV  # was -54
vr = -60*mV
El = -74*mV  # what is this?
taue = 5*ms

## STDP
taupre = 20*ms
taupost = taupre
gmax = 1  # todo: what is this?
dApre = .01  # and this?
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax

## Dopamine signaling
tauc = 1000*ms
taud = 200*ms
taus = 1e-2*ms  # changed from 1, looks like lr?
epsilon_dopa = 5e-3

# Setting the stage

## Stimuli section
input_indices = array([0,
                       0, 1, 0, 1, 1, 0,
                       0, 1, 0, 1,
                       0])
input_times = array([500,
                     1000, 1050, 1500, 1510, 2000, 2010,
                     3500, 3550, 4000, 4010,
                     5500])*ms
spike_input = SpikeGeneratorGroup(2, input_indices, input_times)

neurons = NeuronGroup(2, '''dv/dt = (ge * (Ee-v) + El - v) / taum : volt
                            dge/dt = -ge / taue : 1''',
                      threshold='v>vt', reset='v = vr', refractory=10*ms,
                      method='euler')
neurons.v = vr
neurons_monitor = SpikeMonitor(neurons)
state_monitor = StateMonitor(neurons, 'v', record=1)


synapse = Synapses(spike_input, neurons,
                   model='''s: volt''',
                   on_pre='v += s')
synapse.connect(i=[0, 1], j=[0, 1])
synapse.s = 100. * mV

## STDP section
synapse_stdp = Synapses(neurons, neurons,
                   model='''
                         dc/dt = -c / tauc : 1 (clock-driven)
                         dd/dt = -d / taud : 1 (clock-driven)
                         ds/dt = c * d / taus : 1 (clock-driven)
                         dApre/dt = -Apre / taupre : 1 (event-driven)
                         dApost/dt = -Apost / taupost : 1 (event-driven)''',
                   on_pre='''ge += s
                          Apre += dApre
                          c = clip(c + Apost, -gmax, gmax)
                          s = clip(s, -gmax, gmax)
                          ''',
                   on_post='''Apost += dApost
                          c = clip(c + Apre, -gmax, gmax)
                          s = clip(s, -gmax, gmax)
                          ''',
                   method='euler'
                   )
synapse_stdp.connect(i=0, j=1)
synapse_stdp.s = 1e-10
synapse_stdp.c = 1e-10
synapse_stdp.d = 0
synapse_stdp_monitor = StateMonitor(synapse_stdp, ['s', 'c', 'd'], record=[0])

## Dopamine signaling section
dopamine_indices = array([0, 0, 0, 0, 0])
dopamine_times = array([1020, 1520, 2020, 3520, 4020])*ms
dopamine = SpikeGeneratorGroup(1, dopamine_indices, dopamine_times)
dopamine_monitor = SpikeMonitor(dopamine)
reward = Synapses(dopamine, synapse_stdp, model='''''',
                            on_pre='''d_post += epsilon_dopa''',
                            method='exact')
reward.connect()

# Simulation
## Dopamine modulated STDP
run(simulation_duration)


# Visualisation
dopamine_indices, dopamine_times = dopamine_monitor.it
neurons_indices, neurons_times = neurons_monitor.it

# Set the style for all plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = [15, 8]

# Create figure with custom layout
fig = plt.figure(constrained_layout=True, dpi=100)
gs = fig.add_gridspec(5, 1, height_ratios=[1, 1, 1, 1, 1])

# Plot 1: Spike and reward timing
ax1 = fig.add_subplot(gs[0])
sns.scatterplot(x=np.array(neurons_times), y=np.array(neurons_indices),
                color='blue', s=100, label='Neuron spikes', ax=ax1)
sns.scatterplot(x=np.array(dopamine_times), y=np.array(dopamine_indices) + 2,
                color='red', s=100, label='Reward', ax=ax1)
ax1.set_xlim([0, simulation_duration/second])
ax1.set_ylim([-0.5, 3])
ax1.set_yticks([0, 1, 2])
ax1.set_yticklabels(['Pre-neuron', 'Post-neuron', 'Reward'])
ax1.set_xticks([])

# Plot 2: Extracellular dopamine
ax2 = fig.add_subplot(gs[1])
sns.lineplot(x=synapse_stdp_monitor.t/second,
            y=synapse_stdp_monitor.d.T.flatten()/gmax,
            color='red', ax=ax2)
ax2.set_xlim([0, simulation_duration/second])
ax2.set_ylabel('Extracellular\ndopamine d(t)')
ax2.set_xticks([])

# Plot 3: Eligibility trace
ax3 = fig.add_subplot(gs[2])
sns.lineplot(x=synapse_stdp_monitor.t/second,
            y=synapse_stdp_monitor.c.T.flatten()/gmax,
            color='blue', ax=ax3)
ax3.set_xlim([0, simulation_duration/second])
ax3.set_ylabel('Eligibility\ntrace c(t)')
ax3.set_xticks([])

# Plot 4: Synaptic strength
ax4 = fig.add_subplot(gs[3])
sns.lineplot(x=synapse_stdp_monitor.t/second,
            y=synapse_stdp_monitor.s.T.flatten()/gmax,
            color='green', ax=ax4)
ax4.set_xlim([0, simulation_duration/second])
ax4.set_ylabel('Synaptic\nstrength s(t)')
ax4.set_xticks([])

# todo: i dont see the spike going into positive potential, does it matter?
# Plot 5: Postsynaptic potential
potential = state_monitor.v.T.flatten()/mV
ax5 = fig.add_subplot(gs[4])
sns.lineplot(x=state_monitor.t/second,
            y=potential,
            color='black', ax=ax5)
# plot the threshold
ax5.axhline(vt/mV, linestyle='dashed', color='gray', label='Threshold')
ax5.set_xlim([0, simulation_duration/second])
ax5.set_ylabel('Post-neuron\npotential v(t)')
ax5.set_ylim([-80, -40])
ax5.legend()

ax5.set_xlabel('Time (s)')
# Add title describing the model
plt.suptitle('Dopamine Modulated STDP', fontsize=16)

plt.show()
