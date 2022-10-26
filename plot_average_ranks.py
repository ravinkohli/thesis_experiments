#!/usr/bin/env python3

import csv
import sys
import os

import numpy as np

import pandas as pd
import matplotlib.pyplot as plt

"""
Given pickle file containing ensemble curves for each experiment, task and seed, produce ensemble incumbent plot

Best techniques for 
EBO: PEF T, ETP T, UEOL F
iEBO: PEF T, ETP T, W T
ES ETP T
EBOS vs EBO vs EBOR  = EBO > EBOS > EBOR
iEBO vs iEBOS vs iEBOR = iEBOR > iEBOS > iEBO
ES vs ESS vs ESR = ESS > ES > ESR
iEBOR > ESS > EBO

"""

import os
import matplotlib.pyplot as plt
import numpy as np
from plot_utilities import incumbent_plot, incumbent_plot_with_lists, save_fig, set_general_plot_style
import seaborn as sns
from experiment_utils import SEEDS, TASKS, X_LABEL, X_MAP, Y_LABEL


def make_average_rank_plot(
    figure_output_dir,
    strategies,
    results,
    name_to_label,
    dataset,
    durations,
    eih_results
):
    # set_general_plot_style()

    all_trajectories = []
    strategy_names = []
    for strategy in strategies:
        # if strategy not in results:
        #         print(f"{strategy} not found")
        #         continue
        trajectories = []
        strategy_name = name_to_label[strategy]
        strategy_names.append(strategy_name)
        for task_index, task in enumerate(TASKS):


            losses = []
            times = []
            for seed in SEEDS:
                if task in results[strategy] and seed in results[strategy][task] and 'ensemble_history' in results[strategy][task][seed]:
                    
                    useful_results = results if 'eih' not in strategy else eih_results
                    raw_loss = np.array(list(useful_results[strategy][task][seed]['ensemble_history'][f'{dataset}_balanced_accuracy'].values()))
                    failed_losses = [i for i in range(len(raw_loss)) if raw_loss[i] is None]

                    time = np.array(list(useful_results[strategy][task][seed]['ensemble_history']['Timestamp'].values()))/1000
                    duration = durations[strategy][task][seed]['duration']
                    initial_time = time[-1] - duration
                    time = time - initial_time

                    raw_loss = np.delete(raw_loss, failed_losses)
                    min_raw_loss = min(raw_loss)
                    # if min_raw_loss < min_y:
                    #     min_y = min_raw_loss
                    raw_loss = np.append([0], raw_loss)
                    incumbent_loss = np.maximum.accumulate(raw_loss)
                    incumbent_time = np.delete(time, failed_losses)
                    # min_incumbent_time = min(incumbent_time)
                    # if min_incumbent_time < min_x:
                    #     min_x = min_incumbent_time
                    # max_incumbent_time = max(incumbent_time)
                    # if max_incumbent_time > max_x:
                    #     max_x = max_incumbent_time
                    incumbent_time = np.append([0], incumbent_time)
                    # losses[strategy].append(incumbent_loss)
                    # times[strategy].append(incumbent_time)
                    losses.append(incumbent_loss)
                    times.append(incumbent_time)
            # trajectory is the pd.Series object containing all seed runs of the
            # current model and current task.
            trajectory = fill_trajectory(losses, times)
            trajectories.append(trajectory)
        all_trajectories.append(trajectories)

    all_rankings = []
    n_iter = 500  # number of bootstrap samples to use for estimating the ranks.
    n_tasks = len(TASKS)

    for i in range(n_iter):
        pick = np.random.choice(all_trajectories[0][0].shape[1], size=(len(strategy_names)))
        # print(pick)
        for j in range(n_tasks):
            all_trajectories_tmp = pd.DataFrame(
                {
                    strategy_names[k]: at[j].iloc[:, pick[k]]
                    for k, at in enumerate(all_trajectories)
                }
            )
            all_trajectories_tmp = all_trajectories_tmp.fillna(method="ffill", axis=0)
            r_tmp = all_trajectories_tmp.rank(axis=1)
            all_rankings.append(r_tmp)

    # print(all_rankings[0])
    final_ranks = []
    for i, model in enumerate(strategy_names):
        # model = [key for key, value in name_to_label.items() if value == model][0]
        # print(model)
        ranks_for_model = []
        for ranking in all_rankings:
            # print(ranking.columns)
            ranks_for_model.append(ranking.loc[:, model])
        ranks_for_model = pd.DataFrame(ranks_for_model)
        ranks_for_model = ranks_for_model.fillna(method="ffill", axis=1)
        final_ranks.append(ranks_for_model.mean(skipna=True))

    # Step 3. Plot the average ranks over time.
    #####################################################################################
    for i, model in enumerate(strategy_names):
        X_data = []
        y_data = []
        for x, y in final_ranks[i].iteritems():
            X_data.append(x)
            y_data.append(y)
        # X_data.append(max_runtime)
        # y_data.append(y)
        plt.plot(X_data, y_data, label=model)
        plt.xlabel("time [sec]")
        plt.ylabel("average rank")
        plt.legend()
        plt.xscale("log")

    if not os.path.exists(figure_output_dir):
        os.makedirs(figure_output_dir)
    plt.savefig(os.path.join(figure_output_dir,"average_ranks_over_time.png"))


def fill_trajectory(performance_list, time_list):
    # Create n series objects.
    series_list = []
    for n in range(len(time_list)):
        series_list.append(pd.Series(data=performance_list[n], index=time_list[n]))

    # Concatenate to one Series with NaN vales.
    series = pd.concat(series_list, axis=1)

    # Fill missing performance values (NaNs) with last non-NaN value.
    series = series.fillna(method="ffill")

    # return the trajectories over seeds (series object)
    return series
