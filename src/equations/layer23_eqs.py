import numpy as np
from brian2 import Equations, mV, ms

from Original_model.network_parameters import net_dict as ORIGINAL_NET_DICT, neuron_dict as ORIGINAL_NEURON_DICT

POPULATIONS = ['L23E', 'L23PV', 'L23SST', 'L23VIP']  # indices 1, 2, 3, 4 from the original model

N_tot = 5000 # Total number of neurons if the model would be for the full column
N_23 = 0.291088453*N_tot # Number of neurons in layer 23
proportion_exc = 0.85 # Proportion of excitatory neurons in each layer
proportion_inh = 0.15 # Proportion of inhibitory neurons in each layer
L_23_exc = int(proportion_exc*N_23) # Number of excitatory neurons in layer 23
L_23_pv = int(0.295918*proportion_inh*N_23) # Number of PV neurons in layer 23
L_23_sst = int(0.214286*proportion_inh*N_23) # Number of SST neurons in layer 23
L_23_vip = int(0.489796*proportion_inh*N_23) # Number of VIP neurons in layer 23


NET_DICT = ORIGINAL_NET_DICT
# remove unnecessary populations
for key, value in NET_DICT.items():
    if isinstance(value, list):
        assert len(value) == 17
        NET_DICT[key] = value[1:5]  # slice to get only the values for the 4 considered populations
    elif isinstance(value, np.ndarray):
        if value.shape == ():
            continue
        if value.shape == (17,):
            NET_DICT[key] = value[1:5]
        elif value.shape == (17, 17):
            NET_DICT[key] = value[1:5, 1:5]
        else:
            raise ValueError(f"Unexpected shape of {key}: {value.shape}")

NET_DICT['num_neurons'] = np.array([L_23_exc, L_23_pv, L_23_sst, L_23_vip])
NET_DICT['global_g'] = 200.


NEURON_DICT = ORIGINAL_NEURON_DICT
for key, value in NEURON_DICT.items():
    NEURON_DICT[key] = value[1:5]  # slice to get only the values for the 4 considered populations

V_E = 0.
tau_ampa = 2.
g_ampa_ext = 1.
g_ampa_rec = 1.

receptors_V_I = [-80.97, -82.35, -69.16, -67.94]*mV
tau_gaba = 5.
g_gaba = 1.


ampa_components = [f's_ampa_tot_{i}' for i in range(5)]
_ampa_inits = '\n'.join([f'{comp} : 1' for comp in ampa_components])
NEURON_MODEL = Equations(f'''
        dv/dt = (-g_L*(v - V_L) - I_syn)/C_m: volt (unless refractory)
        I_syn = I_DC_input + I_ampa_ext + I_ampa_rec + I_gaba : amp

        V_L : volt
        g_L : siemens
        C_m : farad
        v_th : volt
        v_reset : volt
        I_DC_input: amp

        I_ampa_ext = {g_ampa_ext}*nS*(v - {V_E}*mV)*s_ampa_ext : amp
        ds_ampa_ext/dt = -s_ampa_ext/({tau_ampa}*ms) : 1

        I_ampa_rec = {g_ampa_rec}*nS*(v - {V_E}*mV)*s_ampa_tot : amp
        s_ampa_tot = {' + '.join(ampa_components)} : 1
        {_ampa_inits}

        I_gaba = {g_gaba}*nS*(v - V_I)*s_gaba_tot : amp
        V_I : volt
        s_gaba_tot = s_gaba_tot_l23pv + s_gaba_tot_l23sst + s_gaba_tot_l23vip : 1
        s_gaba_tot_l23pv : 1
        s_gaba_tot_l23sst : 1
        s_gaba_tot_l23vip : 1

        ''')


taupre = 20*ms
taupost = taupre
gmax = 0.5
max_strength = 10000  # todo: lower
dApre = 0.1  # this is basically by how much the eligibility trace increases
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax

## Dopamine signaling
tauc = 250*ms
taud = 10*ms
taus = 1*ms  # this is lr, but prob better to increase eligibility trace for faster learning
epsilon_dopa = 1e-2

expected_reward_change_rate = 0.25

_ampa_counter = 0
def get_ampa_model():
    global _ampa_counter
    eq = Equations(f'''
        s_ampa_tot_{_ampa_counter}_post = w*s_ampa : 1 (summed)  
        ds_ampa/dt = - s_ampa/({tau_ampa}*ms) : 1 (clock-driven)
        
        dc/dt = -c / tauc : 1 (clock-driven)
        dd/dt = -d / taud : 1 (clock-driven)
        dw/dt = c * d / taus : 1 (clock-driven)
        dApre/dt = -Apre / taupre : 1 (event-driven)
        dApost/dt = -Apost / taupost : 1 (event-driven)
    ''')
    _ampa_counter += 1
    return eq

ampa_on_pre = '''
    w = clip(w, 0, max_strength)
    s_ampa += 1
    Apre += dApre
    c = clip(c + Apost, -gmax, gmax)
'''

ampa_on_post = '''
    Apost += dApost
    c = clip(c + Apre, -gmax, gmax)
'''

AMPA_PARAMS = {
    'on_pre': ampa_on_pre,
    'on_post': ampa_on_post,
    'method': 'euler',
    'delay': NET_DICT['delay']
}


_inhib_synapse_shared = f'''
    ds_gaba/dt = - s_gaba/({tau_gaba}*ms) : 1 (clock-driven)
    w : 1
'''

PV_MODEL = f'''
    s_gaba_tot_l23pv_post = w*s_gaba : 1 (summed)  
''' + _inhib_synapse_shared

SST_MODEL = f'''
    s_gaba_tot_l23sst_post = w*s_gaba : 1 (summed)  
''' + _inhib_synapse_shared

VIP_MODEL = f'''
    s_gaba_tot_l23vip_post = w*s_gaba : 1 (summed)  
''' + _inhib_synapse_shared

gaba_on_pre = '''
    s_gaba += 1
'''

gaba_on_post = ''
# todo: add homeostasis
