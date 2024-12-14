import datetime
from omegaconf import OmegaConf
import os
import logging
import pandas as pd
import sys


def save_config(cfg, run_dir): # Save config file explicitly
    with open(os.path.join(run_dir, "config.yaml"), 'w') as f:
        f.write(OmegaConf.to_yaml(cfg))

def create_run_folder(base_dir: str, experiment_type: str):
    run_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(base_dir, f"run_{run_id}_{experiment_type}")
    os.makedirs(run_dir, exist_ok=True)

    raster_plots_dir = os.path.join(run_dir, 'raster_plots') # Create folder for raster plots
    os.makedirs(raster_plots_dir, exist_ok=True)

    spike_times_dir = os.path.join(run_dir, 'spike_times') # Create folder to save csv files for spike times
    os.makedirs(spike_times_dir, exist_ok=True)

    metrics_dir = os.path.join(run_dir, 'metrics') # Create folder to save csv files for various metrics
    os.makedirs(metrics_dir, exist_ok=True)

    return run_dir, raster_plots_dir, spike_times_dir, metrics_dir

def setup_loggers(run_dir):
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG) # DEBUG level captures all messages

    console_handler = logging.StreamHandler(sys.stdout)

    # Create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    log.addHandler(console_handler)
    return log

def create_weights_dict(file_path):
    df = pd.read_csv(file_path)
    weights_dict = {}
    
    for index, row in df.iterrows():
        source = row['Source Population']
        target = row['Target Population']
        weight = row['Weight Value']
        
        if source not in weights_dict:
            weights_dict[source] = {}
        weights_dict[source][target] = weight
    
    return weights_dict