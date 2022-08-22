import pandas as pd
from itertools import product
values = [[True, False]]*4
values.append([1,2])
boolean_keys = ['posthoc_ensemble_fit', 'enable_traditional_pipeline', 'use_ensemble_opt_loss', 'warmstart']
boolean_keys.append('num_stacking_layers')
xl_file = pd.ExcelFile('gathered_results_proper_2.xlsx')
dfs = {sheet_name: xl_file.parse(sheet_name) 
          for sheet_name in xl_file.sheet_names}
# sebo = []
# for key in dfs:
# 	if 'SEBO' in key:
# 		sebo.append(dfs[key])

# for key in list(dfs.keys()):
# 	if 'SEBO' in key:
# 		del dfs[key]

# dfs['stacking_ensemble_optimisation'] = pd.concat(sebo)

for key in list(dfs.keys()):
        dfs[key].columns =  dfs[key].iloc[0]
        dfs[key] = dfs[key][1:]

# key = 'stacking_ensemble_selection_pe1'
# dfs[key].columns =  dfs[key].iloc[0]
# dfs[key] = dfs[key][1:]

product_values = list(product(*values))

sorted_dfs = {}
delete_keys = []
for experiment_name in dfs.keys():
    delete_keys.append(experiment_name)
    for p_values in product_values:
        name = experiment_name
        for key, val in zip(boolean_keys, p_values):
            name = name + f"_{''.join([k[0] for k in key.split('_')])}_{str(val)[0]}"
        sorted_dfs[name] = dfs[experiment_name].copy()
        for key, val in zip(boolean_keys, p_values):
            sorted_dfs[name] = sorted_dfs[name].loc[sorted_dfs[name][key] == val]

dfs = sorted_dfs
# len([key for key in dfs if 'sebo' in key])
# print(dfs.keys())

# del dfs['stacking_ensemble_optimisation']

for key in list(dfs.keys()):
    if 'test balanced accuracy' in dfs[key].columns:
        dfs[key] = dfs[key].astype({'test balanced accuracy':float})
        keep_keys = [b_key for b_key in boolean_keys if b_key in dfs[key].columns]
        # print(f"{key}") #: {dfs[key].columns}")
        if not dfs[key].empty:
            for k_key in keep_keys:
                print(f"{k_key} = {dfs[key][k_key].iloc[0]}")
            dfs[f'{key}_mean'] = dfs[key][dfs[key]['test balanced accuracy'] != 0].groupby('task_id')['test balanced accuracy'].mean()
            dfs[f'{key}_std'] = dfs[key][dfs[key]['test balanced accuracy'] != 0].groupby('task_id')['test balanced accuracy'].std()
        del dfs[key]
    else:
        print("problem in ", key)

# print(dfs.keys())
# writer = pd.ExcelWriter('test.xlsx', engine='openpyxl')
# for df_name, df in dfs.items():
#     df.to_excel(writer, sheet_name=df_name)

# writer.save()
for key in list(dfs.keys()):
    # print(key)
    if dfs[key].empty:
        del dfs[key]
    else:
        dfs[key] = dfs[key].rename(key)
    # else:
    #     dfs[key][key] = dfs[key]['test balanced accuracy']
    #     dfs[key] = dfs[key].drop(['test balanced accuracy'], axis=1)

pd.concat([val for key, val in dfs.items() if 'mean' in key], axis=1).fillna(0).to_csv('combined_results_mean_new_2(22.08).csv')
pd.concat([val for key, val in dfs.items() if 'std' in key], axis=1).fillna(0).to_csv('combined_results_std_new_2(22.08).csv')

