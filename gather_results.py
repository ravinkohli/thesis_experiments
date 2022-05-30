import pandas as pd
import os
import json

file_data = dict()
for root, dirs, files in os.walk('/work/ws/nemo/fr_rk250-autopytorch_thesis-0/runs/'):
    for file in files:
        if 'final_result.json' in file:
            task = [file_name for file_name in root.split('/')][-1]
            task_id = task.split('_')[0]
            if task_id not in file_data.keys():
                file_data[task_id] = dict()
            content = pd.read_json(os.path.join(root, file), typ='series')
            content.drop(['train balanced accuracy', 'duration'])
            experiment_name = task.replace(f"{task_id}_1_", '')
            file_data[task_id][experiment_name] = float("{:.4f}".format(content['test balanced accuracy']))
            # del content["task_id"]

pd.DataFrame(file_data).transpose().to_csv('results/gathered_results_proper.csv')

