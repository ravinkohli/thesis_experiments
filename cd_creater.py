import argparse
import os

import pandas as pd

from cd_creater_utils import ALGORITHM_COLUMN_NAME, PERFORMANCE_METRIC_COLUMN_NAME, TASK_COLUMN_NAME, draw_cd_diagram
from plot_utilities import test_method, task_bool_mask



def create_performance_df(final_combined_results_file, results_dir):
    data = pd.read_csv(final_combined_results_file)

    individual_dfs = []
    for column in data.columns[1:]:
        df = data[['task_id', column]].copy()
        df[PERFORMANCE_METRIC_COLUMN_NAME] = df[column]
        df = df.drop(columns=[column])
        column_names = pd.Series([column.replace('_mean', '')] * data.shape[1])
        df[ALGORITHM_COLUMN_NAME] = column_names
        individual_dfs.append(df)

    df = pd.concat(individual_dfs, axis=0, ignore_index=True)
    df.to_csv(os.path.join(results_dir, 'performance_df.csv'), index=False)
    return df

def save_comparison(out_dir, csv_file, experiment_set, strategies, name_to_label, final_combined_results_file, results_dir, size=5, benchmark=None):
    if not os.path.exists(os.path.join(results_dir, 'performance_df.csv')):
        df_perf = create_performance_df(final_combined_results_file, results_dir=results_dir)
    else:
        df_perf = pd.read_csv(os.path.join(results_dir, 'performance_df.csv'))

    # df_perf[PERFORMANCE_METRIC_COLUMN_NAME] *= 100
    print("Before", df_perf.shape)
    df_perf = df_perf.iloc[task_bool_mask(
        df_perf[TASK_COLUMN_NAME], benchmark, size)]
    print("After", df_perf.shape)
    df_perf = df_perf.iloc[test_method(
        df_perf[ALGORITHM_COLUMN_NAME], strategies)]
    df_perf = df_perf.replace(name_to_label)
    draw_cd_diagram(
        setname=experiment_set,
        df_perf=df_perf,
        title='Balanced Accuracy',
        labels=True, out_dir=out_dir,
        figname=os.path.join(out_dir, f"{csv_file.split('/')[-1]}"))
