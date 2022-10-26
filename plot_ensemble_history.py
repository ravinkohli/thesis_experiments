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
from experiment_utils import SEEDS, TASKS, X_LABEL, Y_MAP, Y_LABEL


def make_incumbent_plot(
    figure_output_dir,
    dataset_info,
    strategies,
    results,
    name_to_label,
    dataset,
    color_marker,
    durations,
    eih_results,
    experiment_set
):

    trajectories = []
    for task_index, task in enumerate(TASKS):
        strategies_dict = {}
        strategy_names = []
        set_general_plot_style()

        dataset_name = dataset_info[dataset_info['OpenML Task Id'] == task]['Dataset Name'].item()
        fig, axs = plt.subplots(
            1,
            figsize=(5, 3),

        )
        # losses = {}
        # times = {}

        min_x = np.inf
        max_x = -np.inf
        all_losses = []
        all_times = []
        for strategy in strategies:
            if strategy not in results:
                print(f"{strategy} not found")
                continue
            strategy_name = name_to_label[strategy]
            strategies_dict[strategy_name] = {}
            strategy_names.append(strategy_name)
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
                    # min_raw_loss = min(raw_loss)
                    # if min_raw_loss < min_y:
                    #     min_y = min_raw_loss
                    raw_loss = np.append([0], raw_loss)
                    incumbent_loss = np.maximum.accumulate(raw_loss)
                    incumbent_time = np.delete(time, failed_losses)
                    min_incumbent_time = min(incumbent_time)
                    if min_incumbent_time < min_x:
                        min_x = min_incumbent_time
                    max_incumbent_time = max(incumbent_time)
                    if max_incumbent_time > max_x:
                        max_x = max_incumbent_time
                    incumbent_time = np.append([0], incumbent_time)

                    # losses[strategy].append(incumbent_loss)
                    # times[strategy].append(incumbent_time)
                    losses.append(incumbent_loss)
                    times.append(incumbent_time)

            all_losses.append(losses)
            all_times.append(times)

            df = incumbent_plot(
                ax=axs,
                x=times,
                y=losses,
                name_to_label=name_to_label,
                color_marker=color_marker,
                title=dataset_name,
                xlabel=X_LABEL,
                ylabel=f"{dataset[0].replace('t', 'T')}{dataset[1:]} {Y_LABEL}",
                strategy=strategy,
                log=True,
            )

        # df = incumbent_plot_with_lists(
        #         ax=axs,
        #         times=times,
        #         losses=losses,
        #         name_to_label=name_to_label,
        #         color_marker=color_marker,
        #     )

        # title=dataset_name
        # xlabel=X_LABEL
        # ylabel=f"{dataset[0].replace('t', 'T')}{dataset[1:]} {Y_LABEL}"
        # log=True
        # if title is not None:
        #     axs.set_title(title, fontsize=18) # [title])
        # if xlabel is not None:
        #     axs.set_xlabel(xlabel, fontsize=18)
        # if ylabel is not None:
        #     axs.set_ylabel(ylabel, fontsize=18)
        # axs.grid(True, which="both", ls="-", alpha=0.8)

        # axs.tick_params(axis='both', which='major', labelsize=18)

        # if log:
        #     axs.set_xscale("log")
        
        # axs.set_xticks(X_MAP[task])
        axs.set_xlim(min_x, max_x)
        min_y = np.inf
        for losses, times in zip(all_losses, all_times):
            losses = [min(loss[time>=min_x]) for loss, time in zip(losses, times)]
            min_loss = min(losses)
            if min_loss < min_y:
                min_y = min_loss
            # min(X_MAP[task]), max(X_MAP[task]))
            # axs[task_index].set_ylim(
            #     min(Y_MAP[dataset][experiment]),
            #     max(Y_MAP[dataset][experiment])
            # )
        
        max_y = 1

        if experiment_set in Y_MAP:
            min_y, max_y = Y_MAP[experiment_set][task]
        
        # min_y -= 0.1
        # if task == 10101:
        #     min_y = 0.6
        #     max_y = 0.8
        # elif task == 7592:
        #     min_y = 0.45
        #     max_y = 0.8
        # elif task == 146195:
        #     min_y = 0.65
        #     max_y = 0.8
        # elif task == 14965:
        #     min_y = 0.8
        #     max_y = 0.9
        # elif task == 3:
        #     min_y = .95
        # elif task == 31:
        #     min_y = 0.5
        #     max_y = 0.8
        # elif task == 9981:
        #     min_y = 0.95


        axs.set_ylim(ymin=min_y, ymax=max_y)

        sns.despine(fig)

        # fig.legend(prop={'size':13}, bbox_to_anchor=(1,0), loc="center right",  bbox_transform=fig.transFigure)
        _legend_flag = len(strategies) % 2 != 0
        handles, labels = axs.get_legend_handles_labels()
        fig.legend(
            handles,
            labels,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.15) if _legend_flag else (0.5, -0.25),
            ncol=len(strategies) if _legend_flag else 2,
            frameon=False
        )
        fig.tight_layout(pad=0, h_pad=.5)

        save_fig(
            fig,
            filename= f"{task}",
            output_dir=figure_output_dir,
        )
        trajectories.append(df)
    return trajectories
    

# all_rankings = []
# n_iter = 500  # number of bootstrap samples to use for estimating the ranks.
# n_tasks = len(task_list)

# for i in range(n_iter):
#     pick = np.random.choice(all_trajectories[0][0].shape[1], size=(len(model_list)))

#     for j in range(n_tasks):
#         all_trajectories_tmp = pd.DataFrame(
#             {
#                 model_list[k]: at[j].iloc[:, pick[k]]
#                 for k, at in enumerate(all_trajectories)
#             }
#         )
#         all_trajectories_tmp = all_trajectories_tmp.fillna(method="ffill", axis=0)
#         r_tmp = all_trajectories_tmp.rank(axis=1)
#         all_rankings.append(r_tmp)

# final_ranks = []
# for i, model in enumerate(model_list):
#     ranks_for_model = []
#     for ranking in all_rankings:
#         ranks_for_model.append(ranking.loc[:, model])
#     ranks_for_model = pd.DataFrame(ranks_for_model)
#     ranks_for_model = ranks_for_model.fillna(method="ffill", axis=1)
#     final_ranks.append(ranks_for_model.mean(skipna=True))

# # Step 3. Plot the average ranks over time.
# #####################################################################################
# for i, model in enumerate(model_list):
#     X_data = []
#     y_data = []
#     for x, y in final_ranks[i].iteritems():
#         X_data.append(x)
#         y_data.append(y)
#     X_data.append(max_runtime)
#     y_data.append(y)
#     plt.plot(X_data, y_data, label=model)
#     plt.xlabel("time [sec]")
#     plt.ylabel("average rank")
#     plt.legend()
# plt.savefig(saveto)


# ['ebo_etp_F_w_F_pef_T_ueol_F',
# 'ebo_etp_T_w_F_pef_T_ueol_F',
# 'ebo_etp_F_w_F_pef_F_ueol_F',
# 'ebor_etp_T_w_F_pef_T_ueol_F',
# 'ebos_etp_T_w_F_pef_T_ueol_F',
# 'es_etp_F_w_F_pef_F_ueol_F',
# 'es_etp_T_w_F_pef_F_ueol_F',
# 'eih_etp_F_w_F_pef_T_ueol_F',
# 'eih_etp_T_w_F_pef_T_ueol_F',
# 'eih_etp_F_w_T_pef_T_ueol_F',
# 'eih_etp_T_w_T_pef_T_ueol_F',
# 'eih_etp_F_w_T_pef_F_ueol_F',
# 'eih_etp_T_w_T_pef_F_ueol_F',
# 'eih_etp_F_w_F_pef_F_ueol_F',
# 'ebo_etp_F_w_F_pef_F_ueol_T',
# 'ebo_etp_F_w_F_pef_T_ueol_T',
# 'ebo_etp_T_w_F_pef_T_ueol_T',
# 'ebor_etp_F_w_F_pef_T_ueol_T',
# 'ebos_etp_F_w_F_pef_T_ueol_T',
# 'ebor_etp_T_w_F_pef_T_ueol_T',
# 'ebos_etp_T_w_F_pef_T_ueol_T',
# 'sespl_etp_F_w_F_pef_F_ueol_F',
# 'esr_etp_F_w_F_pef_F_ueol_F',
# 'sespl_etp_T_w_F_pef_F_ueol_F',
# 'esr_etp_T_w_F_pef_F_ueol_F',
# 'eihr_etp_F_w_T_pef_T_ueol_F',
# 'eihs_etp_F_w_T_pef_T_ueol_F',
# 'eihs_etp_T_w_T_pef_T_ueol_F',
# 'eihr_etp_T_w_T_pef_T_ueol_F',
# 'eihr_etp_F_w_F_pef_T_ueol_F',
# 'eihs_etp_F_w_F_pef_T_ueol_F',
# 'sft_etp_F_w_F_pef_T_ueol_F',
# 'eihr_etp_T_w_F_pef_T_ueol_F',
# 'sft_etp_T_w_F_pef_T_ueol_F',
# 'eihs_etp_T_w_F_pef_T_ueol_F',
# 'sft_etp_F_w_F_pef_F_ueol_F',
# 'eihr_etp_F_w_T_pef_F_ueol_F',
# 'eihs_etp_F_w_T_pef_F_ueol_F',
# 'sa_etp_F_w_F_pef_F_ueol_F']