import argparse
import os
import pandas as pd
from itertools import product

def store_split_excel_file(out_dir, size, result_dir, dataset):

    result_df = pd.read_csv(os.path.join(result_dir, f'gathered_results_size_{size}.csv'))

    result_df = result_df.astype({'experiment_name': 'category'})
    all_experiment_names = result_df['experiment_name'].cat.categories


    with pd.ExcelWriter(os.path.join(out_dir, f'split_gathered_results_{dataset}.xlsx')) as w:
        for experiment_name in all_experiment_names:
            result_df[result_df['experiment_name'] == experiment_name].to_excel(w, experiment_name)

def store_combined_results(out_dir, dataset):
    values = [[True, False]]*4
    values.append([1,2])
    boolean_keys = ['posthoc_ensemble_fit', 'enable_traditional_pipeline', 'use_ensemble_opt_loss', 'warmstart']
    boolean_keys.append('num_stacking_layers')
    product_values = list(product(*values))

    xl_file = pd.ExcelFile(os.path.join(out_dir, f'split_gathered_results_{dataset}.xlsx'))
    dfs = {sheet_name: xl_file.parse(sheet_name, header=None, names=['Unnamed: 0', 'train balanced accuracy', 'test balanced accuracy',
        'task_id', 'duration', 'dataset_name', 'wall_time', 'mem_limit',
        'func_eval_time', 'min_epochs', 'epochs', 'seed', 'splits', 'repeats',
        'exp_dir', 'nr_workers', 'experiment_name', 'use_ensemble_opt_loss',
        'num_stacking_layers', 'ensemble_size', 'posthoc_ensemble_fit',
        'warmstart', 'enable_traditional_pipeline', 'dataset_compression'], skiprows=1) 
            for sheet_name in xl_file.sheet_names}


    sorted_dfs = {}
    delete_keys = []
    for experiment_name in dfs.keys():
        delete_keys.append(experiment_name)
        for p_values in product_values:
            name = ''.join([k[0] for k in experiment_name.split('_')])
            for key, val in zip(boolean_keys, p_values):
                name = name + f"_{''.join([k[0] for k in key.split('_')])}_{str(val)[0]}"
            # name = 
            sorted_dfs[name] = dfs[experiment_name].copy()
            for key, val in zip(boolean_keys, p_values):
                sorted_dfs[name] = sorted_dfs[name].loc[sorted_dfs[name][key] == val]

    dfs = sorted_dfs

    for key in list(dfs.keys()):
        if f'{dataset} balanced accuracy' in dfs[key].columns:
            dfs[key] = dfs[key].astype({f'{dataset} balanced accuracy':float})
            keep_keys = [b_key for b_key in boolean_keys if b_key in dfs[key].columns]
            if not dfs[key].empty:
                for k_key in keep_keys:
                    print(f"{k_key} = {dfs[key][k_key].iloc[0]}")
                temp_df = dfs[key].copy()
                temp_df[f'{dataset} balanced accuracy'] *= 100
                df_group = temp_df[temp_df[f'{dataset} balanced accuracy'] != 0].groupby('task_id')[f'{dataset} balanced accuracy']
                dfs[f'{key}_mean'] = df_group.mean()
                dfs[f'{key}_std'] = df_group.std()
            del dfs[key]
        else:
            print("problem in ", key)

    for key in list(dfs.keys()):
        # print(key)
        if dfs[key].empty:
            del dfs[key]
        else:
            dfs[key] = dfs[key].rename(key)

    pd.concat([val for key, val in dfs.items() if 'mean' in key], axis=1).fillna(0).to_csv(os.path.join(out_dir, f'combined_results_mean_{dataset}.csv'))
    pd.concat([val for key, val in dfs.items() if 'std' in key], axis=1).fillna(0).to_csv(os.path.join(out_dir, f'combined_results_std_{dataset}.csv'))

