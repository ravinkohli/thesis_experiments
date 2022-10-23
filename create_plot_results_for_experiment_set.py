import argparse
import os
import pickle
from shutil import which
from cd_creater import save_comparison, test_method
from cd_creater_utils import ALGORITHM_COLUMN_NAME, TASK_COLUMN_NAME
from get_acc_per_method import store_combined_results, store_split_excel_file
from plot_ensemble_history import make_incumbent_plot
from experiment_utils import DATASET_INFO, SETS, replace_key
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from plot_utilities import make_overfit_plot, replace_name, task_bool_mask

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
    '--set',
    type=str,
    default='ebo_1_etp',
)
parser.add_argument(
    '--comparison',
    action='store_true'
)
parser.add_argument(
    '--ensemble_plot',
    action='store_true'
)
parser.add_argument(
    '--plot_ranks',
    action='store_true'
)
parser.add_argument(
    '--perf_file',
    type=str,
    default='task_id_to_performance'
    # default='trial_for_now'
)
parser.add_argument(
    '--eih_perf_file',
    type=str,
    default='trial_for_now'
)
parser.add_argument(
    '--dur_file',
    type=str,
    default='task_id_to_duration'
)
parser.add_argument(
    '--overfit',
    action='store_true'
)
parser.add_argument(
    '--set_combined',
    action='store_true'
)
args = parser.parse_args()
options = vars(args)
print(options)

if __name__ == '__main__':
    sets = SETS[f"size_{args.size}"]
    for experiment_set in sets:
        if experiment_set != args.set:
            continue
        result_dir = f'final_thesis_results/ensemble_size_{args.size}'
        out_dir = os.path.join(result_dir, experiment_set, 'overfit')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        for dataset in ['train', 'test']:
            final_combined_results_file = os.path.join(out_dir, f'combined_results_mean_{dataset}.csv')
            if not os.path.exists(final_combined_results_file):
                store_split_excel_file(out_dir, args.size, result_dir, dataset)
                store_combined_results(out_dir, dataset)

            dataset_info = pd.read_csv(DATASET_INFO)
            
            strategies = sets[experiment_set]['strategies']
            name_to_label = sets[experiment_set]['NAME_TO_LABEL']
            color_marker = sets[experiment_set]['color_marker']
            results = pickle.load(open(os.path.join(result_dir, f"{args.perf_file}_size_{args.size}.pkl"), 'rb'))
            eih_results = pickle.load(open(os.path.join(result_dir, f"{args.eih_perf_file}_size_{args.size}.pkl"), 'rb'))
            durations = pickle.load(open(os.path.join(result_dir,f"{args.dur_file}_size_{args.size}.pkl"), 'rb'))

            new_results = {}
            for strategy in results:
                new_results[replace_key(strategy)] = results[strategy]
            del results

            new_durations = {}
            for strategy in durations:
                new_durations[replace_key(strategy)] = durations[strategy]
            del durations
            
            if args.set_combined:
                try:
                    df = pd.read_csv(final_combined_results_file)
                    print("Before", df.shape)
                    # print(strategies)
                    # print(df.columns)
                    df = df.iloc[task_bool_mask(
                        df['task_id'], size=args.size)]
                    print("After", df.shape)
                    new_df = df[[strategy+'_mean' for strategy in strategies]]
                    column_names = [strategy for strategy in strategies]
                    new_df.columns = column_names
                    new_df['Dataset']  = list(map(replace_name, df['task_id']))

                    new_df = new_df.round(decimals=2)
                    new_column_names = ['Dataset']
                    new_column_names.extend(column_names)
                    new_df = new_df[new_column_names]
                    new_df.to_csv(os.path.join(out_dir, f'combined_results_mean_{dataset}_{experiment_set}.csv'), index=False)
                except Exception as e:
                    raise(e)
            
            if args.ensemble_plot and dataset == 'test':
                try:
                    trajectories = make_incumbent_plot(figure_output_dir=os.path.join(out_dir, f"{dataset}_plots"), dataset_info=dataset_info, strategies=strategies, results=new_results, name_to_label=name_to_label, color_marker=color_marker, dataset=dataset, durations=new_durations, eih_results=eih_results)
                except Exception as e:
                    # raise(e)
                    continue
                if args.plot_ranks:
                    print(trajectories)

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
                results_dir=result_dir)

        # break