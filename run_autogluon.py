import argparse
import logging
import json
import os
import pickle
import shutil
import tempfile
import warnings

import matplotlib

import numpy as np

import openml

import pandas as pd

import psutil

from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.utils.multiclass import type_of_target

from autogluon.tabular import TabularPredictor
from autogluon.core.utils.savers import save_pd, save_pkl
import autogluon.core.metrics as metrics
from autogluon.tabular.version import __version__
from autogluon.tabular.configs.hyperparameter_configs import get_hyperparameter_config

warnings.simplefilter("ignore")
matplotlib.use('agg')  # no need for tk
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# Credits to Francisco Rivera


def get_data(
    task_id: int,
):

    task = openml.tasks.get_task(task_id=task_id)
    dataset = task.get_dataset()
    data, _, _, _ = dataset.get_data(
        dataset_format='dataframe',
    )

    print(data)
    train_indices, test_indices = task.get_train_test_split_indices()

    train = data.iloc[train_indices]
    test = data.iloc[test_indices]

    return {
        'train': train,
        'test': test,
        'label': dataset.default_target_attribute,
    }


def run(config):

    log.info(f"\n**** AutoGluon [v{__version__}] ****\n")
    log.info(f"config:\n{pd.DataFrame([{a:b for a, b in config.items() if a not in ['train', 'test']}]).to_markdown()}")

    metrics_mapping = dict(
        acc=metrics.accuracy,
        auc=metrics.roc_auc,
        f1=metrics.f1,
        logloss=metrics.log_loss,
        mae=metrics.mean_absolute_error,
        mse=metrics.mean_squared_error,
        r2=metrics.r2,
        rmse=metrics.root_mean_squared_error,
        balacc=metrics.balanced_accuracy,
    )

    perf_metric = metrics_mapping[config["metric"]]
    if perf_metric is None:
        raise ValueError(f"Need a valid metric, one from {metrics_mapping}")

    is_classification = config["type"] == 'classification'

    log.info(f"Columns dtypes:\n{config['train'].dtypes}")
    params = get_hyperparameter_config('default')

    params['NN_TORCH']['num_epochs'] = config['epochs']
    params.pop('FASTAI')
    log.info(f"Models to use:\n{json.dumps(params, indent=4, sort_keys=True)}")

    predictor = TabularPredictor(
        label=config['label'],
        eval_metric=perf_metric.name,
        path=config['exp_dir']
    ).fit(
        train_data=config['train'],
        # Enable stacking!
        presets='best_quality',
        time_limit=config["wall_time"],
        hyperparameters=params,
        num_bag_folds=config['num_bag_folds'],
        num_bag_sets=config['num_bag_sets'],
        num_stack_levels=config['num_stack_levels']
    )

    y_test = config['test'][config['label']]
    test = config['test'].drop(columns=config['label'])

    if is_classification:
        probabilities = predictor.predict_proba(test, as_multiclass=True)
        predictions = probabilities.idxmax(axis=1).to_numpy()
    else:
        predictions = predictor.predict(test, as_pandas=False)
        probabilities = None

    leaderboard_kwargs = dict(silent=True, extra_info=True)
    test[config['label']] = y_test
    leaderboard_kwargs['data'] = test

    leaderboard = predictor.leaderboard(**leaderboard_kwargs)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None,
                           'display.width', 1000):
        log.info(leaderboard)

    log.info("\n\n\n")
    leaderboard_kwargs['extra_info'] = False
    leaderboard = predictor.leaderboard(**leaderboard_kwargs)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None,
                           'display.width', 1000):
        log.info(leaderboard)

    return predictions, probabilities, y_test, predictor


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run autogluon on a benchmark'
    )
    # experiment setup arguments
    parser.add_argument(
        '--task_id',
        type=int,
        default=3917,
    )
    parser.add_argument(
        '--wall_time',
        type=int,
        default=1800,
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=50,
    )
    parser.add_argument(
        '--min_epochs',
        type=int,
        default=50,
    )
    parser.add_argument(
        '--num_stacking_layers',
        type=int,
        default=2,
    )
    parser.add_argument(
        '--num_bag_folds',
        type=int,
        default=3,
    )
    parser.add_argument(
        '--num_bag_sets',
        type=int,
        default=1,
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=11,
    )
    parser.add_argument(
        '--exp_dir',
        type=str,
        default='./autogluon_run/'
    )
    parser.add_argument(
        '--func_eval_time',
        type=int,
        default=100800,
    )
    parser.add_argument(
        '--dataset_compression',
        help='whether to use search space updates from the reg cocktails paper',
        default=False,
    )
    parser.add_argument(
        '--experiment_name',
        type=str,
        default='stacked_ensemble'
    )
    parser.add_argument(
        '--nr_workers',
        type=int,
        default=1,
    )
    parser.add_argument(
        '--mem_limit',
        type=int,
        default=8000,
    )
    args = parser.parse_args()

    exp_dir = os.path.join(
        args.exp_dir,
        f'{args.seed}',
        f'{args.task_id}',
    )
    os.makedirs(exp_dir, exist_ok=True)
    # Log to a file
    logFormatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

    fileHandler = logging.FileHandler(os.path.join(exp_dir, 'info.log'))
    fileHandler.setFormatter(logFormatter)
    log.addHandler(fileHandler)

    # Build a configuration to run the experiments
    config = {'task_id': args.task_id, 'exp_dir': exp_dir}

    # Add the train and test data
    config.update(get_data(task_id=args.task_id))

    options = vars(args)
    config.update(**options)
    config.update({
        'metric': 'balacc',
        'type': 'classification',
        'wall_time': args.wall_time,
        'num_bag_sets': args.num_bag_sets,
        'num_bag_folds': args.num_bag_folds,
        'num_stack_levels': args.num_stacking_layers-1,
        'epochs': args.epochs,
        'experiment_name': 'autogluon_original_stacking'
    })

    # Run the example -- and also warn the user about autogluon settings
    log.warning(f"Autogluon does not accept a seed. Also, the cores are taken automatically "
                f"from the system, and in this case {psutil.cpu_count()} cores are used.")
    predictions, probabilities, truth, predictor = run(config)

    # Store the predictions if things go south
    with open(os.path.join(exp_dir, f"predictions.{args.task_id}.pickle"), 'wb') as handle:
        pickle.dump(predictions, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(os.path.join(exp_dir, f"truth.{args.task_id}.pickle"), 'wb') as handle:
        pickle.dump(truth, handle, protocol=pickle.HIGHEST_PROTOCOL)

    predictor.save()

    try:
        score = balanced_accuracy_score(truth, predictions)
    except ValueError:
        # Autogluon predictions have unkown data type. Align to the dtype of the train
        # data
        from sklearn import preprocessing
        le = preprocessing.LabelEncoder()
        if isinstance(truth, pd.Series):
            truth = pd.Series(truth, dtype=config['train'][config['label']].dtype)
            predictions = pd.Series(predictions, dtype=config['train'][config['label']].dtype)
        le.fit(config['train'][config['label']])
        score = balanced_accuracy_score(le.transform(truth), le.transform(predictions))

    log.info(f"Trained AutoGluon on task {args.task_id} resulted in score {score}")

    # save score to a file, just in case!
    config.pop('train')
    config.pop('test')
    config['score'] = score
    task_csv_dir = os.path.join(
        exp_dir,
        'results.csv',
    )
    pd.DataFrame([config]).to_csv(
        task_csv_dir,
    )

    # Exit with a success status!
    exit(0)
