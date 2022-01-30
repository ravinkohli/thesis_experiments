import argparse
import os

import openml
import pandas as pd


def get_task_ids():
    # test datasets
    test_task_ids = [232, 167149, 167161, 235, 167168, 167184 , 167104, 189871, 189860, 167201]
    
    # 168794, 168797, 168796, 189861, 167185, 189872, 18990, 7510, 167152, 168793, 189862, 126026, 189866,
    #     189873, 168792, 75193, 168798, , , 167200, 189874, 167181, 167083, , 189865, 189906, , 126029,
    #     , 126025, 5097, 168795, 75127, 189905, 189909, 167190, ]

    return test_task_ids

def get_task_times():
    test_task_times = [300, 300, 300, 300, 300, 300, 300, 4000, 6000, 4200]
    return test_task_times


if __name__ == "__main__":
    task_id_function = get_task_ids
    task_ids = task_id_function()
    dataset_table = {
        'Task Id': [],
        'Dataset Name': [],
        'Number of examples': [],
        'Number of features': [],
        'Majority class percentage': [],
        'Minority class percentage': [],
    }
    for task_id in task_ids:
        task = openml.tasks.get_task(task_id, download_data=False)
        dataset = openml.datasets.get_dataset(task.dataset_id, download_data=False)
        dataset_table['Task Id'].append(task_id)
        dataset_table['Dataset Name'].append(dataset.name)
        dataset_table['Number of examples'].append(dataset.qualities['NumberOfInstances'])
        dataset_table['Number of features'].append(dataset.qualities['NumberOfFeatures'])
        dataset_table['Majority class percentage'].append(f"{dataset.qualities['MajorityClassPercentage']:.3f}")
        dataset_table['Minority class percentage'].append(f"{dataset.qualities['MinorityClassPercentage']:.3f}")

    output_path = './dataset_collection.csv'

    dataset_info_frame = pd.DataFrame.from_dict(dataset_table)
    dataset_info_frame.to_csv(output_path, index=False)