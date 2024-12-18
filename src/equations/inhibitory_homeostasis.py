learning_rate = 0.05
exc_to_inhib_ratio = 1  # firing ratio that balances out the strength update
amplitude = 1
inhib_s_initial = -1
baseline_inhib_s = inhib_s_initial

use_linear_model = False
linear_change = 0.05
linear_min = -3


inhibitory_synapse_model = '''
s : 1
'''

# on pre, we should decrease inhibition (make it larger, less negative),
# as that will increase the amount of times on post is called, and achieve e-i balance
inhibitory_on_pre = '''
s = clip(s, -10, 0)
ge_post += s
s += exp(-(s - baseline_inhib_s)/amplitude)*learning_rate
'''
if use_linear_model:
    inhibitory_on_pre = '''
        s = clip(s, linear_min, 0)
        ge_post += s
        s += linear_change
    '''

# on post, we should increase inhibition, as it means the excitatory (post) neuron is firing too much
inhibitory_on_post = '''
s -= exp((s - baseline_inhib_s)/amplitude)*learning_rate/exc_to_inhib_ratio
'''
if use_linear_model:
    inhibitory_on_post = '''
        s -= linear_change
    '''

INHIBITORY_SYNAPSE_PARAMS = {
    'model': inhibitory_synapse_model,
    'on_pre': inhibitory_on_pre,
    'on_post': inhibitory_on_post,
    'method': 'euler'
}
