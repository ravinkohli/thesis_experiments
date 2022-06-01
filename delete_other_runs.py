import os
import pickle
import shutil

for root, dirs, files in os.walk('/work/ws/nemo/fr_rk250-autopytorch_thesis_final-0/small_tasks/'):
    for directory in dirs:
        if 'tmp' == directory and 'num_stacking_layers_2' in root:
            internal_directory = os.path.join(root, directory, '.autoPyTorch')
            if any(['ensemble_identifiers_1' in file for file in os.listdir(internal_directory)]):
                ensemble_identifiers = pickle.load(open(os.path.join(internal_directory, 'ensemble_identifiers_0.pkl'), 'rb'))
                print(f"Deleting runs from {internal_directory} which are not {ensemble_identifiers}")
                ensemble_run_folders = ['/'.join(identifier.split('/')[:-1]) for identifier in ensemble_identifiers]
                
                runs_directory = os.path.join(internal_directory, 'runs')
                for run in os.listdir(runs_directory):
                    run_folder = os.path.join(runs_directory, run)
                    print(run_folder)
                    if run_folder not in ensemble_run_folders:
                        print(f"Deleting {run_folder}")
                        shutil.rmtree(os.path.join(run_folder))