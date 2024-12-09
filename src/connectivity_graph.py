import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def visualize_network_connectivity(neuron_groups, synapses, figsize=(12, 8)):
    """
    Visualize network connectivity as a graph with neurons spatially grouped by name
    and arrows for connections.

    Parameters:
    -----------
    neuron_groups : dict
        Dictionary with group names as keys and NeuronGroup objects as values
    synapses : dict
        Dictionary with synapse names as keys and Synapses objects as values
    figsize : tuple
        Size of the figure (width, height)
    """
    import networkx as nx
    import numpy as np
    import matplotlib.pyplot as plt

    # Create directed graph
    G = nx.DiGraph()

    # Colors for different neuron groups
    colors = ['blue', 'green', 'orange', 'red']

    # Initialize position dictionaries and colors
    pos = {}
    node_colors = []
    color_map = {}

    assert len(neuron_groups) == 4, "This function is designed for 4 neuron groups"

    group_centers = {
        'input': (0, 1),
        'hidden': (0, 0.5),
        'inhibitory': (0.5, 0.5),
        'output': (0, 0)
    }

    # Add nodes for each neuron group with positions relative to group centers
    offset = 0
    for idx, (name, group) in enumerate(neuron_groups.items()):
        color = colors[idx % len(colors)]
        color_map[name] = color
        center_x, center_y = group_centers[name]

        # Calculate positions in a circular pattern around group center
        num_neurons = len(group)
        for i in range(num_neurons):
            node_id = f"{name}_{i}"
            G.add_node(node_id)

            if name in ['input', 'output']:
                # Create a small circular layout around the group center
                radius = 0.1
                angle = 2 * np.pi * i / num_neurons
                pos[node_id] = (
                    center_x + radius * np.cos(angle),
                    center_y + radius * np.sin(angle)
                )
            else:
                scale = 0.05 * np.sqrt(num_neurons)
                x = np.random.uniform(-scale, scale)
                y = np.random.uniform(-scale, scale)
                pos[node_id] = (center_x + x, center_y + y)

            node_colors.append(color)

        offset += len(group)

    # Add edges for each synapse group
    edge_colors = []
    for name, synapse in synapses.items():
        pre_group = name.split('->')[0]
        post_group = name.split('->')[1]

        # Get the synapse indices
        i, j = synapse.i[:], synapse.j[:]

        # Add edges
        for pre, post in zip(i, j):
            pre_id = f"{pre_group}_{pre}"
            post_id = f"{post_group}_{post}"
            G.add_edge(pre_id, post_id)
            edge_colors.append(color_map[pre_group])

    # Create the plot
    plt.figure(figsize=figsize, dpi=100)

    # Draw the network
    nx.draw(G, pos,
            node_color=node_colors,
            node_size=50,
            edge_color=edge_colors,
            arrows=True,
            arrowsize=10,
            width=0.5,
            alpha=0.6)  # Slightly transparent edges for better visibility

    # Add group labels at the center of each group
    for name, (x, y) in group_centers.items():
        if name == 'hidden':
            name = 'excitatory'
        plt.text(x, y, name,
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontweight='bold',
                 fontsize=12,
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # Add legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                                  markerfacecolor=color, label=name, markersize=10)
                       for name, color in color_map.items()]
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

    plt.axis('off')

    return plt.gca()


# neuron_groups = {
#     'input': input_neurons,
#     'hidden': neurons,
#     'inhibitory': inhibitory_neurons,
#     'output': output_neurons
# }
#
# synapses = {
#     'input->hidden': input_synapse,
#     'hidden->hidden': main_synapse,
#     'hidden->inhibitory': to_inhib_synapse,
#     'inhibitory->hidden': inhib_synapse,
#     'hidden->output': output_synapse
# }
#
# visualize_network_connectivity(neuron_groups, synapses)
# plt.savefig('network_connectivity.png')
# plt.show()
# exit()
