import argparse
import json
import os
import random
import time
import warnings
import shutil
import sys


os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'


warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
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
    '--mem_limit',
    type=int,
    default=8000,
)
parser.add_argument(
    '--func_eval_time',
    type=int,
    default=500,
)
parser.add_argument(
    '--min_epochs',
    type=int,
    default=12,
)
parser.add_argument(
    '--epochs',
    type=int,
    default=50,
)
parser.add_argument(
    '--seed',
    type=int,
    default=11,
)
parser.add_argument(
    '--splits',
    type=int,
    default=3,
)
parser.add_argument(
    '--repeats',
    type=int,
    default=2,
)
parser.add_argument(
    '--exp_dir',
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
parser.add_argument(
    '--use_ensemble_opt_loss',
    type=str2bool,
    default=False
)
parser.add_argument(
    '--num_stacking_layers',
    type=int,
    default=1
)
parser.add_argument(
    '--ensemble_size',
    type=int,
    default=7
)
parser.add_argument(
    '--posthoc_ensemble_fit',
    type=str2bool,
    default=False
)
parser.add_argument(
    '--warmstart',
    type=str2bool,
    default=False
)
parser.add_argument(
    '--enable_traditional_pipeline',
    type=str2bool,
    default=False
)
parser.add_argument(
    '--dataset_compression',
    help='whether to use search space updates from the reg cocktails paper',
    type=str2bool,
    default=False,
)
args = parser.parse_args()
options = vars(args)
print(options)



if __name__ == '__main__':
    import torch

    from autoPyTorch.api.tabular_classification import TabularClassificationTask
    from autoPyTorch.api.utils import get_autogluon_default_nn_config

    import numpy as np
    from utilities import (
        get_data,
        get_smac_object,
        get_experiment_args,
        get_updates_for_regularization_cocktails,
        get_compression_args
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
    X_train, X_test, y_train, y_test, categorical_indicator, dataset_name, feat_type = get_data(
        task_id=args.task_id,
    )

    output_dir = os.path.expanduser(
        os.path.join(
            args.exp_dir,
            f'out',
        )
    )
    temp_dir = os.path.expanduser(
        os.path.join(
            args.exp_dir,
            f'tmp',
        )
    )
    search_space_updates = get_autogluon_default_nn_config(feat_types=feat_type)
    init_args, search_args = get_experiment_args(
        args.experiment_name,
        splits=args.splits,
        repeats=args.repeats,
        use_ensemble_opt_loss=args.use_ensemble_opt_loss,
        num_stacking_layers=args.num_stacking_layers,
        ensemble_size=args.ensemble_size,
        posthoc_ensemble_fit=args.posthoc_ensemble_fit,
        enable_traditional_pipeline=args.enable_traditional_pipeline,
    )
    print(f"init_args: {init_args}, search_args: {search_args}")
    ############################################################################
    # Build and fit a classifier
    # ==========================


    api = TabularClassificationTask(
        temporary_directory=temp_dir,
        output_directory=output_dir,
        delete_tmp_folder_after_terminate=False,
        delete_output_folder_after_terminate=False,
        seed=args.seed,
        search_space_updates=search_space_updates,
        **init_args
    )

    ############################################################################
    # Search for the best hp configuration
    # =====================================================

    pipeline_config = get_updates_for_regularization_cocktails(args)
    api.set_pipeline_config(**pipeline_config)

    search_func = search_args.pop('search_func', 'search')
    common_args = dict(
        X_train=X_train.copy(),
        y_train=y_train.copy(),
        X_test=X_test.copy(),
        y_test=y_test.copy(),
        feat_types=feat_type,
        dataset_name=dataset_name,
        optimize_metric='balanced_accuracy',
        total_walltime_limit=args.wall_time,
        memory_limit=args.mem_limit,
        func_eval_time_limit_secs=args.func_eval_time,
        max_budget=args.epochs,
        all_supported_metrics=False,
        dataset_compression=get_compression_args() if args.dataset_compression else False,
        **search_args
    )

    search_func_args = dict(
        get_smac_object_callback=get_smac_object,
        smac_scenario_args={
            'runcount_limit': 1000,
        },
        min_budget=args.min_epochs,
        warmstart=args.warmstart
        )
    if search_func in ["search", "run_iterative_hpo_ensemble_optimisation"]:
        common_args.update(search_func_args)
    getattr(api, search_func)(**common_args)

    train_preds = api.predict(X_train)
    test_preds = api.predict(X_test)
    train_score = api.score(train_preds, y_train)
    test_score = api.score(test_preds, y_test)
    duration = time.time() - start_time

    print(f'Final Train Balanced accuracy: {train_score}')
    print(f'Final Test Balanced accuracy: {test_score}')
    print(f'Time taken: {duration}')

    result_dict = {
        'train balanced accuracy': list(train_score.values())[-1],
        'test balanced accuracy': list(test_score.values())[-1],
        'task_id': args.task_id,
        'duration': duration,
        'dataset_name': dataset_name,
        **options
    }

    with open(os.path.join(args.exp_dir, 'final_result.json'), 'w') as file:
        json.dump(result_dict, file)
    
    # delete all runs
    shutil.rmtree(api._backend.get_runs_directory())

    # archive tmp folder
    shutil.make_archive(os.path.join(os.path.dirname(api._backend.temporary_directory), 'tmp'), 'zip', api._backend.temporary_directory)
    shutil.rmtree(api._backend.temporary_directory)
