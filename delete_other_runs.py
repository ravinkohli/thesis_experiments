import os
import shutil


# failed_jobs = 0
folders = ['autopytorch_thesis']
for folder in folders:
    for root, dirs, files in os.walk(f'/work/ws/nemo/fr_rk250-{folder}-0/'):
        for directory in dirs:
            if 'tmp' == directory and 'posthoc_ensemble_fit_False' in root:
                tmp_dir = os.path.join(root, directory)
                out_dir = os.path.join(tmp_dir, '../out')
                if not os.path.exists(os.path.join(tmp_dir, '../final_result.json')):
                    internal_directory = os.path.join(tmp_dir, '.autoPyTorch')
                    # if any(['ensemble_identifiers_1' in file for file in os.listdir(internal_directory)]):
                    #     ensemble_identifiers = pickle.load(open(os.path.join(internal_directory, 'ensemble_identifiers_0.pkl'), 'rb'))
                    #     print(f"Deleting runs from {internal_directory} which are not {ensemble_identifiers}")
                    #     ensemble_run_folders = ['/'.join(identifier.split('/')[:-1]) for identifier in ensemble_identifiers]
                    runs_directory = os.path.join(internal_directory, 'runs')
                    ensemble_directory = os.path.join(internal_directory, 'ensembles')
                    if os.path.exists(runs_directory):
                        shutil.rmtree(os.path.join(runs_directory))
                    if os.path.exists(ensemble_directory):
                        shutil.rmtree(os.path.join(ensemble_directory))
                    if os.path.exists(out_dir):
                        shutil.rmtree(os.path.join(out_dir))
                    # shutil.make_archive(os.path.join(os.path.dirname(tmp_dir), 'tmp'), 'zip', tmp_dir)
                    shutil.rmtree(tmp_dir)
