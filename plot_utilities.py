
from datetime import datetime
import os
import seaborn as sns
from tkinter.tix import Tree
from typing import Dict, NamedTuple
from autoPyTorch.utils.results_visualizer import PlotSettingParams
from autoPyTorch.utils.results_visualizer import ResultsVisualizer, _get_perf_and_time
from autoPyTorch import metrics
from autoPyTorch.utils.results_manager import MetricResults
from autoPyTorch.utils.results_visualizer import ColorLabelSettings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
# from path import Path


class StoreResults(NamedTuple):
    results: MetricResults
    colors: Dict
    labels: Dict
    plot_setting_params: PlotSettingParams

def interpolate_time(incumbents, costs):
    df_dict = {}

    for i, _ in enumerate(incumbents):
        _seed_info = pd.Series(incumbents[i], index=costs[i])
        df_dict[f"seed{i}"] = _seed_info
    df = pd.DataFrame.from_dict(df_dict)

    df = df.fillna(method="backfill", axis=0).fillna(method="ffill", axis=0)
    return df

def incumbent_plot(
    ax,
    x,
    y,
    name_to_label,
    color_marker,
    xlabel=None,
    ylabel=None,
    title=None,
    strategy=None,
    log=False,
    **plot_kwargs,
):
    if isinstance(x, list):
        x = np.array(x)
    if isinstance(y, list):
        y = np.array(y)

    df = interpolate_time(incumbents=y, costs=x)
    df = df.iloc[np.linspace(0, len(df) - 1, 1001)]
    x = df.index
    y_mean = df.mean(axis=1)
    std_error = stats.sem(df.values, axis=1)

    ax.plot(
        x,
        y_mean,
        label=name_to_label[strategy],
        **plot_kwargs,
        color=color_marker[strategy],
        linewidth=0.7
    )

    ax.fill_between(
        x,
        y_mean - std_error,
        y_mean + std_error,
        color=color_marker[strategy],
        alpha=0.2,
    )

    if title is not None:
        ax.set_title(title, fontsize=18) # [title])
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=18)
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=18)
    ax.grid(True, which="both", ls="-", alpha=0.8)

    ax.tick_params(axis='both', which='major', labelsize=18)

    if log:
        ax.set_xscale("log")
        # ax.set_yscale("log")


def save_fig(fig, filename, output_dir, dpi: int = 100):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    fig.savefig(os.path.join(output_dir, f"{filename}.pdf"), bbox_inches="tight", dpi=dpi)
    print(f'Saved to "{output_dir}/{filename}.pdf"')


def set_general_plot_style():
    sns.set_style("ticks")
    sns.set_context("paper")
    sns.set_palette("deep")
    plt.switch_backend("pgf")
    plt.rcParams.update(
        {
            "text.usetex": True,
            "pgf.texsystem": "pdflatex",
            "pgf.rcfonts": False,
            "font.family": "serif",
            "font.serif": [],
            "font.sans-serif": [],
            "font.monospace": [],
            "font.size": "10.90",
            "legend.fontsize": "9.90",
            "xtick.labelsize": "small",
            "ytick.labelsize": "small",
            "legend.title_fontsize": "small",
            # "bottomlabel.weight": "normal",
            # "toplabel.weight": "normal",
            # "leftlabel.weight": "normal",
            # "tick.labelweight": "normal",
            # "title.weight": "normal",
            "pgf.preamble": r"""
                \usepackage[T1]{fontenc}
                \usepackage[utf8x]{inputenc}
                \usepackage{microtype}
            """,
        }
    )



def replace_name(task_id):
    dataset_df = pd.read_csv('dataset_collection.csv')
    name = dataset_df[dataset_df['OpenML Task Id'] == int(task_id)]['Dataset Name'].item()
    return name


def make_overfit_plot(out_dir, strategies, name_to_label, color_marker, best_test=True):
    if best_test:
        overfit_df = pd.read_csv('final_thesis_results/ensemble_size_5/all/combined_results_mean_test_all_overfit.csv').set_index('Dataset')
        not_needed_column_names = [column_name for column_name in overfit_df.columns if column_name not in strategies]
            # not_needed_column_names.pop('task_id')
            
        # print(strategies, "\n", not_needed_column_names)
        overfit_df = overfit_df.drop(not_needed_column_names, axis=1)
        overfit_df.columns = [name_to_label[column_name]  for column_name in overfit_df.columns]
        overfit_df = overfit_df.reset_index()
        # overfit_df = overfit_df[overfit_df['task_id'] != 168910]
        # overfit_df['Dataset'] = list(map(replace_name, overfit_df['task_id']))
        # overfit_df = overfit_df.drop(['task_id'], axis=1)
    else:
        combined_results = {}
        for dataset in ['train', 'test']:
            combined_results[dataset] = pd.read_csv(os.path.join(out_dir, f'combined_results_mean_{dataset}.csv'))
        overfit_df = (combined_results['test'] - combined_results['train'])
        overfit_df['task_id'] = combined_results['train']['task_id']
        not_needed_column_names = [column_name for column_name in overfit_df.columns if column_name.replace('_mean', '') not in strategies and column_name != 'task_id' and column_name in overfit_df.columns]
            # not_needed_column_names.pop('task_id')
            
        print(strategies, "\n", not_needed_column_names)
        overfit_df = overfit_df.drop(not_needed_column_names, axis=1)
        overfit_df.columns = [name_to_label[column_name.replace('_mean', '')] if column_name != 'task_id' else column_name for column_name in overfit_df.columns]
        overfit_df = overfit_df[overfit_df['task_id'] != 168910]
        overfit_df['Dataset'] = list(map(replace_name, overfit_df['task_id']))
        overfit_df = overfit_df.drop(['task_id'], axis=1)

    figsize=(21, 16)
    markersize = 300
    ax = overfit_df.plot.scatter(
            x=name_to_label[strategies[0]],
            y='Dataset',
            label=name_to_label[strategies[0]],
            yticks=(overfit_df['Dataset']),
            marker='*',
            figsize=figsize,
            c=color_marker[strategies[0]],
            s=markersize)

    for i, strategy in enumerate(strategies):
        if i==0:
            continue
        ax = overfit_df.plot.scatter(
                            x=name_to_label[strategy],
                            y='Dataset',
                            label=name_to_label[strategy],
                            yticks=(overfit_df['Dataset']),
                            marker='*',
                            figsize=figsize,
                            c=color_marker[strategy],
                            ax=ax,
                            s=markersize
                        )
    ax.axvline(x=0, color='black', alpha=0.5, linestyle='--')
    ax.set_xlabel('Best ever test score - test score [%]')
    ax.set_ylabel('Dataset')
    minmax_df = overfit_df.drop(['Dataset'], axis=1).to_numpy()
    print(overfit_df.head())
    print(minmax_df.min(), minmax_df.max()) # np.arange(minmax_df.min(), minmax_df.max(), 2))
    ax.set_xticks(np.arange(np.floor(minmax_df.min()), np.ceil(minmax_df.max()), 0.5), minor=True)
    ax.grid(which='major', alpha=0.7)
    ax.grid(which='minor', alpha=0.4)
    fig = ax.get_figure()
    fig.savefig(os.path.join(out_dir, f'combined_results_overfit.png'))
    plt.close(fig)
    overfit_df.to_csv(os.path.join(out_dir, f'combined_results_overfit.csv'))


from dataset_collection import medium_task_ids, small_task_ids

IGNORE_TASKS = [146606, 168868]
SIZE_11_IGNORE_TASKS = [168909, 146825]

def test_method(df_method:  pd.Series, values):
    bool_mask = []
    values = values.copy()
    for method in df_method.items():
        this_mask = []
        for val in values:
            this_mask.append(val == method[1])
        bool_mask.append(this_mask)
    return bool_mask

def task_bool_mask(df_task:  pd.Series, benchmark=None, size=5):
    ignore_task_ids = []
    if benchmark is not None:
        if benchmark == 'small':
            ignore_task_ids = medium_task_ids
        elif benchmark == 'medium':
            ignore_task_ids = small_task_ids
    ignore_task_ids.extend(IGNORE_TASKS)
    if size == 11:
        ignore_task_ids.extend(SIZE_11_IGNORE_TASKS)

    print(f"Ignored task ids: {ignore_task_ids}")
    bool_mask = []
    for task in df_task.items():
        bool_mask.append(all(val != task[1] for val in ignore_task_ids))
    return bool_mask



# for strategy, item in data.items():
#     for task, item_2 in item.items():
#         if 106 in item_2 and 'ensemble_history' in item_2[106]:
#             if task not in max_budget:
#                 max_budget[task] = 0
#             time =np.array(list(item_2[106]['ensemble_history']['Timestamp'].values()))
#             time -= time[0]
#             max_time = max(time)/1000
#             if max_time > max_budget[task]:
#                 max_budget[task] = max_time


# new_data = {}
# min_max = {}
# i = 0
# j = 0
# for strategy in data:
#     # if 'stacking' not in strategy and 'repeats' not in strategy:
#     new_data[strategy] = {}
#     for task in data[strategy]:
#         if task not in min_max:
#             min_max[task] = []
#         new_data[strategy][task] = {}
#         for seed in data[strategy][task]:
#             if 'ensemble_history' in data[strategy][task][seed]:
#                 new_data[strategy][task][seed] = {}
#                 new_data[strategy][task][seed]['loss'] = data[strategy][task][seed]['ensemble_history']['test_balanced_accuracy']
#                 time = data[strategy][task][seed]['ensemble_history']['Timestamp']
#                 j += 1
#                 try:
#                     initial_time = datetime.fromtimestamp(time[0])
#                     final_time = datetime.fromtimestamp(time[-1])
#                     # print("\n", final_time - initial_time)
#                     min_max[task].append((max(time) - min(time)))
#                     new_data[strategy][task][seed]['time'] = time - time[0]
#                 except:
#                     i+= 1
#             break

# import pickle
# with open('final_thesis_results/ensemble_size_5/task_id_to_performance_fixed.pkl', 'wb') as fp:
#     pickle.dump(new_data, fp)


# for task in min_max:
#     print(task, max(min_max[task]))


# '146212','12','7592','146822','53','9981','14965','168911','3','168331','146825','146818','168330','146195','168335','168909','168912','10101','9952','167120','168910','146821','3917','31','168908','9977','167119','168329','9977','9981','168912','146195','146818','31','3917','168908','53','167120','168335','168909','146822','168910','168331','10101','168329','146821','9952','146212','12','7592','3','168911','168330','146825','167119','14965','167120','9981','9952','168331','168330','168910','168329','146821','146822','3917','31','14965','168908','168911','9977','168909','10101','146195','53','146212','7592','3','146825','146818','168912','168335','12','167119','9977','167120','168910','168909','168329','168331','3917','146818','14965','167119','53','146606','168335','168868','31','12','168330','168912','146821','146822','9981','7592','168908','10101','9952','3','168911','146212','146195','146825','3917','168909','7592','168912','9981','9977','12','14965','146195','146606','167120','146825','167119','146818','31','3','168908','168910','168330','168868','168331','53','146212','9952','146822','168329','168911','146821','10101','168335','9977','3','7592','31','168912','168909','12','168331','168908','146195','168330','146818','146822','9952','168329','168911','168910','167120','53','168335','167119','146821','3917','14965','10101','9981','146212','146825','146195','3917','12','10101','168909','167120','167119','14965','168330','168329','3','168911','146822','146212','53','31','146818','168908','9981','7592','146825','168335','146821','168331','9952','168910','9977','168912','146195','146821','31','9981','9977','7592','168909','146818','168329','10101','168331','167120','3917','146822','12','168908','53','14965','168912','168330','3','168335','168910','167119','9952','146212','168911','146825','168331','146195','31','168911','146821','9977','14965','3917','146212','168912','168329','9952','146825','167119','9981','168330','168908','3','12','146818','167120','168910','53','168909','146822','10101','7592','168335','168331','168911','10101','167120','3917','168335','9977','146195','168910','146825','3','146821','53','168329','14965','167119','12','31','168330','9981','146818','168909','146212','168912','168908','7592','146822','9952','168329','3','146822','168909','168911','146818','9981','168335','168910','146195','146821','168908','31','168912','168330','9977','167120','146212','14965','167119','12','9952','168331','146825','10101','7592','53','3917','10101','12','146821','14965','167120','168912','168911','7592','168331','168335','168330','3917','146195','53','9977','168908','9952','168329','168909','168910','146822','167119','31','3','146818','9981','146212','146195','168329','168330','146822','168335','167119','14965','3','168909','9981','146825','146818','167120','168911','168908','9977','7592','146212','3917','168331','12','53','9952','168910','146821','168912','31','10101','167120','146822','167119','168912','7592','146821','146195','3917','168911','31','146825','14965','12','146818','9952','168331','168909','168910','9981','168335','168908','53','10101','3','168330','146212','168329','9977','9977','146825','168911','146821','7592','167120','168331','168330','168909','168910','53','146822','168329','168908','146212','9952','168335','10101','9981','3','12','3917','167119','146818','168912','146195','31','14965'

# {'ensemble_iterative_hpo_enable_traditional_pipeline_True_warmstart_True_posthoc_ensemble_fit_False_use_ensemble_opt_loss_False', 'ensemble_selection_enable_traditional_pipeline_False_warmstart_False_posthoc_ensemble_fit_False_use_ensemble_opt_loss_False', 'ensemble_iterative_hpo_enable_traditional_pipeline_False_warmstart_True_posthoc_ensemble_fit_True_use_ensemble_opt_loss_False', 'ensemble_iterative_hpo_enable_traditional_pipeline_False_warmstart_False_posthoc_ensemble_fit_False_use_ensemble_opt_loss_False', 'ensemble_bayesian_optimisation_enable_traditional_pipeline_False_warmstart_False_posthoc_ensemble_fit_False_use_ensemble_opt_loss_False', 'ensemble_iterative_hpo_enable_traditional_pipeline_False_warmstart_False_posthoc_ensemble_fit_True_use_ensemble_opt_loss_False', 'ensemble_bayesian_optimisation_enable_traditional_pipeline_True_warmstart_False_posthoc_ensemble_fit_True_use_ensemble_opt_loss_False', 'ensemble_iterative_hpo_enable_traditional_pipeline_True_warmstart_False_posthoc_ensemble_fit_True_use_ensemble_opt_loss_False', 'ensemble_bayesian_optimisation_enable_traditional_pipeline_False_warmstart_False_posthoc_ensemble_fit_False_use_ensemble_opt_loss_True', 'ensemble_bayesian_optimisation_enable_traditional_pipeline_False_warmstart_False_posthoc_ensemble_fit_True_use_ensemble_opt_loss_True', 'ensemble_bayesian_optimisation_enable_traditional_pipeline_True_warmstart_False_posthoc_ensemble_fit_True_use_ensemble_opt_loss_True', 'ensemble_iterative_hpo_enable_traditional_pipeline_False_warmstart_True_posthoc_ensemble_fit_False_use_ensemble_opt_loss_False', 'ensemble_iterative_hpo_enable_traditional_pipeline_True_warmstart_True_posthoc_ensemble_fit_True_use_ensemble_opt_loss_False', 'ensemble_bayesian_optimisation_enable_traditional_pipeline_False_warmstart_False_posthoc_ensemble_fit_True_use_ensemble_opt_loss_False', 'ensemble_selection_enable_traditional_pipeline_True_warmstart_False_posthoc_ensemble_fit_False_use_ensemble_opt_loss_False'}

ebo_1 = {
        "strategies": [
            # 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1',
            # 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1',
            # 'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1',
            # 'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2',
            # 'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2',
            # 'es_pef_F_etp_F_ueol_F_w_F_nsl_1',
            # 'es_pef_F_etp_T_ueol_F_w_F_nsl_1',
            # 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1',
            # 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1',
            # 'eih_pef_T_etp_F_ueol_F_w_T_nsl_1',
            'eih_pef_T_etp_T_ueol_F_w_T_nsl_1',
            # 'eih_pef_F_etp_F_ueol_F_w_T_nsl_1',
            # 'eih_pef_F_etp_T_ueol_F_w_T_nsl_1',
            # 'eih_pef_F_etp_F_ueol_F_w_F_nsl_1',
            # 'ebo_pef_F_etp_F_ueol_T_w_F_nsl_1',
            # 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1',
            # 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1',
            # 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2',
            # 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2',
            # 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2',
            # 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2',
            # 'sespl_pef_F_etp_F_ueol_F_w_F_nsl_2',
            # 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2',
            # 'sespl_pef_F_etp_T_ueol_F_w_F_nsl_2',
            # 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2',
            # 'eihr_pef_T_etp_F_ueol_F_w_T_nsl_2',
            # 'eihs_pef_T_etp_F_ueol_F_w_T_nsl_2',
            # 'eihs_pef_T_etp_T_ueol_F_w_T_nsl_2',
            'eihr_pef_T_etp_T_ueol_F_w_T_nsl_2',
            # 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2',
            # 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2',
            # 'sft_pef_T_etp_F_ueol_F_w_F_nsl_2',
            # 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2',
            # 'sft_pef_T_etp_T_ueol_F_w_F_nsl_2',
            # 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2',
            # 'sft_pef_F_etp_F_ueol_F_w_F_nsl_2',
            # 'eihr_pef_F_etp_F_ueol_F_w_T_nsl_2',
            'eihs_pef_F_etp_F_ueol_F_w_T_nsl_2',
            # 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2'
        ],
    "NAME_TO_LABEL": {
        'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1': 'EBO (Post-hoc + Trad.)',
        'ebor_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post-hoc + Trad. + RBM)',
        'ebos_pef_T_etp_T_ueol_F_w_F_nsl_2': 'EBO (Post-hocs + Trad. + RBS)' ,
    # 'ebo_pef_F_etp_F_ueol_F_w_F_nsl_1': 'EBO ',
    # 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1': 'EBO (post-hoc ensemble)', 
    }
}