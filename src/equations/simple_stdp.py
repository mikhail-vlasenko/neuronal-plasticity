from brian2 import ms, mV

## Neurons
taum = 10*ms
Ee = 0*mV    # reversal potential
vt = -54*mV  # threshold potential
vr = -60*mV  # reset potential
El = -74*mV  # resting potential
taue = 5*ms

## STDP
taupre = 20*ms
taupost = taupre
gmax = 1
max_strength = 1
dApre = 0.1  # this is basically by how much the eligibility trace increases
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax

## Dopamine signaling
tauc = 1000*ms  # very slow decay of eligibility trace
taud = 200*ms
taus = 1*ms  # this is lr, but prob better to increase eligibility trace for faster learning
epsilon_dopa = 5e-3

NEURON_MODEL = '''
dv/dt = (ge * (Ee-v) + El - v) / taum : volt
dge/dt = -ge / taue : 1
'''

NEURON_PARAMS = {
    'model': NEURON_MODEL,
    'threshold': 'v>vt',
    'reset': 'v = vr',
    'refractory': '5*ms',
    'method': 'euler'
}

SYNAPSE_MODEL = '''
dc/dt = -c / tauc : 1 (clock-driven)
dd/dt = -d / taud : 1 (clock-driven)
ds/dt = c * d / taus : 1 (clock-driven)
dApre/dt = -Apre / taupre : 1 (event-driven)
dApost/dt = -Apost / taupost : 1 (event-driven)
'''

SYNAPSE_PARAMS = {
    'model': SYNAPSE_MODEL,
    'on_pre': '''
        s = clip(s, -max_strength, max_strength)
        ge += s
        Apre += dApre
        c = clip(c + Apost, -gmax, gmax)
    ''',
    'on_post': '''
        Apost += dApost
        c = clip(c + Apre, -gmax, gmax)
    ''',
    'method': 'euler'
}


OUTPUT_NEURON_MODEL = '''
dv/dt = (ge * (Ee-v) + El - v + rate*taum) / taum : volt
dge/dt = -ge / taue : 1
rate : volt/second  # Growth rate - will be reset after each spike
'''

OUTPUT_NEURON_PARAMS = {
    'model': NEURON_MODEL,
    'threshold': 'v > vt',
    'reset': '''
        v = vr
        rate = 0
        ''',  # Reset both v and rate
    'refractory': '20*ms',
    'method': 'euler'
}

# DOPAMINE_NEURON_PARAMS = {
#     'model': 'dv/dt = (vr-v)/taum : volt',
#     'threshold': 'v>(vr+1*mV)',
#     'reset': 'v = vr',
#     'refractory': '5*ms',
#     'method': 'exact'
# }

