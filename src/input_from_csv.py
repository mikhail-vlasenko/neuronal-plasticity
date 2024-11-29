import numpy as np
import pandas as pd
from brian2 import ms, second, SpikeGeneratorGroup


def csv_input_neurons(csv_path: str, duration = 1.0 * second):
    """
    Produces the input neurons from a CSV file.
    Also returns the input size and the simulation duration.
    """
    df = pd.read_csv(csv_path, dtype={'input': str})
    input_dim = None

    indices = []
    times = []
    pattern_duration = duration  # Duration for each pattern

    # Loop through each input pattern
    for pattern_idx, row in df.iterrows():
        input_pattern = [int(x) for x in row['input']]  # Convert string to list of integers
        if input_dim is None:
            input_dim = len(input_pattern)
        else:
            assert len(input_pattern) == input_dim, \
                f"All input patterns must have the same length, found {len(input_pattern)} and {input_dim}."

        # For each '1' in the pattern, an input neuron spikes
        for i, val in enumerate(input_pattern):
            if val == 1:
                indices.append(i)  # Neuron index
                times.append(int(pattern_idx) * pattern_duration)

    # Convert to arrays with proper units
    indices = np.array(indices)
    times = np.array(times) * second

    # Create input neurons
    input_neurons = SpikeGeneratorGroup(input_dim, indices, times)
    return input_neurons, input_dim, len(df) * pattern_duration
