import argparse
import os

import pandas as pd

from cd_creater_utils import ALGORITHM_COLUMN_NAME, PERFORMANCE_METRIC_COLUMN_NAME, draw_cd_diagram

sets = {
    'num_stacking_layers_2': [
      'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2', 'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2',
 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 'sft_pef_F_etp_F_ueol_F_w_F_nsl_2', 'sft_pef_T_etp_F_ueol_F_w_F_nsl_2', 'sft_pef_T_etp_T_ueol_F_w_F_nsl_2'],
    'ebo_1': [
      'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'ebo_pef_F_etp_F_ueol_T_w_F_nsl_1',
      'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 
      'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1',
      'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
      'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1',
    ],
    'ebo': [
      'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'ebo_pef_F_etp_F_ueol_T_w_F_nsl_1',
      'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 
      'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1',
      'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
      'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1',
      'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2',
      'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2',
      'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
      'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2',
    ],
    'eih_1': [
      'eih_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'eih_pef_F_etp_F_ueol_F_w_T_nsl_1', 
      'eih_pef_F_etp_T_ueol_F_w_T_nsl_1',
      'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 
      'eih_pef_T_etp_F_ueol_F_w_T_nsl_1',
      'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 
      'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
    ],
    'eih': [
      'eih_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'eih_pef_F_etp_F_ueol_F_w_T_nsl_1', 
      'eih_pef_F_etp_T_ueol_F_w_T_nsl_1',
      'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 
      'eih_pef_T_etp_F_ueol_F_w_T_nsl_1',
      'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 
      'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
      'eihr_pef_F_etp_F_ueol_F_w_T_nsl_2',
      'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
      'eihr_pef_T_etp_F_ueol_F_w_T_nsl_2',
      'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2',
      'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
      'eihs_pef_F_etp_F_ueol_F_w_T_nsl_2',
      'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
      'eihs_pef_T_etp_F_ueol_F_w_T_nsl_2',
      'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2',
      'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
    ],
    'es_1': [
      'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
    ],
    'es': [
      'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
      'esr_pef_F_etp_F_ueol_F_w_F_nsl_2',
      'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
      'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2',
      'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
   ],
    'ebo_2': ['ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2'],
    'es_2': [
 'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2', 'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2',
 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2'],
    'eih_2': [
      'eihr_pef_F_etp_F_ueol_F_w_T_nsl_2',
      'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
      'eihr_pef_T_etp_F_ueol_F_w_T_nsl_2',
      'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2',
      'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
      'eihs_pef_F_etp_F_ueol_F_w_T_nsl_2',
      'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
      'eihs_pef_T_etp_F_ueol_F_w_T_nsl_2',
      'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2',
      'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
 ],
    'num_stacking_layers_1': [
       'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'ebo_pef_F_etp_F_ueol_T_w_F_nsl_1',
      'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 
      'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1',
      'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
      'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1',
      'eih_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'eih_pef_F_etp_F_ueol_F_w_T_nsl_1', 
      'eih_pef_F_etp_T_ueol_F_w_T_nsl_1',
      'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 
      'eih_pef_T_etp_F_ueol_F_w_T_nsl_1',
      'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 
      'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
      'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
    ],

    'all': [
      'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'ebo_pef_F_etp_F_ueol_T_w_F_nsl_1',
      'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 
      'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1',
      'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
      'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1',
      'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2',
      'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2',
      'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
      'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2',
      'eih_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'eih_pef_F_etp_F_ueol_F_w_T_nsl_1', 
      'eih_pef_F_etp_T_ueol_F_w_T_nsl_1',
      'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 
      'eih_pef_T_etp_F_ueol_F_w_T_nsl_1',
      'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 
      'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
      'eihr_pef_F_etp_F_ueol_F_w_T_nsl_2',
      'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
      'eihr_pef_T_etp_F_ueol_F_w_T_nsl_2',
      'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2',
      'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
      'eihs_pef_F_etp_F_ueol_F_w_T_nsl_2',
      'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
      'eihs_pef_T_etp_F_ueol_F_w_T_nsl_2',
      'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2',
      'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
      'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
      'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
      'esr_pef_F_etp_F_ueol_F_w_F_nsl_2',
      'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
      'sa_pef_F_etp_F_ueol_F_w_F_nsl_2',
      'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2',
      'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
      'sft_pef_F_etp_F_ueol_F_w_F_nsl_2',
      'sft_pef_T_etp_F_ueol_F_w_F_nsl_2',
      'sft_pef_T_etp_T_ueol_F_w_F_nsl_2'],

    'sft': [
      'sft_pef_F_etp_F_ueol_F_w_F_nsl_2',
      'sft_pef_T_etp_F_ueol_F_w_F_nsl_2',
      'sft_pef_T_etp_T_ueol_F_w_F_nsl_2'
    ],
    'etp_T': 
      ['ebos_pef_T_etp_T_ueol_T_w_F_nsl_2',
      'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2',
      'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2',
      'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2',
      'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 
      'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
      'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1',
      'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
      'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
      'es_pef_F_etp_T_ueol_F_w_F_nsl_1'],
    'etp_F': 
      [ 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
      'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2',
      'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
      'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
      'eih_pef_T_etp_F_ueol_F_w_F_nsl_1',
      'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1',
      'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2',
      'esr_pef_F_etp_F_ueol_F_w_F_nsl_2',
      'es_pef_F_etp_F_ueol_F_w_F_nsl_1'],
    'ebos_ebor':
      [
         'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
         'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2'],
    'eihs_eihr':
      [
         'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
         'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
      ],
    'ebo_eih': [
 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1',
 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1',
    ],
    'ebos_eihs_sespl': ['ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2', 'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2'],
    'ebor_eihr_esr': [
 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2'],
}
parser = argparse.ArgumentParser(
    description='Run autoPyTorch on a benchmark'
)

def test_method(df_method:  pd.Series, values):
    bool_mask = []
    for method in df_method.items():
        bool_mask.append(any(val in method[1] for val in values))
    return bool_mask

parser.add_argument(
    '--csv',
    type=str,
    default='results',
)
parser.add_argument(
    '--set',
    choices=sets,
    default='num_stacking_layers_2',
)
args = parser.parse_args()
options = vars(args)
print(options)

if __name__ == '__main__':

    df_perf = pd.read_csv(f'{args.csv}.csv',index_col=False, sep=',')

    df_perf[PERFORMANCE_METRIC_COLUMN_NAME] *= 100

    df_perf = df_perf.iloc[test_method(df_perf[ALGORITHM_COLUMN_NAME], sets[args.set])]
    draw_cd_diagram(df_perf=df_perf, title='Balanced Accuracy', labels=True, figname=os.path.join('final_thesis_results/cd_diagram_plots', f"{args.csv.split('/')[-1]}_{args.set}"))