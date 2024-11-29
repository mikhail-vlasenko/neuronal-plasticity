import numpy as np
import pandas as pd
from brian2 import ms, SpikeGeneratorGroup, second


def csv_input_neurons(csv_path: str, duration, repeat_for=1, num_exposures=1):
    """
    Produces the input neurons from a CSV file.
    Also returns the input size and the simulation duration.
    """
    df = pd.read_csv(csv_path, dtype={'input': str, 'target': int})
    input_dim = None

    indices = []
    times = []
    pattern_duration = duration  # Duration for each pattern
    offset = 0
    targets = []

    # Loop through each input pattern
    for _ in range(repeat_for):
        for pattern_idx, row in df.iterrows():
            input_pattern = [int(x) for x in row['input']]  # Convert string to list of integers
            if input_dim is None:
                input_dim = len(input_pattern)
            else:
                assert len(input_pattern) == input_dim, \
                    f"All input patterns must have the same length, found {len(input_pattern)} and {input_dim}."

            # For each '1' in the pattern, an input neuron spikes
            for exposure in range(num_exposures):
                for i, val in enumerate(input_pattern):
                    if val == 1:
                        indices.append(i)  # Neuron index
                        times.append((offset + exposure / num_exposures / 2) * pattern_duration)
            offset += 1
            targets.append(row['target'])

    # Convert to arrays with proper units
    indices = np.array(indices)
    times = np.array(times) * second

    # Create input neurons
    input_neurons = SpikeGeneratorGroup(input_dim, indices, times)
    return input_neurons, targets, input_dim, len(df) * pattern_duration * repeat_for
