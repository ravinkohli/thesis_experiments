import argparse
import os

import pandas as pd

from cd_creater_utils import draw_cd_diagram

parser = argparse.ArgumentParser(
    description='Run autoPyTorch on a benchmark'
)

parser.add_argument(
    '--csv',
    type=str,
    default='thesis_other_results/cd_diagram_all',
)

args = parser.parse_args()
options = vars(args)
print(options)

if __name__ == '__main__':

    df_perf = pd.read_csv(f'{args.csv}.csv',index_col=False, sep=';')

    df_perf['test_accuracy'] *= 100
    draw_cd_diagram(df_perf=df_perf, title='Balanced Accuracy', labels=True, figname=os.path.join('cd_diagram_plots', args.csv.split('/')[-1]))