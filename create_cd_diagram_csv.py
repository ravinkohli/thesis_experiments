from genericpath import exists
import pandas as pd

from cd_creater_utils import ALGORITHM_COLUMN_NAME, PERFORMANCE_METRIC_COLUMN_NAME

data = pd.read_csv('Thesis Results-incomplete - all_methods.csv')


individual_dfs = []
for column in data.columns[1:]:
    df = data[['task_id', column]].copy()
    df[PERFORMANCE_METRIC_COLUMN_NAME] = df[column]
    df = df.drop(columns=[column])
    column_names = pd.Series([column.replace('_mean', '')] * data.shape[1])
    df[ALGORITHM_COLUMN_NAME] = column_names
    individual_dfs.append(df)

pd.concat(individual_dfs, axis=0, ignore_index=True).to_csv('cd_diagram_pre_results.csv')
