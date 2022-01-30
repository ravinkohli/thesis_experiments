import argparse
from cgi import test
import json
from operator import ge
import os
import pandas as pd
import pickle
import random
import time
import warnings
from zipfile import ZipFile

os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'


warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

import torch

from autoPyTorch.api.tabular_classification import TabularClassificationTask
from autoPyTorch.datasets.resampling_strategy import HoldoutValTypes

import numpy as np

from smac.tae import StatusType

def str2bool(v):
    if isinstance(v, bool):
        return [v, ]
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return [True, ]
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return [False, ]
    elif v.lower() == 'conditional':
        return [True, False]
    else:
        raise argparse.ArgumentTypeError('No valid value given.')


parser = argparse.ArgumentParser(
    description='Run autoPyTorch on a benchmark'
)
# experiment setup arguments
parser.add_argument(
    '--task_id',
    type=int,
    default=233088,
)
parser.add_argument(
    '--wall_time',
    type=int,
    default=3000,
)
parser.add_argument(
    '--func_eval_time',
    type=int,
    default=500,
)
parser.add_argument(
    '--epochs',
    type=int,
    default=5,
)
parser.add_argument(
    '--seed',
    type=int,
    default=11,
)
parser.add_argument(
    '--tmp_dir',
    type=str,
    default='./runs/autoPyTorch_portfolio',
)
parser.add_argument(
    '--output_dir',
    type=str,
    default='./runs/autoPyTorch_portfolio',
)
parser.add_argument(
    '--nr_workers',
    type=int,
    default=1,
)
parser.add_argument(
    '--experiment_name',
    type=str,
    default='stacked_ensemble'
)

args = parser.parse_args()
options = vars(args)
print(options)



if __name__ == '__main__':
    from utilities import (
        get_data,
        get_smac_object,
        get_experiment_args
    )

    # Setting up reproducibility
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)

    ############################################################################
    # Data Loading
    # ============
    start_time = time.time()
    X_train, X_test, y_train, y_test, categorical_indicator = get_data(
        task_id=args.task_id,
        seed=args.seed,
    )

    output_dir = os.path.expanduser(
        os.path.join(
            args.output_dir,
            f'out',
        )
    )
    temp_dir = os.path.expanduser(
        os.path.join(
            args.tmp_dir,
            f'tmp',
        )
    )

    init_args, search_args = get_experiment_args(args.experiment_name)
    ############################################################################
    # Build and fit a classifier
    # ==========================


    api = TabularClassificationTask(
        temporary_directory=temp_dir,
        output_directory=output_dir,
        delete_tmp_folder_after_terminate=False,
        delete_output_folder_after_terminate=False,
        seed=args.seed,
        **init_args
    )

    ############################################################################
    # Search for the best hp configuration
    # =====================================================

    # We search for the best hp configuration only in the case of a cocktail ingredient
    # that has hyperparameters from which it is controlled

    api.search(
        X_train=X_train.copy(),
        y_train=y_train.copy(),
        X_test=X_test.copy(),
        y_test=y_test.copy(),
        optimize_metric='balanced_accuracy',
        total_walltime_limit=args.wall_time,
        memory_limit=12000,
        func_eval_time_limit_secs=args.func_eval_time,
        enable_traditional_pipeline=False,
        get_smac_object_callback=get_smac_object,
        smac_scenario_args={
            'runcount_limit': 1000,
        },
        **search_args
    )

    train_preds = api.predict(X_train)
    test_preds = api.predict(X_test)
    train_score = api.score(train_preds, y_train)
    test_score = api.score(test_preds, y_test)
    duration = time.time() - start_time

    print(f'Final Train Balanced accuracy: {train_score}')
    print(f'Final Test Balanced accuracy: {test_score}')
    print(f'Time taken: {duration}')

    # result_directory = os.path.expanduser(
    #     os.path.join(
    #         args.output_dir,
    #     )
    # )
    result_dict = {
        'train balanced accuracy': train_score,
        'test balanced accuracy': test_score,
        'task_id': args.task_id,
        'duration': duration,
    }
    # os.makedirs(result_directory, exist_ok=True)
    with open(os.path.join(args.output_dir, 'final_result.json'), 'w') as file:
        json.dump(result_dict, file)
