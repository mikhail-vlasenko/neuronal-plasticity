from brian2 import *
import network_main
from network_parameters import net_dict, neuron_dict, receptors_dict, eqs_dict
from utils.utils import save_config, create_run_folder, setup_loggers
import csv
import pandas as pd
from collections import defaultdict
import hydra
from omegaconf import DictConfig
from omegaconf import OmegaConf
import os
import logging
import brian2cuda

set_device("cuda_standalone")

defaultclock.dt = 0.1*ms # Time resolution of the simulation
np.random.seed(net_dict['Seed']) 
@hydra.main(version_base=None, config_path='config', config_name='config.yaml')
def main(cfg: DictConfig):
    t_sim = cfg.t_sim * ms # Simulation time - needs to be in ms in config file
    EXPERIMENT_PATH = os.environ.get('EXPERIMENT_PATH', 'experiments') # Path of directory where experiments are saved
    experiment_dir = EXPERIMENT_PATH
    run_dir, raster_plots_dir, spike_times_dir, metrics_dir = create_run_folder(experiment_dir, cfg.experiment_type)
    save_config(cfg, run_dir)
    log = setup_loggers(run_dir)

    net = network_main.Network_main(net_dict, neuron_dict, receptors_dict, eqs_dict, log)
    net.create()
    net.connect(cfg)
    net.simulate(t_sim)
    net.plot_spikes(raster_plots_dir)
    net.firing_rates(t_sim, metrics_dir)
    net.write_data(spike_times_dir)

if __name__ == "__main__":
    main()