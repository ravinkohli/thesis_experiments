from utilities import _get_experiment_args
from itertools import product


experiment_args = _get_experiment_args()

parameters = {
    'ensemble_bayesian_optimisation':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [11],
        'use_ensemble_opt_loss': [True, False],
        'num_stacking_layers': [1], #, 2], # , 3],
        'posthoc_ensemble_fit': [False],
        'enable_traditional_pipeline': [False],
    },
    'ensemble_iterative_hpo':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [11],
        'num_stacking_layers': [1], #, 2], # , 3],
        'posthoc_ensemble_fit': [False], # , False],
        'warmstart': [True],
        'enable_traditional_pipeline': [True, False],
    },
    'ensemble_selection':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [11],
        'num_stacking_layers': [1], #, 2], # , 3],
        'enable_traditional_pipeline': [True, False],
    },
    'ensemble_bayesian_optimisation_stacking':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [11],
        'use_ensemble_opt_loss': [False],
        'num_stacking_layers': [2], # , 3],
        'posthoc_ensemble_fit': [True], # , False],
        'enable_traditional_pipeline': [True, False],
    },
    'ensemble_iterative_hpo_stacking':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [11],
        'num_stacking_layers': [2], # , 3],
        'posthoc_ensemble_fit': [True], # , False],
        'warmstart': [True],
        'enable_traditional_pipeline': [True, False],
    },
    'stacking_ensemble_selection_per_layer':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [11],
        'num_stacking_layers': [2], # , 3],
        'enable_traditional_pipeline': [True, False],
    },
    'ensemble_bayesian_optimisation_repeats':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [11],
        'use_ensemble_opt_loss': [False],
        'num_stacking_layers': [2], # , 3],
        'posthoc_ensemble_fit': [True], # , False],
        'enable_traditional_pipeline': [True, False],
    },
    'ensemble_iterative_hpo_repeats':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [11],
        'num_stacking_layers': [2], # , 3],
        'posthoc_ensemble_fit': [True], # , False],
        'warmstart': [True],
        'enable_traditional_pipeline': [True, False],
    },
    'ensemble_selection_repeats':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [11],
        'num_stacking_layers': [2], # , 3],
        'enable_traditional_pipeline': [True, False],
    },
    'stacking_autogluon':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [11],
        'num_stacking_layers': [2], # , 3],
    },
    'autogluon_original_stacking':{
        'num_bag_sets': [2],
        'num_bag_folds': [3],
        'num_stacking_layers': [2],
    }
}


if __name__ == '__main__':
    all_strings = {}
    for param, values in parameters.items():
        all_strings[param] = []
        for value in values:
            all_strings[param].append(f'"--{param}", "{value}",\n')

    for experiment_name, experiment_arg in experiment_args.items():
        potential_args = []
        for param, values in all_strings.items():
            if param in experiment_arg[0] or param in experiment_arg[1]:
                potential_args.append(list(values))
        potential_args = list(product(*potential_args))
        for potential_arg in potential_args:
            print(experiment_name, ''.join(potential_arg))




# python run_autogluon.py --task_id 10101 --num_bag_sets 2 --num_bag_folds 3 --num_stacking_layers 2 --max_epochs 50 --nr_workers 1 --wall_time 1800 --mem_limit 10000 --func_eval_time 6000 --dataset_compression False --experiment_name autogluon_original_stacking --seed 106 --min_epochs 12 --epochs 50 --exp_dir ./autogluon_runs/task_id

# python run_autogluon.py --t ask_id 3 --num_bag_sets 2 --num_bag_folds 3 --num_stacking_layers 2 --nr_workers 1 --wall_time 1800 --mem_limit 10000 --func_eval_time 6000 --dataset_compression False --experiment_name autogluon_original_stacking --seed 355 --min_epochs 12 --epochs 50 --exp_dir ./autogluon_runs/task_id

# for p_values in product_values:
#     name = 'sebo_'
#     for key, val in zip(boolean_keys, p_values):
#         name = name + f'{key}_{val}'
#     dfs[name] = dfs['stacking_ensemble_optimisation'].copy()
#     for key, val in zip(boolean_keys, p_values):
#         dfs[name] = dfs[name].loc[dfs[name][key] == val]