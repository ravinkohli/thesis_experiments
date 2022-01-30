import pandas as pd
import os
import json

file_data = dict()
for root, dirs, files in os.walk('/work/ws/nemo/fr_rk250-autopytorch_icml-0/results'):
    for file in files:
        if 'final_result.json' in file:
            task = [file_name for file_name in root.split('/')][-1]
            content = json.load(open(os.path.join(root, file)))
            del content["task_id"]
            file_data[task] = content

data = pd.DataFrame(file_data).T
data.to_csv("./gathered_results.csv")