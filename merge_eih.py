import pickle
import os


folder_prefix = 'final_thesis_results/ensemble_size_5_old/'
outfolder_prefix = 'final_thesis_results/ensemble_size_5'
rerun_data = pickle.load(open(os.path.join(folder_prefix, 'task_id_to_performance_eih_rerun_fixed.pkl'), 'rb'))
data = pickle.load(open(os.path.join(folder_prefix, 'task_id_to_performance_eih_fixed.pkl'), 'rb'))

data.update(rerun_data)

pickle.dump(data, open(os.path.join(outfolder_prefix, 'task_id_to_performance_eih.pkl'), 'wb'))