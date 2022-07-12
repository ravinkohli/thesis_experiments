from argparse import Namespace
from typing import Any, Callable, Dict, List, Optional

from ConfigSpace.configuration_space import Configuration

import dask.distributed

import openml

from smac.runhistory.runhistory2epm import RunHistory2EPM4LogCost
from smac.scenario.scenario import Scenario
from smac.facade.smac_ac_facade import SMAC4AC
from smac.intensification.hyperband import Hyperband
from smac.optimizer.smbo import SMBO

from autoPyTorch.optimizer.utils import autoPyTorchSMBO
from autoPyTorch.datasets.resampling_strategy import RepeatedCrossValTypes
from autoPyTorch.ensemble.utils import BaseLayerEnsembleSelectionTypes, StackingEnsembleSelectionTypes


def get_compression_args():
    return {'memory_allocation': 0.02, 'methods': ['precision', 'subsample']}


def get_data(
        task_id: int,
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

    train_indices, test_indices = task.get_train_test_split_indices()

    # uncomment only for np.arrays

    X_train = X.iloc[train_indices]
    y_train = y.iloc[train_indices]
    X_test = X.iloc[test_indices]
    y_test = y.iloc[test_indices]

    feat_type = ["numerical" if not indicator else "categorical" for indicator in categorical_indicator]

    return X_train, X_test, y_train, y_test, categorical_indicator, dataset.name, feat_type


def get_experiment_args(
    experiment_name: str = 'ensemble_bayesian_optimisation',
    splits: int = 5,
    repeats: int = 2,
    use_ensemble_opt_loss: bool = False,
    num_stacking_layers: int = 1,
    ensemble_size: int = 7,
    posthoc_ensemble_fit: bool = False,
    enable_traditional_pipeline: bool = False
):
    EXPERIMENT_ARGS = _get_experiment_args(splits, repeats, use_ensemble_opt_loss, num_stacking_layers, ensemble_size, posthoc_ensemble_fit, enable_traditional_pipeline)
    return EXPERIMENT_ARGS[experiment_name]

def _get_experiment_args(
    splits: int = 5,
    repeats: int = 2,
    use_ensemble_opt_loss: bool = False,
    num_stacking_layers: int = 1,
    ensemble_size: int = 7,
    posthoc_ensemble_fit: bool = False,
    enable_traditional_pipeline: bool = False
):
    EXPERIMENT_ARGS = {
        'ensemble_bayesian_optimisation':
            (
                {
                    'resampling_strategy': RepeatedCrossValTypes.stratified_repeated_k_fold_cross_validation,
                    'resampling_strategy_args': {'num_splits': splits, 'num_repeats': repeats},
                    'base_ensemble_method': BaseLayerEnsembleSelectionTypes.ensemble_bayesian_optimisation,
                    'ensemble_size': ensemble_size,
                    'num_stacking_layers': num_stacking_layers,
                },
                { 
                    'smbo_class': autoPyTorchSMBO,
                    'use_ensemble_opt_loss': use_ensemble_opt_loss,
                    'posthoc_ensemble_fit': posthoc_ensemble_fit,
                    'enable_traditional_pipeline': enable_traditional_pipeline
                }
            ),
        'ensemble_iterative_hpo':
            (
                {
                    'resampling_strategy': RepeatedCrossValTypes.stratified_repeated_k_fold_cross_validation,
                    'resampling_strategy_args': {'num_splits': splits, 'num_repeats': repeats},
                    'base_ensemble_method': BaseLayerEnsembleSelectionTypes.ensemble_iterative_hpo,
                    'ensemble_size': ensemble_size,
                    'num_stacking_layers': num_stacking_layers,
                },
                { 
                    'search_func': 'run_iterative_hpo_ensemble_optimisation',
                    'posthoc_ensemble_fit': posthoc_ensemble_fit,
                    'enable_traditional_pipeline': enable_traditional_pipeline
                }
            ),
        'ensemble_selection':
            (
                {
                    'resampling_strategy': RepeatedCrossValTypes.stratified_repeated_k_fold_cross_validation,
                    'resampling_strategy_args': {'num_splits': splits, 'num_repeats': repeats},
                    'base_ensemble_method': BaseLayerEnsembleSelectionTypes.ensemble_selection,
                    'ensemble_size': ensemble_size,
                },
                {
                    'enable_traditional_pipeline': enable_traditional_pipeline
                }
            ),
        'ensemble_bayesian_optimisation_stacking':
            (
                {
                    'resampling_strategy': RepeatedCrossValTypes.stratified_repeated_k_fold_cross_validation,
                    'resampling_strategy_args': {'num_splits': splits, 'num_repeats': repeats},
                    'base_ensemble_method': BaseLayerEnsembleSelectionTypes.ensemble_bayesian_optimisation,
                    'stacking_ensemble_method': StackingEnsembleSelectionTypes.stacking_ensemble_bayesian_optimisation,
                    'ensemble_size': ensemble_size,
                    'num_stacking_layers': num_stacking_layers,
                },
                { 
                    'smbo_class': autoPyTorchSMBO,
                    'use_ensemble_opt_loss': use_ensemble_opt_loss,
                    'posthoc_ensemble_fit': posthoc_ensemble_fit,
                    'enable_traditional_pipeline': enable_traditional_pipeline
                }
            ),
        'ensemble_iterative_hpo_stacking':
            (
                {
                    'resampling_strategy': RepeatedCrossValTypes.stratified_repeated_k_fold_cross_validation,
                    'resampling_strategy_args': {'num_splits': splits, 'num_repeats': repeats},
                    'base_ensemble_method': BaseLayerEnsembleSelectionTypes.ensemble_iterative_hpo,
                    'stacking_ensemble_method': StackingEnsembleSelectionTypes.stacking_ensemble_iterative_hpo,
                    'ensemble_size': ensemble_size,
                    'num_stacking_layers': num_stacking_layers,
                },
                { 
                    'search_func': 'run_iterative_hpo_ensemble_optimisation',
                    'posthoc_ensemble_fit': posthoc_ensemble_fit,
                    'enable_traditional_pipeline': enable_traditional_pipeline
                }
            ),
        'stacking_ensemble_selection_per_layer':
            (
                {
                    'resampling_strategy': RepeatedCrossValTypes.repeated_k_fold_cross_validation,
                    'resampling_strategy_args': {'num_splits': splits, 'num_repeats': repeats},
                    'base_ensemble_method': BaseLayerEnsembleSelectionTypes.ensemble_selection,
                    'stacking_ensemble_method': StackingEnsembleSelectionTypes.stacking_ensemble_selection_per_layer,
                    'ensemble_size': ensemble_size,
                    'num_stacking_layers': num_stacking_layers,
                },
                {
                    'enable_traditional_pipeline': enable_traditional_pipeline
                }
            ),
        'ensemble_bayesian_optimisation_repeats':
            (
                {
                    'resampling_strategy': RepeatedCrossValTypes.stratified_repeated_k_fold_cross_validation,
                    'resampling_strategy_args': {'num_splits': splits, 'num_repeats': repeats},
                    'base_ensemble_method': BaseLayerEnsembleSelectionTypes.ensemble_bayesian_optimisation,
                    'stacking_ensemble_method': StackingEnsembleSelectionTypes.stacking_repeat_models,
                    'ensemble_size': ensemble_size,
                    'num_stacking_layers': num_stacking_layers,
                },
                { 
                    'smbo_class': autoPyTorchSMBO,
                    'use_ensemble_opt_loss': use_ensemble_opt_loss,
                    'posthoc_ensemble_fit': posthoc_ensemble_fit,
                    'enable_traditional_pipeline': enable_traditional_pipeline
                }
            ),
        'ensemble_iterative_hpo_repeats':
            (
                {
                    'resampling_strategy': RepeatedCrossValTypes.stratified_repeated_k_fold_cross_validation,
                    'resampling_strategy_args': {'num_splits': splits, 'num_repeats': repeats},
                    'base_ensemble_method': BaseLayerEnsembleSelectionTypes.ensemble_iterative_hpo,
                    'stacking_ensemble_method': StackingEnsembleSelectionTypes.stacking_repeat_models,
                    'ensemble_size': ensemble_size,
                    'num_stacking_layers': num_stacking_layers,
                },
                { 
                    'smbo_class': autoPyTorchSMBO,
                    'posthoc_ensemble_fit': posthoc_ensemble_fit,
                    'enable_traditional_pipeline': enable_traditional_pipeline
                }
            ),
        'ensemble_selection_repeats':
            (
                {
                    'resampling_strategy': RepeatedCrossValTypes.stratified_repeated_k_fold_cross_validation,
                    'resampling_strategy_args': {'num_splits': splits, 'num_repeats': repeats},
                    'base_ensemble_method': BaseLayerEnsembleSelectionTypes.ensemble_selection,
                    'stacking_ensemble_method': StackingEnsembleSelectionTypes.stacking_repeat_models,
                    'ensemble_size': ensemble_size,
                },
                {
                    'enable_traditional_pipeline': enable_traditional_pipeline
                }
            ),
        'stacking_autogluon':
            (
                {
                    'resampling_strategy': RepeatedCrossValTypes.repeated_k_fold_cross_validation,
                    'resampling_strategy_args': {'num_splits': splits, 'num_repeats': repeats},
                    'base_ensemble_method': BaseLayerEnsembleSelectionTypes.ensemble_autogluon,
                    'stacking_ensemble_method': StackingEnsembleSelectionTypes.stacking_autogluon,
                    'ensemble_size': ensemble_size,
                    'num_stacking_layers': num_stacking_layers,
                },
                {
                    'search_func': 'run_autogluon_stacking'
                }
            ),
        }
        
    return EXPERIMENT_ARGS


def get_smac_object(
    scenario_dict: Dict[str, Any],
    seed: int,
    ta: Callable,
    ta_kwargs: Dict[str, Any],
    n_jobs: int,
    initial_budget: int,
    max_budget: int,
    dask_client: Optional[dask.distributed.Client],
    smbo_class: Optional[SMBO] = None,
    initial_configurations: Optional[List[Configuration]] = None,
) -> SMAC4AC:
    """
    This function returns an SMAC object that is gonna be used as
    optimizer of pipelines

    Args:
        scenario_dict (Dict[str, Any]): constrain on how to run
            the jobs
        seed (int): to make the job deterministic
        ta (Callable): the function to be intensifier by smac
        ta_kwargs (Dict[str, Any]): Arguments to the above ta
        n_jobs (int): Amount of cores to use for this task
        dask_client (dask.distributed.Client): User provided scheduler
        initial_configurations (List[Configuration]): List of initial
            configurations which smac will run before starting the search process

    Returns:
        (SMAC4AC): sequential model algorithm configuration object

    """
    intensifier = Hyperband

    rh2EPM = RunHistory2EPM4LogCost
    return SMAC4AC(
        scenario=Scenario(scenario_dict),
        rng=seed,
        runhistory2epm=rh2EPM,
        tae_runner=ta,
        tae_runner_kwargs=ta_kwargs,
        initial_configurations=initial_configurations,
        run_id=seed,
        intensifier=intensifier,
        intensifier_kwargs={'initial_budget': initial_budget, 'max_budget': max_budget,
                            'eta': 2, 'min_chall': 1, 'instance_order': 'shuffle_once'},
        dask_client=dask_client,
        n_jobs=n_jobs,
        smbo_class=smbo_class
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
    pipeline_update - dict
        The pipeline updates like number of epochs, budget, seed etc.
    """
    # No early stopping and train on cpu
    pipeline_update = {
        'early_stopping': 20,
        "device": 'cpu',
        'torch_num_threads': 1
    }

    return pipeline_update
