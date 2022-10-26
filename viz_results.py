import glob
import os
import pickle
from typing import Dict, NamedTuple
from autoPyTorch.utils.results_visualizer import PlotSettingParams
from autoPyTorch.utils.results_visualizer import ResultsVisualizer
from autoPyTorch import metrics
from autoPyTorch.utils.results_manager import MetricResults
from autoPyTorch.utils.results_visualizer import ColorLabelSettings
import pandas as pd
import zipfile
import tempfile
import json

class StoreResults(NamedTuple):
    results: MetricResults
    colors: Dict
    labels: Dict
    plot_setting_params: PlotSettingParams

# def store_contents(task_id_to_performance, estimator_file, root, experiment_name):

folders = ['autopytorch_thesis']
task_id_to_performance = {}
task_ids = [10101, 3, 168335, 14965, 146195, 31, 9981, 7592]
for folder in folders:
    for root, dirs, files in os.walk(f'/work/ws/nemo/fr_rk250-{folder}-0/small_tasks/'):
        for file in files:
            if 'final_result.json' in file and 'ensemble_size_5' in root:
                estimator_file = os.path.join(root, 'estimator.pickle')
                content = pd.read_json(os.path.join(root, file), typ='series')
                incumbent_run_history = None
                task_id = content['task_id']
                seed = content['seed']
                experiment_name = content['experiment_name']
                experiment_name = ''.join([k[0] for k in experiment_name.split('_')])
                for option in ['enable_traditional_pipeline', 'warmstart', 'posthoc_ensemble_fit', 'use_ensemble_opt_loss']:
                    experiment_name +=  f"_{''.join([k[0] for k in option.split('_')])}_{str(content[option])[0]}"
                if experiment_name not in task_id_to_performance:
                    task_id_to_performance[experiment_name] = {}
                if task_id not in task_id_to_performance[experiment_name]:
                    task_id_to_performance[experiment_name][task_id] = {}
                if seed not in task_id_to_performance[experiment_name][task_id]:
                    task_id_to_performance[experiment_name][task_id][seed] = {}

                duration = content['duration']
                task_id_to_performance[experiment_name][task_id][seed]['duration'] = duration
            
import pickle
with open('./task_id_to_duration.pkl', 'wb') as fp:
    pickle.dump(task_id_to_performance, fp)



# ebo_pef_T_etp_F_ueol_F_w_F_nsl_1,
# ebo_pef_T_etp_T_ueol_F_w_F_nsl_1,
# ebo_pef_F_etp_F_ueol_F_w_F_nsl_1,
ebor_pef_T_etp_T_ueol_F_w_F_nsl_2,
ebos_pef_T_etp_T_ueol_F_w_F_nsl_2,
# es_pef_F_etp_F_ueol_F_w_F_nsl_1,
# es_pef_F_etp_T_ueol_F_w_F_nsl_1,
# eih_pef_T_etp_F_ueol_F_w_F_nsl_1,
# eih_pef_T_etp_T_ueol_F_w_F_nsl_1,
# eih_pef_T_etp_F_ueol_F_w_T_nsl_1,
# eih_pef_T_etp_T_ueol_F_w_T_nsl_1,
# eih_pef_F_etp_F_ueol_F_w_T_nsl_1,
# eih_pef_F_etp_T_ueol_F_w_T_nsl_1,
# eih_pef_F_etp_F_ueol_F_w_F_nsl_1,
# ebo_pef_F_etp_F_ueol_T_w_F_nsl_1,
# ebo_pef_T_etp_F_ueol_T_w_F_nsl_1,
# ebo_pef_T_etp_T_ueol_T_w_F_nsl_1,
# ebor_pef_T_etp_F_ueol_T_w_F_nsl_2,
# ebos_pef_T_etp_F_ueol_T_w_F_nsl_2,
# ebor_pef_T_etp_T_ueol_T_w_F_nsl_2,
# ebos_pef_T_etp_T_ueol_T_w_F_nsl_2,
sespl_pef_F_etp_F_ueol_F_w_F_nsl_2,
esr_pef_F_etp_F_ueol_F_w_F_nsl_2,
sespl_pef_F_etp_T_ueol_F_w_F_nsl_2,
esr_pef_F_etp_T_ueol_F_w_F_nsl_2,
eihr_pef_T_etp_F_ueol_F_w_T_nsl_2,
eihs_pef_T_etp_F_ueol_F_w_T_nsl_2,
eihs_pef_T_etp_T_ueol_F_w_T_nsl_2,
eihr_pef_T_etp_T_ueol_F_w_T_nsl_2,
# eihr_pef_T_etp_F_ueol_F_w_F_nsl_2,
# eihs_pef_T_etp_F_ueol_F_w_F_nsl_2,
# sft_pef_T_etp_F_ueol_F_w_F_nsl_2,
# eihr_pef_T_etp_T_ueol_F_w_F_nsl_2,
# sft_pef_T_etp_T_ueol_F_w_F_nsl_2,
# eihs_pef_T_etp_T_ueol_F_w_F_nsl_2,
# sft_pef_F_etp_F_ueol_F_w_F_nsl_2,
eihr_pef_F_etp_F_ueol_F_w_T_nsl_2,
eihs_pef_F_etp_F_ueol_F_w_T_nsl_2,
# sa_pef_F_etp_F_ueol_F_w_F_nsl_2