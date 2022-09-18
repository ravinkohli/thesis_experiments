import openml
import pandas as pd

from experiment_utils import DATASET_INFO


def get_task_ids():
    # test datasets
    test_task_ids = [
       10101, 53, 146818, 31, 12, 3917, 146822, 9981, 146821, 9952, 3, 168912,
       168911, 168910, 168908, 9977, 167119, 14965, 146212, 168331, 7592, 168329,
       168330, 168868, 167120, 168909, 146195, 146606, 168335, 146825,
    ]
    return test_task_ids

# def get_task_times():
#     test_task_times = [300, 300, 300, 300, 300, 300, 300, 4000, 6000, 4200]
#     return test_task_times

small_task_ids = [3, 12, 31, 53, 3917, 9952, 9981, 10101, 146606, 146818, 146821, 146822, 168908, 168909, 168910, 168911, 168912]
medium_task_ids = [9977, 167119, 14965, 146212, 168331, 7592, 168329, 168330, 168868, 167120, 146195, 168335, 146825]

if __name__ == "__main__":
    task_ids = get_task_ids()
    dataset_table = {
        'OpenML Task Id': [],
        'Dataset Name': [],
        'Instances': [],
        'Features': [],
        'Classes': [],
        # 'Minority class percentage': [],
    }
    for task_id in task_ids:
        task = openml.tasks.get_task(task_id, download_data=False)
        dataset = openml.datasets.get_dataset(task.dataset_id, download_data=False)
        dataset_table['OpenML Task Id'].append(task_id)
        dataset_table['Dataset Name'].append(dataset.name)
        if task_id in small_task_ids:
            type_ = 's'
        else:
            type_ = 'm'
        dataset_table['Instances'].append(f"{int(dataset.qualities['NumberOfInstances'])} ({type_})")
        dataset_table['Features'].append(int(dataset.qualities['NumberOfFeatures']))
        dataset_table['Classes'].append(int(dataset.qualities['NumberOfClasses']))
        # dataset_table['Minority class percentage'].append(f"{dataset.qualities['MinorityClassPercentage']:.3f}")


    dataset_info_frame = pd.DataFrame.from_dict(dataset_table).sort_values(by='OpenML Task Id')
    dataset_info_frame.to_csv(DATASET_INFO, index=False)