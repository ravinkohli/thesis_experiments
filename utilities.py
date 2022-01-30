from argparse import Namespace
import typing

import dask.distributed

import openml

from sklearn.model_selection import train_test_split

from autoPyTorch.optimizer.utils import autoPyTorchSMBO
from autoPyTorch.datasets.resampling_strategy import HoldoutValTypes
from autoPyTorch.ensemble.utils import EnsembleSelectionTypes
# from autoPyTorch.datasets.resampling_strategy import RepeatedCrossValTypes

from smac.intensification.simple_intensifier import SimpleIntensifier
from smac.runhistory.runhistory2epm import RunHistory2EPM4LogCost
from smac.scenario.scenario import Scenario
from smac.facade.smac_ac_facade import SMAC4AC


def get_data(
        task_id: int,
        test_size: float = 0.2,
        seed: int = 11,
):
    """
    Args:
    _____
        task_id: int
            The id of the task which will be used for the run.
        val_share: float
            The validation split size from the train set.
        test_size: float
            The test split size from the whole dataset.
        seed: int
            The seed used for the dataset preparation.
    Returns:
    ________
    X_train, X_test, y_train, y_test, resampling_strategy_args, categorical indicator: tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray, dict, np.ndarray]
        The train examples, the test examples, the train labels, the test labels, the resampling strategy to be used and the categorical indicator for the features.
    """
    task = openml.tasks.get_task(task_id=task_id)
    dataset = task.get_dataset()
    X, y, categorical_indicator, _ = dataset.get_data(
        dataset_format='dataframe',
        target=dataset.default_target_attribute,
    )

    # AutoPyTorch fails when it is given a y DataFrame with False and True values and category as dtype.
    # in its inner workings it uses sklearn which cannot detect the column type.
    if isinstance(y[1], bool):
        y = y.astype('bool')

    # uncomment only for np.arrays

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=seed,
        stratify=y,
    )

    return X_train, X_test, y_train, y_test, categorical_indicator


def get_experiment_args(experiment_name: str = 'ensemble_bayesian_learning'):
    EXPERIMENT_ARGS = {
        'ensemble_bayesian_learning':
            (
                {
                    'resampling_strategy': HoldoutValTypes.stratified_holdout_validation,
                    'resampling_strategy_args': None,
                    'ensemble_method': EnsembleSelectionTypes.stacking_ensemble,
                    'ensemble_size': 5,
                },
                {
                }
            )
        ,
        # 'stacked_ensemble':{
        #     'resampling_strategy': RepeatedCrossValTypes.repeated_k_fold_cross_validation,
        #     'resampling_strategy_args': None,
        #     'ensemble_method': EnsembleSelectionTypes.stacking_ensemble,
        #     'ensemble_size': 5,
        #     'num_stacking_layers': 2,
        #     'smbo_class': autoPyTorchSMBO
        # },
        'development':(
                {
                'resampling_strategy': HoldoutValTypes.stratified_holdout_validation,
                'resampling_strategy_args': None,
                'ensemble_method': EnsembleSelectionTypes.ensemble_selection,
                'ensemble_size': 5,
                'num_stacking_layers': None,
                },
            {
            }
        )
    }
    return EXPERIMENT_ARGS[experiment_name]


def get_smac_object(
    scenario_dict: typing.Dict[str, typing.Any],
    seed: int,
    ta: typing.Callable,
    ta_kwargs: typing.Dict[str, typing.Any],
    n_jobs: int,
    initial_budget: int,
    max_budget: int,
    initial_configurations,
    dask_client: typing.Optional[dask.distributed.Client],
) -> SMAC4AC:
    """
    This function returns an SMAC object that is gonna be used as
    optimizer of pipelines
    Args:
    _____
        scenario_dict (typing.Dict[str, typing.Any]): constrain on how to run
            the jobs
        seed (int): to make the job deterministic
        ta (typing.Callable): the function to be intensifier by smac
        ta_kwargs (typing.Dict[str, typing.Any]): Arguments to the above ta
        n_jobs (int): Amount of cores to use for this task
        dask_client (dask.distributed.Client): User provided scheduler
    Returns:
    ________
        (SMAC4AC): sequential model algorithm configuration object
    """
    rh2EPM = RunHistory2EPM4LogCost
    return SMAC4AC(
        scenario=Scenario(scenario_dict),
        rng=seed,
        runhistory2epm=rh2EPM,
        tae_runner=ta,
        tae_runner_kwargs=ta_kwargs,
        initial_configurations=None,
        run_id=seed,
        intensifier=SimpleIntensifier,
        dask_client=dask_client,
        n_jobs=n_jobs,
    )


def get_updates_for_regularization_cocktails(
    args: Namespace,
):
    """
    These updates mimic the regularization cocktail paper.

    Args:
    _____
        categorical_indicator: np.ndarray
            An array that indicates whether a feature is categorical or not.
        args: Namespace,
            The different updates for the setup of the run, mostly updates
            for the different regularization ingredients.
    Returns:
    ________
    pipeline_update, search_space_updates, include_updates - Tuple[dict, HyperparameterSearchSpaceUpdates, dict]
        The pipeline updates like number of epochs, budget, seed etc.
        The search space updates like setting different hps to different values or ranges.
        Lastly include updates, which can be used to include different features.
    """
    # No early stopping and train on gpu
    pipeline_update = {
        'early_stopping': -1,
        'min_epochs': args.epochs,
        'epochs': args.epochs,
        "device": 'cpu',
        'torch_num_threads': 2
    }

    return pipeline_update
