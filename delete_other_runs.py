import os
import shutil


folders = ['autopytorch_thesis']
for folder in folders:
    for root, dirs, files in os.walk(f'/work/ws/nemo/fr_rk250-{folder}-0/'):
        for directory in dirs:
            if 'tmp' == directory:
                tmp_dir = os.path.join(root, directory)
                out_dir = os.path.join(tmp_dir, '../out')
                internal_directory = os.path.join(tmp_dir, '.autoPyTorch')
                runs_directory = os.path.join(internal_directory, 'runs')
                ensemble_directory = os.path.join(internal_directory, 'ensembles')
                if os.path.exists(runs_directory):
                    shutil.rmtree(os.path.join(runs_directory))
                if os.path.exists(ensemble_directory):
                    shutil.rmtree(os.path.join(ensemble_directory))
                if os.path.exists(out_dir):
                    shutil.rmtree(os.path.join(out_dir))
                shutil.make_archive(os.path.join(os.path.dirname(tmp_dir), 'tmp'), 'zip', tmp_dir)
                shutil.rmtree(tmp_dir)

