export PYTHONPATH="${PYTHONPATH}:/home/mvlasenko/neuronal-plasticity"
export OPTUNA_DISTRIBUTED=true
cd /home/mvlasenko/neuronal-plasticity/src
python3 hyper_search.py
