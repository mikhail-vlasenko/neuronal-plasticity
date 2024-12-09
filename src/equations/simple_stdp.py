from brian2 import ms, mV

## Neurons
taum = 10*ms
Ee = 0*mV    # reversal potential
vt = -54*mV  # threshold potential
vr = -60*mV  # reset potential
El = -70*mV  # resting potential
OEl = -74*mV  # resting potential for output neurons
taue = 5*ms
tauadapt = 50*ms
v_adaptation = 0*mV
output_neuron_rate_growth = 0.

## Noise
noise_sigma = 1*mV

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
tauc = 50*ms  # very slow decay of eligibility trace
taud = 25*ms
taus = 1*ms  # this is lr, but prob better to increase eligibility trace for faster learning
epsilon_dopa = 1e-2

expected_reward_change_rate = 0.25

NEURON_MODEL = '''
dv/dt = (ge * (Ee-v) + El - v) / taum + noise_sigma*sqrt(2/taum)*xi : volt (unless refractory)
dge/dt = -ge / taue : 1
'''

NEURON_PARAMS = {
    'model': NEURON_MODEL,
    'threshold': 'v>vt',
    'reset': 'v = vr',
    'refractory': '2*ms',
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
        s = clip(s, 0, max_strength)
        ge += s
        Apre += dApre
        c = clip(c + Apost, -gmax, gmax)
    ''',
    'on_post': '''
        Apost += dApost
        c = clip(c + Apre, -gmax, gmax)
    ''',
    'method': 'euler',
    # 'delay': 1*ms
}

OUTPUT_NEURON_MODEL = '''
dv/dt = (ge * (Ee-v) + OEl - v + rate * volt - adaptation) / taum : volt (unless refractory)
dge/dt = -ge / taue : 1
dadaptation/dt = -adaptation / tauadapt : volt
expected_reward : 1
drate/dt = output_neuron_rate_growth/second : 1  # Grows linearly with time with slope 1/second 
'''

OUTPUT_NEURON_PARAMS = {
    'model': OUTPUT_NEURON_MODEL,
    'threshold': 'v > vt',
    'reset': '''
        expected_reward += expected_reward_change_rate * (reward_value - expected_reward)
        adaptation += v_adaptation
        v = OEl
        rate = 0
        ''',  # Reset both v and rate
    'refractory': '5*ms',
    'method': 'euler'
}

# DOPAMINE_NEURON_PARAMS = {
#     'model': 'dv/dt = (vr-v)/taum : volt',
#     'threshold': 'v>(vr+1*mV)',
#     'reset': 'v = vr',
#     'refractory': '5*ms',
#     'method': 'exact'
# }

