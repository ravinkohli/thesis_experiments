import enum
import pickle
from smac.tae import StatusType

from experiment_utils import replace_key


data = pickle.load(open('final_thesis_results/ensemble_size_5/task_id_to_performance_eih_rerun.pkl', 'rb'))
results = pickle.load(open('final_thesis_results/ensemble_size_5/task_id_to_performance_size_5.pkl', 'rb'))

new_results = {}
for strategy in results:
    new_results[replace_key(strategy)] = results[strategy]
del results
def here_replace_key(key):

    if 'es' in key:
        if 'sespl' in key or 'esr' in key:
            key = f"{key}_nsl_2"
        else:
            key = f"{key}_nsl_1"
    else:
        if 's' in key or 'r' in key:
            key = f"{key}_nsl_2"
        else:
            key = f"{key}_nsl_1"
    return key

new_data = {}
for strategy in data:
    new_data[here_replace_key(strategy)] = data[strategy]
data = new_data

new_data = {}

for strategy in data:
    if strategy not in new_data:
        new_data[strategy] = {}
        for task in data[strategy]:
            if task not in new_data[strategy]:
                new_data[strategy][task] = {}
                for seed in data[strategy][task]:
                    if seed not in new_data[strategy][task]:
                        new_data[strategy][task][seed] = {}
                    incumbent_performances = sorted(list(data[strategy][task][seed]['incumbent_run_history'].values()), key=lambda x: x.endtime)
                    ensemble_history_points = {}
                    ensemble_history_points['train'] = list(new_results[strategy][task][seed]['ensemble_history']['train_balanced_accuracy'].values())
                    ensemble_history_points['test'] = list(new_results[strategy][task][seed]['ensemble_history']['test_balanced_accuracy'].values())
                    ensemble_history_points['time'] = list(new_results[strategy][task][seed]['ensemble_history']['Timestamp'].values())
                    ensemble_history = {}
                    ensemble_history['train_balanced_accuracy'] = {}
                    ensemble_history['test_balanced_accuracy'] = {}
                    ensemble_history['Timestamp'] = {}

                    j = 0 # ensemble history points pointer
                    i = 0 # new ensemble history pointer

                    for performance in incumbent_performances:
                        if performance.status == StatusType.SUCCESS:
                            if performance.endtime > ensemble_history_points['time'][j]:
                                ensemble_history['train_balanced_accuracy'][i] = ensemble_history_points['train']
                                ensemble_history['Timestamp'][i] = ensemble_history_points['time']
                                ensemble_history['test_balanced_accuracy'][i] = ensemble_history_points['test']
                                i += 1
                                j += 1
                            else:
                                ensemble_history['train_balanced_accuracy'][i] = 1 - performance.cost
                                ensemble_history['Timestamp'][i] = performance.endtime * 1000
                                ensemble_history['test_balanced_accuracy'][i] = 1 - performance.additional_info['test_loss']['balanced_accuracy']
                                i += 1

                    new_data[strategy][task][seed]['ensemble_history'] = ensemble_history


pickle.dump(new_data, open('task_id_to_performance_eih_rerun_fixed.pkl', 'wb'))
