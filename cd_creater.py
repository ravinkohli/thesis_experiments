import argparse
import os

import pandas as pd

from cd_creater_utils import draw_cd_diagram

sets = {
    'num_stacking_layers_2': ['ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2',
 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2'],
    'ebo': ['ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1'],
    'eih': [
 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1'],
    'es': [
 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
 'es_pef_F_etp_F_ueol_F_w_F_nsl_1'],
    'ebo_2': ['ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2'],
    'es_2': [
 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2',
 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2'],
    'eih_2': [
 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
 ],
    'num_stacking_layers_1': [
 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1',
 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1',
 'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
 'es_pef_F_etp_F_ueol_F_w_F_nsl_1'],
    'all': ['ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1',
 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1',
 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2',
 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
 'es_pef_F_etp_F_ueol_F_w_F_nsl_1'],
    'etp_T': 
['ebos_pef_T_etp_T_ueol_T_w_F_nsl_2',
 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2',
 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2',
 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2',
 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 
 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1',
 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2',
 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
 'es_pef_F_etp_T_ueol_F_w_F_nsl_1'],
    'etp_F': 
[ 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1',
 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1',
 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2',
 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2',
 'es_pef_F_etp_F_ueol_F_w_F_nsl_1'],
    'ebos_ebor': ['ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2'],
    'eihs_eihr': [
 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
 ],
    'ebo_eih': [
 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1',
 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1',
    ],
    'ebos_eihs_ess': ['ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2'],
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

    df_perf = pd.read_csv(f'{args.csv}.csv',index_col=False, sep=';')

    df_perf['test_accuracy'] *= 100

    df_perf = df_perf.iloc[test_method(df_perf['method'], sets[args.set])]
    draw_cd_diagram(df_perf=df_perf, title='Balanced Accuracy', labels=True, figname=os.path.join('cd_diagram_plots_new', f"{args.csv.split('/')[-1]}_{args.set}"))