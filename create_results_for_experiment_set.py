import argparse
import os
import pickle
from re import L
from cd_creater import save_comparison
from get_acc_per_method import store_combined_results, store_split_excel_file
from plot_ensemble_history import make_incumbent_plot
from experiment_utils import DATASET_INFO, SETS, replace_key
import pandas as pd


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
    '--perf_file',
    type=str,
    default='task_id_to_performance'
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
args = parser.parse_args()
options = vars(args)
print(options)

if __name__ == '__main__':
    sets = SETS[f"size_{args.size}"]
    result_dir = f'final_thesis_results/ensemble_size_{args.size}'
    out_dir = os.path.join(result_dir, args.set)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for dataset in ['train', 'test']:
        final_combined_results_file = os.path.join(out_dir, f'combined_results_mean_{dataset}.csv')
        if not os.path.exists(final_combined_results_file):
            store_split_excel_file(out_dir, args.size, result_dir, dataset)
            store_combined_results(out_dir, dataset)

        dataset_info = pd.read_csv(DATASET_INFO)
        
        strategies = sets[args.set]['strategies']
        name_to_label = sets[args.set]['NAME_TO_LABEL']
        color_marker = sets[args.set]['color_marker']
        results = pickle.load(open(os.path.join(result_dir, f"{args.perf_file}_size_{args.size}.pkl"), 'rb'))
        durations = pickle.load(open(os.path.join(result_dir,f"{args.dur_file}_size_{args.size}.pkl"), 'rb'))

        new_results = {}
        for strategy in results:
            new_results[replace_key(strategy)] = results[strategy]
        del results

        new_durations = {}
        for strategy in durations:
            new_durations[replace_key(strategy)] = durations[strategy]
        del durations
        
        if args.ensemble_plot:
            make_incumbent_plot(figure_output_dir=os.path.join(out_dir, f"{dataset}_plots"), dataset_info=dataset_info, strategies=strategies, results=new_results, name_to_label=name_to_label, color_marker=color_marker, dataset=dataset, durations=new_durations)

    if args.overfit:
        combined_results = []
        for dataset in ['train', 'test']:
            combined_results.append(pd.read_csv(os.path.join(out_dir, f'combined_results_mean_{dataset}.csv')))
        (combined_results[1] - combined_results[0]).to_csv(os.path.join(out_dir, f'combined_results_overfit.csv'), index=False)

    if args.comparison:
        save_comparison(
            out_dir=out_dir,
            experiment_set=args.set,
            strategies=strategies,
            name_to_label=name_to_label,
            final_combined_results_file=final_combined_results_file,
            csv_file=args.csv,
            results_dir=result_dir)