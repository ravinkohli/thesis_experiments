from utilities import _get_experiment_args
from itertools import product


experiment_args = _get_experiment_args()

parameters = {
    'stacking_ensemble_bayesian_optimisation':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [7],
        'use_ensemble_opt_loss': [True, False],
        'num_stacking_layers': [1, 2], # , 3],
        'posthoc_ensemble_fit_stacking_ensemble_optimization': [True, False],
        'enable_traditional_pipeline': [True, False],
    },
    'ensemble_selection':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [7],
        'enable_traditional_pipeline': [True, False],
    },
    'stacking_ensemble_selection_per_layer':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [7],
        'num_stacking_layers': [2], # , 3],
        'enable_traditional_pipeline': [True, False],
    },
    'stacking_repeat_models':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'ensemble_size': [7],
        'num_stacking_layers': [2], # , 3],
        'enable_traditional_pipeline': [True, False],
    },
    'stacking_autogluon':
    {
        'splits': [3], # , 5],
        'repeats': [2], # [1, 2],
        'num_stacking_layers': [2], # , 3],
    },
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



# for p_values in product_values:
#     name = 'sebo_'
#     for key, val in zip(boolean_keys, p_values):
#         name = name + f'{key}_{val}'
#     dfs[name] = dfs['stacking_ensemble_optimisation'].copy()
#     for key, val in zip(boolean_keys, p_values):
#         dfs[name] = dfs[name].loc[dfs[name][key] == val]