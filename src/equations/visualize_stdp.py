import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Parameters
ms = 0.001  # Convert ms to seconds for calculations
taupre = 20 * ms
taupost = taupre
gmax = 0.5
max_strength = 1
dApre = 0.1
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax
tauc = 25*ms

# Time window for simulation
dt = 0.1 * ms  # simulation time step
t_window = np.arange(-100 * ms, 100 * ms, dt)


def compute_weight_change(delta_t):
    """Compute weight change for a given time difference between pre and post spikes"""
    if delta_t > 0:  # Post after Pre
        # Pre spike at t=0, Post spike at t=delta_t
        Apre = dApre * np.exp(-delta_t / taupre)
        weight_change = Apre
    else:  # Pre after Post
        # Post spike at t=0, Pre spike at t=-delta_t
        Apost = dApost * np.exp(delta_t/taupost)
        weight_change = Apost

    return weight_change


# Calculate weight changes for different time differences
delta_ts = np.linspace(-50 * ms, 50 * ms, 1000)
weight_changes = [compute_weight_change(dt) for dt in delta_ts]

# Create the plot
plt.figure(figsize=(10, 6), dpi=200)
sns.set_style("whitegrid")

# Plot the STDP curve
plt.plot(delta_ts / ms, weight_changes, 'b-', linewidth=2)

# Add horizontal and vertical lines at zero
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

# Customize the plot
plt.xlabel('Δt (ms)', fontsize=12)
plt.ylabel('Eligibility Trace Change (Δc)', fontsize=12)
plt.title('Spike-Timing-Dependent Plasticity (STDP)', fontsize=14)

# Add text annotations explaining the timing
plt.text(25, max(weight_changes) / 2, 'Post after Pre\n(LTP)', horizontalalignment='center')
plt.text(-25, min(weight_changes) / 2, 'Pre after Post\n(LTD)', horizontalalignment='center')

# Set reasonable axis limits
plt.xlim(-50, 50)
y_max = max(abs(min(weight_changes)), abs(max(weight_changes)))
plt.ylim(-y_max * 1.1, y_max * 1.1)

# Show the plot
plt.tight_layout()
plt.savefig('stdp.png')
