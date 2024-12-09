from brian2 import ms

learning_rate = 0.05
amplitude = 2
inhib_s_initial = -2


inhibitory_synapse_model = '''
s : 1
'''

inhibitory_on_pre = '''
s = clip(s, -10, 0)
ge += s
s += exp(-s/amplitude)*learning_rate
'''

inhibitory_on_post = '''
s -= exp(s/amplitude)*learning_rate
'''

INHIBITORY_SYNAPSE_PARAMS = {
    'model': inhibitory_synapse_model,
    'on_pre': inhibitory_on_pre,
    'on_post': inhibitory_on_post,
    'method': 'euler'
}
