import pandas as pd

result_df = pd.read_csv('final_thesis_results/gathered_results_size_11.csv')

result_df = result_df.astype({'experiment_name': 'category'})
all_experiment_names = result_df['experiment_name'].cat.categories


with pd.ExcelWriter('final_thesis_results/split_gathered_results.xlsx') as w:
    for experiment_name in all_experiment_names:
        result_df[result_df['experiment_name'] == experiment_name].to_excel(w, experiment_name)