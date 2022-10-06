import argparse
import os
import pickle
from re import L
from cd_creater import save_comparison
from get_acc_per_method import store_combined_results, store_split_excel_file
from plot_ensemble_history import make_incumbent_plot
from experiment_utils import DATASET_INFO, SETS, replace_key
import pandas as pd
import matplotlib.pyplot as plt

from plot_utilities import make_overfit_plot


parser = argparse.ArgumentParser(
    description='Run autoPyTorch on a benchmark'
)

parser.add_argument(
    '--csv',
    type=str,
    default='cd_diagram_pre_results',
)

parser.add_argument(
    '--size',
    type=int,
    default=5,
)

parser.add_argument(
    '--comparison',
    action='store_true'
)
parser.add_argument(
    '--perf_file',
    type=str,
    default='task_id_to_performance.pkl'
)
parser.add_argument(
    '--dur_file',
    type=str,
    default='task_id_to_duration.pkl'
)
parser.add_argument(
    '--overfit',
    action='store_true'
)
args = parser.parse_args()
options = vars(args)
print(options)


def replace_name(task_id):
    dataset_df = pd.read_csv('dataset_collection.csv')
    name = dataset_df[dataset_df['OpenML Task Id'] == int(task_id)]['Dataset Name'].item()
    return name


if __name__ == '__main__':
    experiment_sets = SETS[f"size_{args.size}"]
    for experiment_set in experiment_sets:
        # if experiment_set != 'all_base':
        #     continue
        try:
            result_dir = f'final_thesis_results/ensemble_size_{args.size}'
            out_dir = os.path.join(result_dir, experiment_set)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            print(out_dir)
            for dataset in ['train', 'test']:
                final_combined_results_file = os.path.join(out_dir, f'combined_results_mean_{dataset}.csv')
                if not os.path.exists(final_combined_results_file):
                    store_split_excel_file(out_dir, args.size, result_dir, dataset)
                    store_combined_results(out_dir, dataset)

                dataset_info = pd.read_csv(DATASET_INFO)
                
                strategies = experiment_sets[experiment_set]['strategies']
                name_to_label = experiment_sets[experiment_set]['NAME_TO_LABEL']
                color_marker = experiment_sets[experiment_set]['color_marker']

            if args.overfit:
                make_overfit_plot(out_dir, strategies, name_to_label, color_marker)

            if args.comparison:
                save_comparison(
                    out_dir=out_dir,
                    experiment_set=experiment_set,
                    strategies=strategies,
                    name_to_label=name_to_label,
                    final_combined_results_file=final_combined_results_file,
                    csv_file=args.csv,
                    results_dir=result_dir,
                    size=args.size)
        except Exception as e:
            raise e
            pass




# ax = data.plot.scatter(y='task_id', x=['EBO'], xlim=(-18, 5), grid=True, figsize=(10, 10))
# data.plot.scatter(y='task_id', x=['iEBO'], xlim=(-18, 5), grid=True, figsize=(10, 10), ax=ax)
# data.plot.scatter(y='task_id', x=['HPO + GES'], xlim=(-18, 5), grid=True, figsize=(10, 10), ax=ax)