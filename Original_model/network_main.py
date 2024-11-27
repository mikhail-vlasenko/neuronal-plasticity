from brian2 import *
import matplotlib.pyplot as plt
import numpy as np
import os
from pprint import pprint
from network_parameters import net_dict, neuron_dict, eqs_dict, receptors_dict
import csv
from collections import defaultdict
import hydra
from omegaconf import DictConfig
from omegaconf import OmegaConf
import logging
import pandas as pd

np.random.seed(net_dict['Seed']) # Set the seed of the simulation for reproducibility

class Network_main:
    """"
    Parameters
    ---------
    net_dict : dictionary
         Contains parameters specific to overall network (see: 'network_parameters.py').
    neuron_dict : dictionary
         Contains parameters specific to neuron used (see: 'network_parameters.py').
    receptors_dict : dictionary
         Contains parameters specific to AMPA, GABA, NMDA receptors (see: 'network_parameters.py').
    eqs_dict : dictionary
         Contains equations of neurons and specific to AMPA, GABA, NMDA receptors (see: 'network_parameters.py').
    """
    def __init__(self, net_dict, neuron_dict, receptors_dict, eqs_dict, log):
        self.net_dict = net_dict
        self.neuron_dict = neuron_dict
        self.receptors_dict = receptors_dict
        self.eqs_dict = eqs_dict
        self.log = log
        
        self.log.info('---------------------------------')
        self.log.info('      CORTICAL COLUMN MODEL')
        self.log.info('---------------------------------')
        self.num_pops = len(self.net_dict['populations']) # Number of populations
        self.log.info('Number of populations: %s', self.num_pops)
        self.num_neurons = self.net_dict['num_neurons'] # Number of neurons
        self.log.info(self.net_dict['num_neurons'])

    def create(self):
        """ Creates network populations and input.

        Neuronal populations and devices (recording and generators) are created.

        """
        self.__create_neuronal_populations()
        self.__create_poisson_bg_input()

    def connect(self, cfg):
        """ Connects the population and devices (recording and generators).

        Neuronal populations are connected between and within themselves,
        as well as generator devices and recording devices

        """
        
        self.__connect_poisson_bg_input()
        self.__connect_neuronal_populations(cfg)
        self.__connect_recording_devices()

    def simulate(self, t_sim):
        """ Simulates the network.

        Parameters
        ----------
        t_sim: Simulation time in ms.

        """
        @network_operation(dt=1*ms)
        
        def update_input(t):
            # Function in which variables can be changed during simulation time
            pass
            # if t>self.net_dict['t_start_DC'] and t<self.net_dict['t_end_DC']: # Add DC input to E4 starting at time t_start_DC and end at t_end_DC
            #     self.pops[5].I_DC_input = self.net_dict['I_DC'][5] # Value corresponding to E4
            #     #self.pops[insert_desired_population_index].I_DC_input = self.net_dict['I_DC'][insert_desired_population_index] # Value corresponding to insert_desired_population_index

            # else:
            #     self.pops[5].I_DC_input = 0.*pA
            #     #self.pops[insert_desired_population_index].I_DC_input = 0.*pA

        self.log.info('-----------------------------')
        self.log.info('Simulating')
        self.log.info('-----------------------------')
        # Here pay attention to add all synapses and objects (incl network operations) to self.net_mon, otherwise they won't be included in the sim!
        self.net_run = Network(update_input, self.spike_mon[:], self.rate_mon[:], self.pops, self.Poisson_groups[:], self.S_Poisson[:],
                                self.S_ampa[:], self.S_gaba[:], self.S_nmda[:]) # This uses Brian2 Network class to inlcude the monitors when running the simulation
        self.net_run.run(t_sim)

        self.log.info('Finished simulation')
        self.log.info('-----------------------------')


    def __create_neuronal_populations(self):
        """ Creates the neuronal populations with parameters defined in 'network_parameters.py'.

            Stores them in a list, pops
        """
        self.log.info('Creating neuronal populations')
        self.pops = []
        for m in np.arange(self.num_pops):
            Vth = self.neuron_dict['V_th'][m]
            Vrest = self.neuron_dict['V_reset'][m]
            V_L_i = self.neuron_dict['V_L'][m]
            C_m_i = self.neuron_dict['C_m'][m]
            g_L_i = self.neuron_dict['g_L'][m]
            population = NeuronGroup(self.net_dict['num_neurons'][m], model=self.eqs_dict['eqs_neuron'], threshold='v > v_th', # repr method to convert a Quantity object, which is a physical quantity with units, to a string that can be used in a string format expression.
                                    reset='v = v_rest', refractory=self.neuron_dict['tau_ref'][m], method='euler')
            for n in range(self.net_dict['num_neurons'][m]):
                population[n].v_th = self.neuron_dict['V_th'][m]
                population[n].v_rest = self.neuron_dict['V_reset'][m]
                population[n].v[0] = self.neuron_dict['V_0'][m]
            
            population.V_L = V_L_i # Set V_l for each population as in network_parameters
            population.C_m = C_m_i # Set C_m for each population as in network_parameters
            population.g_L = g_L_i # Set g_L for each population as in network_parameters
            population.V_I = receptors_dict['V_I'][m] # V_I for GABA
            population.I_DC_input = 0*pA # Initial DC input at time t = 0 set to 0pA, can be changed later in simulate function
            self.pops.append(population)

    def __create_poisson_bg_input(self):
        """ Creates Poisson background input ith parameters 
        as specified in 'network_parameters.py'.

            The same number of generators is created as neuronal populations.
            The number of neurons in each Poisson generator is equal to the
            number of neurons in the population it targets.

        """
        self.log.info('-----------------------------')
        self.log.info('Creating Poisson background input')
        self.log.info('-----------------------------')

        self.Poisson_groups = [] # List to hold Poisson background generators
        for n in np.arange(self.num_pops):
            Poisson_groups = PoissonGroup(self.net_dict['num_neurons'][n], rates=self.net_dict['bg_rate'][n])
            self.Poisson_groups.append(Poisson_groups)
    
    def __connect_neuronal_populations(self, cfg):
        """ Connects neuronal populations recurrently, with parameters
        as specified in 'network_parameters.py'.

            There are E-E, E-I, I-E and I-I connections.

        """
        self.log.info('-----------------------------')
        self.log.info('Connecting synapses (289)')
        self.log.info('-----------------------------')

        self.S_ampa = []
        self.S_nmda = []
        self.S_gaba = []
        # Excitatory are: [1, 5, 9, 13]
        # Inhibitory are: [0, 2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16]
        
        # Dictionary storing every population's equation and what should happen with every pre-synaptic spike
        # Excitatory populations have both AMPA and NMDA parameters
        pop_map = {
            0: ('INH', 'eqs_s_gaba_l1vip', ''),
            1: ('EXC', 'eqs_s_ampa_l23', 'eqs_s_nmda_l23'),
            2: ('INH', 'eqs_s_gaba_l23pv', ''),
            3: ('INH', 'eqs_s_gaba_l23sst', ''),
            4: ('INH', 'eqs_s_gaba_l23vip', ''),
            5: ('EXC', 'eqs_s_ampa_l4', 'eqs_s_nmda_l4'),
            6: ('INH', 'eqs_s_gaba_l4pv', ''),
            7: ('INH', 'eqs_s_gaba_l4sst', ''),
            8: ('INH', 'eqs_s_gaba_l4vip', ''),
            9: ('EXC', 'eqs_s_ampa_l5', 'eqs_s_nmda_l5'),
            10: ('INH', 'eqs_s_gaba_l5pv', ''),
            11: ('INH', 'eqs_s_gaba_l5sst', ''),
            12: ('INH', 'eqs_s_gaba_l5vip', ''),
            13: ('EXC', 'eqs_s_ampa_l6', 'eqs_s_nmda_l6'),
            14: ('INH', 'eqs_s_gaba_l6pv', ''),
            15: ('INH', 'eqs_s_gaba_l6sst', ''),
            16: ('INH', 'eqs_s_gaba_l6vip', ''),
        }
        iteration = 1
        # For each target, create synapses from all possible sources
        for n, target_pop in enumerate(self.pops):
            for m, source_pop in enumerate(self.pops, start=0):
                self.net_dict['connect_probs'][n][m] = float(self.net_dict['connect_probs'][n][m]) * cfg.synaptic_density
                print('Synapse', iteration)
                iteration += 1
                neuron_type, eq_1, eq_2 = pop_map[m]
                # GABA synapses
                if neuron_type == 'INH':
                    S = Synapses(source_pop, target_pop, model=self.eqs_dict[eq_1], on_pre='s_gaba += 1', method='euler')
                    if m == n:
                        S.connect(condition='i != j', p=self.net_dict['connect_probs'][n][m]) # Prevent auto-synapses
                    else:
                        S.connect(p=self.net_dict['connect_probs'][n][m])
                    if self.net_dict['connect_probs'][n][m] == 0 or self.net_dict['synaptic_strength'][n][m] == 0: # Condition to prevent division by 0 when calculating weight
                        S.w = 0
                    else:
                        S.w = self.net_dict['global_g']*self.net_dict['synaptic_strength'][n][m]/(self.net_dict['num_neurons'][m]*self.net_dict['connect_probs'][n][m]) # Formula for synaptic weight used in Giulia's model
                    S.delay = self.net_dict['delay']
                    self.S_gaba.append(S)
                    del S
                elif neuron_type == 'EXC':
                    # AMPA synapses
                    S = Synapses(source_pop, target_pop, model=self.eqs_dict[eq_1], on_pre='s_ampa += 1', method='euler')
                    if m == n:
                        S.connect(condition='i != j', p=self.net_dict['proportion_AMPA']*self.net_dict['connect_probs'][n][m]) # Prevent auto-synapses
                    else:
                        S.connect(p=self.net_dict['proportion_AMPA']*self.net_dict['connect_probs'][n][m])
                    if self.net_dict['connect_probs'][n][m] == 0 or self.net_dict['synaptic_strength'][n][m] == 0: # Condition to prevent division by 0 when calculating weight
                        S.w = 0
                    else:
                        S.w = self.net_dict['global_g']*self.net_dict['synaptic_strength'][n][m]/(self.net_dict['num_neurons'][m]*self.net_dict['proportion_AMPA']*self.net_dict['connect_probs'][n][m]) # Formula for synaptic weight used in Giulia's model
                    S.delay = self.net_dict['delay']
                    self.S_ampa.append(S)
                    del S

                    # NMDA synapses
                    S = Synapses(source_pop, target_pop, model=self.eqs_dict[eq_2], on_pre='x += 1', method='euler')
                    if m == n:
                        S.connect(condition='i != j', p=self.net_dict['proportion_NMDA']*self.net_dict['connect_probs'][n][m]) # Prevent auto-synapses
                    else:
                        S.connect(p=self.net_dict['proportion_NMDA']*self.net_dict['connect_probs'][n][m])
                    if self.net_dict['connect_probs'][n][m] == 0 or self.net_dict['synaptic_strength'][n][m] == 0: # Condition to prevent division by 0 when calculating weight
                        S.w = 0
                    else:
                        S.w = self.net_dict['global_g']*self.net_dict['synaptic_strength'][n][m]/(self.net_dict['num_neurons'][m]*self.net_dict['proportion_NMDA']*self.net_dict['connect_probs'][n][m]) # Formula for synaptic weight used in Giulia's model
                    S.delay = self.net_dict['delay']
                    self.S_nmda.append(S)
                    del S


    def __connect_poisson_bg_input(self):
        """ Connects generator devices as specified in 'network_parameters.py'.

            Connects Poisson background generator to each population.
        
        """
        self.log.info('Connecting Poisson background input')
        self.log.info('-----------------------------')

        self.S_Poisson = [] # List for Poisson background synapses
        for n in np.arange(self.num_pops):
            self.log.info('Connecting Poisson %s', n)
            S_Poisson = Synapses(self.Poisson_groups[n], self.pops[n], on_pre='s_ampa_ext += 1', method='euler')
            self.S_Poisson.append(S_Poisson)
            self.S_Poisson[n].connect(j='i') # Connects Poisson one-to-one

    def __connect_recording_devices(self):
        """ Creates the spike/voltage recording devices for each population.

            It automatically connects to the population specified.

        """
        self.log.info('-----------------------------')
        self.log.info('Connecting recording devices')

        self.spike_mon = list(range(self.num_pops)) # List of spike monitors
        self.rate_mon = list(range(self.num_pops)) # List of rate monitors
        for i in np.arange(self.num_pops):
            self.spike_mon[i] = SpikeMonitor(self.pops[i]) # Record from all neurons in each population
            self.rate_mon[i] = PopulationRateMonitor(self.pops[i])
    
    def plot_spikes(self, raster_plots_dir):
        """ Plots raster graphs after simulation is run.

        """
        list_ex = [1, 5, 9 , 13] # Indexes corresponding to excitatory populations
        color = ''
        for i in range(len(self.pops)):
            pop = self.net_dict['populations'][i]
            if i in list_ex:
                color = '.r' # Red for excitatory
            else:
                color = '.b' # Blue for inhibitory
            plt.figure(i)
            plt.plot(self.spike_mon[i].t/ms, self.spike_mon[i].i, color, label=pop)
            xlabel('Time (ms)')
            ylabel('Neuron index')
            legend()
            plt.savefig(os.path.join(raster_plots_dir, f"5000_spikes_population_{i}.png"))

    def firing_rates(self, t_sim, metrics_dir):
        """ Calculates and prints mean firing rates in spikes/s for each population.

        """
        avg_firing_rates = pd.DataFrame(columns=['Population', 'Avg Firing Rate Hz'])
        avg_firing_rates_path = os.path.join(metrics_dir, 'avg_firing_rates.csv')
        for i in range(self.num_pops):
            mean_rate = self.spike_mon[i].num_spikes/(self.net_dict['num_neurons'][i]*t_sim)
            self.log.info(f"Mean rate of population {self.net_dict['populations'][i]}: {mean_rate:.2f} Hz")

            new_row = [self.net_dict['populations'][i], f'{mean_rate:.2f}']
            avg_firing_rates.loc[len(avg_firing_rates)] = new_row
            avg_firing_rates.to_csv(avg_firing_rates_path, index=False)       

    def write_data(self, spike_times_dir):
        """ Creates files with spike data.
            For each population, create a csv file which has one column
            with the index of the neuron and the second column with
            a list containing the spike times (in s or ms) of that neuron.
            Saves them in a folder called Spike_times of the current run.
        """
        for n in range(self.num_pops):
            data = defaultdict(list)
            for i in range(len(self.spike_mon[n].i)):
                spike_time = self.spike_mon[n].t[i]
                data[self.spike_mon[n].i[i]].append(spike_time)
            with open(f"{spike_times_dir}/{self.net_dict['populations'][n]}.csv", 'w') as csv_file:
                writer = csv.writer(csv_file)
                for key, value in data.items():
                    writer.writerow([key, value])