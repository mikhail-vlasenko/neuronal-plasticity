learning_rate = 0.05
exc_to_inhib_ratio = 1  # firing ratio that balances out the strength update
amplitude = 2
inhib_s_initial = -1
baseline_inhib_s = inhib_s_initial


inhibitory_synapse_model = '''
s : 1
'''

inhibitory_on_pre = '''
s = clip(s, -10, 0)
ge_post += s
s += exp(-(s - baseline_inhib_s)/amplitude)*learning_rate
'''

inhibitory_on_post = '''
s -= exp((s - baseline_inhib_s)/amplitude)*learning_rate/exc_to_inhib_ratio
'''

INHIBITORY_SYNAPSE_PARAMS = {
    'model': inhibitory_synapse_model,
    'on_pre': inhibitory_on_pre,
    'on_post': inhibitory_on_post,
    'method': 'euler'
}
