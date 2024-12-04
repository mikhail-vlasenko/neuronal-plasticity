from io import StringIO

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns

exp_data = """cell_type,firing_rate
EXC_L23,0.27
EXC_L4,1.06
EXC_L5,2.22
EXC_L6,0.93
PV_L23,3.10
PV_L4,3.89
PV_L5,4.58
PV_L6,4.61
SST_L23,3.63
SST_L4,1.89
SST_L5,3.78
SST_L6,6.30
VIP_L23,7.97
VIP_L4,0.85
VIP_L5,6.50
VIP_L6,2.90"""

model_data = """Population,firing_rate
L1VIP,0.90
L23E,0.30
L23PV,3.00
L23SST,3.41
L23VIP,7.62
L4E,1.11
L4PV,3.89
L4SST,1.61
L4VIP,0.75
L5E,2.14
L5PV,4.14
L5SST,3.82
L5VIP,5.91
L6E,0.94
L6PV,4.41
L6SST,6.44
L6VIP,3.33"""

def process_model_data(_df_model):
    _df_model['layer'] = _df_model['Population'].str.extract(r'L(\d+)')[0]
    _df_model['type'] = _df_model['Population'].str.extract(r'L\d+(.*)')[0]
    _df_model['type'] = _df_model['type'].replace('E', 'EXC')
    _df_model['source'] = 'Model'
    return _df_model

def additional_processing(_result_df):
    _result_df['layer'] = _result_df['layer'].replace('23', '2/3')
    _result_df.sort_values(by=['layer', 'type'], inplace=True, ignore_index=True)
    _result_df['full_type'] = _result_df['type'] + '@' + _result_df['layer']
    return _result_df

df_exp = pd.read_csv(StringIO(exp_data))
df_model = pd.read_csv(StringIO(model_data))

df_exp['layer'] = df_exp['cell_type'].str.extract(r'L(\d+)')[0]
df_exp['type'] = df_exp['cell_type'].str.extract(r'(.*)_L')[0]
df_exp['source'] = 'Experiment'

df_model = process_model_data(df_model)
result_df = pd.concat([df_exp, df_model], ignore_index=True)
result_df = additional_processing(result_df)

# Define colors for each cell type
colors = {
    'EXC': '#fb6a4a',  # Red
    'PV':  '#4292c6',  # Blue
    'SST': '#74c476',  # Green
    'VIP': '#fdae6b'   # Orange
}


def plot_firing_rate_comparison():
    plt.figure(figsize=(10, 6), dpi=150)
    g = sns.barplot(data=result_df,
                    x='full_type',
                    y='firing_rate',
                    hue='source',
                    alpha=0.7)

    # Update the colors based on cell type
    for i in range(2):
        for j, bar in enumerate(g.containers[i]):
            idx = j*2 + i
            cell_type = result_df['type'].iloc[idx]
            bar.set_color(colors[cell_type])
            # Make model bars slightly darker
            if result_df['source'].iloc[idx] == 'Model':
                bar.set_alpha(1.0)
            else:  # Experimental bars
                bar.set_alpha(0.5)
                bar.set_hatch('//')


    # Create custom legend handles
    legend_elements = []

    # Add source type elements
    legend_elements.append(Patch(facecolor='gray', alpha=0.5, hatch='//', label='Experiment'))
    legend_elements.append(Patch(facecolor='gray', alpha=1.0, label='Model'))

    # Add cell type elements
    for cell_type, color in colors.items():
        legend_elements.append(Patch(facecolor=color, label=cell_type))

    # Remove the automatic legend
    plt.gca().get_legend().remove()

    # Add custom legend
    plt.legend(handles=legend_elements,
              title='Source and Cell Type',
              loc='upper left',
              frameon=True)

    plt.title('Firing Rates Comparison: Experiment vs Model')
    plt.xlabel('Cell Type and Layer')
    plt.xticks(rotation=45, ha='center')
    plt.ylabel('Firing Rate (Spikes/s)')

    plt.tight_layout()
    plt.savefig('firing_rate_comparison.png')
    plt.show()


plot_firing_rate_comparison()


df = pd.read_csv("experiments/run_20241204_215222_None/metrics/firing_stats.csv")

df = process_model_data(df)
df = additional_processing(df)

def rate_distribution_plot():
    plt.figure(figsize=(10, 6), dpi=150)
    g = sns.boxplot(data=df, x='full_type', y='firing_rate')

    for i, box in enumerate(g.containers[0].boxes):
        cell_type = df_model['type'].iloc[i]
        box.set_color(colors[cell_type])

    legend_elements = []
    for cell_type, color in colors.items():
        legend_elements.append(Patch(facecolor=color, label=cell_type))

    plt.legend(handles=legend_elements,
              title='Cell Type',
              loc='upper left',
              frameon=True)

    plt.title('Firing Rates Distribution: Model')
    plt.xlabel('Cell Type and Layer')
    plt.xticks(rotation=45, ha='center')
    plt.ylabel('Firing Rate (Spikes/s)')

    plt.tight_layout()

    plt.savefig('firing_rate_distribution.png')
    plt.show()

rate_distribution_plot()
