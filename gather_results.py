import pandas as pd
import os
import json

file_data = list()
folders = ['autopytorch_thesis']
for folder in folders:
    for root, dirs, files in os.walk(f'/work/ws/nemo/fr_rk250-{folder}-0/small_tasks/'):
        for file in files:
            if 'final_result.json' in file:
                content = pd.read_json(os.path.join(root, file), typ='series')
                file_data.append(content)

pd.DataFrame(file_data).to_csv('gathered_results_proper.csv')