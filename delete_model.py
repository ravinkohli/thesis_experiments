import os
import shutil


# failed_jobs = 0
folders = ['autopytorch_thesis']
for folder in folders:
    for root, dirs, files in os.walk(f'/work/ws/nemo/fr_rk250-{folder}-0/'):
        for directory in dirs:
            if 'tmp' == directory:
                tmp_dir = os.path.join(root, directory)
                if not os.path.exists(os.path.join(tmp_dir, '../final_result.json')):
                    internal_directory = os.path.join(tmp_dir, '.autoPyTorch')
                    runs_directory = os.path.join(internal_directory, 'runs')
                    model_file_path = None
                    for folder in os.listdir(runs_directory):
                        run_directory = os.path.join(runs_directory, folder)
                        paths = []
                        for file in os.listdir(run_directory):
                            if '.model' in file:
                                model_file_path = os.path.join(run_directory, file)
                                print(model_file_path)
                                os.remove(model_file_path)
                    
