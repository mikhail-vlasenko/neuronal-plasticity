import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def visualize_network_connectivity(neuron_groups, synapses, figsize=(12, 12)):
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

    if len(neuron_groups) == 4:
        colors = ['blue', 'green', 'orange', 'red']

        group_centers = {
            'input': (0, 1),
            'hidden': (0, 0.5),
            'inhibitory': (0.5, 0.5),
            'output': (0, 0)
        }
        color_map = {}

    elif len(neuron_groups) == 6:
        colors = ['blue', 'green', 'orange', 'peru', 'yellow', 'red']
        # labels = ['Input', 'Excitatory', 'PV', 'SST', 'VIP', 'Output']

        group_centers = {
            'Input': (0, 2),
            'Excitatory': (-0.25, 1),
            'PV': (1.25, 0.5),
            'SST': (1.5, 1),
            'VIP': (1.25, 1.5),
            'Output': (0, 0)
        }
        color_map = {
            'Input': 'blue',
            'Excitatory': 'green',
            'PV': 'orange',
            'SST': 'peru',
            'VIP': 'yellow',
            'Output': 'red'
        }
    else:
        raise ValueError("The number of neuron groups should be 4 or 6.")

    scale = 0.5
    for name, (x, y) in group_centers.items():
        group_centers[name] = (x * scale, y * scale)
    # Initialize position dictionaries and colors
    pos = {}
    node_colors = []

    # Add nodes for each neuron group with positions relative to group centers
    offset = 0
    for idx, (name, group) in enumerate(neuron_groups.items()):
        color = colors[idx % len(colors)]
        center_x, center_y = group_centers[name]

        # Calculate positions in a circular pattern around group center
        num_neurons = len(group)
        for i in range(num_neurons):
            node_id = f"{name}_{i}"
            G.add_node(node_id)

            if name in ['Input', 'Output']:
                # Create a small circular layout around the group center
                radius = 0.1
                angle = 2 * np.pi * i / num_neurons
                pos[node_id] = (
                    center_x + radius * np.cos(angle),
                    center_y + radius * np.sin(angle)
                )
            else:
                scale = 0.03 * np.sqrt(num_neurons)
                x = np.random.uniform(-scale, scale)
                y = np.random.uniform(-scale, scale)
                pos[node_id] = (center_x + x, center_y + y)

            node_colors.append(color)

        offset += len(group)

    # Add edges for each synapse group
    for name, synapse in synapses.items():
        pre_group, post_group = name.split('_')

        # Get the synapse indices
        i, j = synapse.i[:], synapse.j[:]

        # Add edges
        for pre, post in zip(i, j):
            pre_id = f"{pre_group}_{pre}"
            post_id = f"{post_group}_{post}"
            G.add_edge(pre_id, post_id, color=color_map[pre_group])

    # Create the plot
    plt.figure(figsize=figsize, dpi=200)

    edges = G.edges()
    edge_colors = [G[u][v]['color'] for u, v in edges]

    # Draw the network
    nx.draw(G, pos,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=50,
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

    # neuron_groups = {
    #     'Input': simulation.input_neurons,
    #     'Excitatory': simulation.pops[0],
    #     'PV': simulation.pops[1],
    #     'SST': simulation.pops[2],
    #     'VIP': simulation.pops[3],
    #     'Output': simulation.output_neurons
    # }
    #
    # synapses = {}
    # for synapse in simulation.synapses:
    #     synapses[f"{synapse.name}"] = synapse
    #
    # visualize_network_connectivity(neuron_groups, synapses)
    # plt.savefig('network_connectivity.png')
    # plt.show()
    # exit()
