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
    default='average_ranks_per_task',
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

args = parser.parse_args()
options = vars(args)
print(options)

if __name__ == '__main__':
    sets = SETS[f"size_{args.size}"]
    for experiment_set in sets:
        # if experiment_set != 'ebo_1_pef':
        #     continue
        try:
            result_dir = f'final_thesis_results/ensemble_size_{args.size}'
            out_dir = os.path.join(result_dir, experiment_set)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            all_df = pd.read_csv(os.path.join(out_dir, f'average_ranks_per_task.csv')).sort_values("Unnamed: 0")
            all_df["strategy"] = all_df['Unnamed: 0'].str.replace('Post-hoc ensemble', 'Post-hoc')
            all_df["All"] = all_df['0']
            all_df = all_df.drop(['0','Unnamed: 0'], axis=1)
            all_df = all_df.sort_values('strategy')
            ranks_per_tasks = [all_df] # {args.csv}.csv'))}
            for benchmark in ['Small Benchmark', 'Medium Benchmark']:
                current_df = pd.read_csv(os.path.join(out_dir, f"{benchmark.split(' ')[0].lower()}", f'average_ranks_per_task.csv')).sort_values("Unnamed: 0")
                current_df["strategy"] = current_df['Unnamed: 0'].str.replace('Post-hoc ensemble', 'Post-hoc')
                current_df[benchmark] = current_df['0']
                current_df = current_df.drop(['0','Unnamed: 0'], axis=1)
                current_df = current_df.sort_values('strategy')
                ranks_per_tasks.append(current_df)

            df = pd.concat(ranks_per_tasks, axis=1)

            df = df.loc[:,~df.columns.duplicated()].copy()
            df.round(2).to_csv(os.path.join(out_dir, f"{args.csv}_all.csv"), index=False)
        except:
            pass