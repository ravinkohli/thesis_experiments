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
                estimator_file = os.path.join(root, 'estimator.pkl')
                content = pd.read_json(os.path.join(root, file), typ='series')
                incumbent_run_history = None
                task_id = content['task_id']
                seed = content['seed']
                experiment_name = content['experiment_name']
                experiment_name = ''.join([k[0] for k in experiment_name.split('_')])
                for option in ['posthoc_ensemble_fit', 'enable_traditional_pipeline', 'use_ensemble_opt_loss', 'warmstart']:
                    experiment_name +=  f"_{''.join([k[0] for k in option.split('_')])}_{str(content[option])[0]}"
                if 'eih' in experiment_name:
                    try:
                        
                        if os.path.exists(estimator_file):
                            print(f"path found: {estimator_file}")
                            directory = root.split('/')[-1]
                            # plot_directory = f'./incumbent_plots/{directory}'
                            # os.makedirs(plot_directory, exist_ok=True)
                            
                            with open(estimator_file, 'rb') as f:
                                estimator = pickle.load(f)
                            # metric_name = 'balanced_accuracy'

                            # metric_results = MetricResults(
                            #     metric=getattr(metrics, metric_name),
                            #     run_history=estimator.run_history,
                            #     ensemble_performance_history=estimator.ensemble_performance_history,
                            # )
                            if experiment_name not in task_id_to_performance:
                                task_id_to_performance[experiment_name] = {}
                            if task_id not in task_id_to_performance[experiment_name]:
                                task_id_to_performance[experiment_name][task_id] = {}
                            if seed not in task_id_to_performance[experiment_name][task_id]:
                                task_id_to_performance[experiment_name][task_id][seed] = {}
                            incumbent_run_history = estimator.run_history
                            task_id_to_performance[experiment_name][task_id][seed]['incumbent_run_history'] = incumbent_run_history
                            with open('./task_id_to_performance_eih.pkl', 'wb') as fp:
                                pickle.dump(task_id_to_performance, fp)
                        else:
                            print(f"path not found: {estimator_file}")  
                    except:
                        continue
                    

with open('./task_id_to_performance_eih.pkl', 'wb') as fp:
    pickle.dump(task_id_to_performance, fp)
                        # colors, labels = ColorLabelSettings().extract_dicts(metric_results)
                        # store_plot_directory = os.path.join(plot_directory, f"{task_id}", f"{seed}")
                        # os.makedirs(store_plot_directory, exist_ok=True)
                        # params = PlotSettingParams(
                        #     xscale='log',
                        #     xlabel='Runtime (second)',
                        #     ylabel='Balanced Accuracy',
                        #     title=f'Incumbent trajectory over time task id-{task_id}',
                        #     figname=os.path.join(store_plot_directory, 'plot_over_time.png'),
                        #     savefig_kwargs={'bbox_inches': 'tight'},
                        #     show=False,  # If you would like to show, make it True and set figname=None
                        #     figsize=(40, 40),
                        #     legend_kwargs={'loc': 'upper left', 'fontsize': 'xx-small', 'bbox_to_anchor': (1,1)},
                        #     # locator_params={'x_nbins': 6, 'y_nbins': 10}
                        # )
                        # store_tuple = StoreResults(results=metric_results,
                        #     colors=colors, labels=labels,
                        #     plot_setting_params=params)
                        # pickle.dump(store_tuple, open(os.path.join(store_plot_directory, 'stored_tuple.pkl'), 'wb'))

                #     zip_file = os.path.join(root, 'tmp.zip')
                #     zf = zipfile.ZipFile(zip_file)
                #     with tempfile.TemporaryDirectory() as tempdir:
                #         zf.extractall(tempdir)
                #         ensemble_history = json.load(open(os.path.join(tempdir, '.autoPyTorch/ensemble_history.json'), 'r'))
                #         # ensemble_history_dict = {}
                #         # time_stamps = list(ensemble_history['Timestamp'].values())
                #         # ensemble_history_dict['Timestamp'] = time_stamps
                #         # ensemble_history_dict['test_balanced_accuracy'] = list(ensemble_history['test_balanced_accuracy'].values())
                #         task_id_to_performance[experiment_name][task_id][seed]['ensemble_history'] = ensemble_history
                        # task_id_to_performance[experiment_name][task_id][seed]['incumbent_run_history'] = incumbent_run_history
                # except:
                #     continue
                                

            
# import pickle
# with open('./task_id_to_performance_eih.pkl', 'wb') as fp:
#     pickle.dump(task_id_to_performance, fp)