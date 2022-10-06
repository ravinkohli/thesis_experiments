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
from plot_utilities import incumbent_plot, save_fig, set_general_plot_style
import seaborn as sns
from experiment_utils import SEEDS, TASKS, X_LABEL, Y_LABEL


def make_incumbent_plot(
    figure_output_dir,
    dataset_info,
    strategies,
    results,
    name_to_label,
    dataset,
    color_marker,
    durations
):

    for task_index, task in enumerate(TASKS):
        strategies_dict = {}
        strategy_names = []
        set_general_plot_style()

        dataset_name = dataset_info[dataset_info['OpenML Task Id'] == task]['Dataset Name'].item()
        fig, axs = plt.subplots(
            1,
            figsize=(10, 4),

        )
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
                    
                    raw_loss = np.array(list(results[strategy][task][seed]['ensemble_history'][f'{dataset}_balanced_accuracy'].values()))
                    failed_losses = [i for i in range(len(raw_loss)) if raw_loss[i] is None]

                    time = np.array(list(results[strategy][task][seed]['ensemble_history']['Timestamp'].values()))/1000
                    duration = durations[strategy][task][seed]['duration']
                    initial_time = time[-1] - duration
                    time = time - initial_time

                    raw_loss = np.delete(raw_loss, failed_losses)
                    losses.append(np.maximum.accumulate(raw_loss))
                    time = np.delete(time, failed_losses)
                    times.append(time)


            incumbent_plot(
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

        
            # axs.set_xticks(X_MAP)
            # axs.set_xlim(min(X_MAP), max(X_MAP))
            # axs[task_index].set_ylim(
            #     min(Y_MAP[dataset][experiment]),
            #     max(Y_MAP[dataset][experiment])
            # )
        
        sns.despine(fig)

        fig.legend(prop={'size':13}, bbox_to_anchor=(1,0), loc="lower right",  bbox_transform=fig.transFigure)
        # _legend_flag = len(strategies) % 2 != 0
        # handles, labels = axs.get_legend_handles_labels()
        # fig.legend(
        #     handles,
        #     labels,
        #     loc="lower center",
        #     bbox_to_anchor=(0.5, -0.15) if _legend_flag else (0.5, -0.25),
        #     ncol=len(strategies) if _legend_flag else 2,
        #     frameon=False
        # )
        # fig.tight_layout(pad=0, h_pad=.5)

        save_fig(
            fig,
            filename= f"{task}",
            output_dir=figure_output_dir,
        )



['ebo_etp_F_w_F_pef_T_ueol_F',
'ebo_etp_T_w_F_pef_T_ueol_F',
'ebo_etp_F_w_F_pef_F_ueol_F',
'ebor_etp_T_w_F_pef_T_ueol_F',
'ebos_etp_T_w_F_pef_T_ueol_F',
'es_etp_F_w_F_pef_F_ueol_F',
'es_etp_T_w_F_pef_F_ueol_F',
'eih_etp_F_w_F_pef_T_ueol_F',
'eih_etp_T_w_F_pef_T_ueol_F',
'eih_etp_F_w_T_pef_T_ueol_F',
'eih_etp_T_w_T_pef_T_ueol_F',
'eih_etp_F_w_T_pef_F_ueol_F',
'eih_etp_T_w_T_pef_F_ueol_F',
'eih_etp_F_w_F_pef_F_ueol_F',
'ebo_etp_F_w_F_pef_F_ueol_T',
'ebo_etp_F_w_F_pef_T_ueol_T',
'ebo_etp_T_w_F_pef_T_ueol_T',
'ebor_etp_F_w_F_pef_T_ueol_T',
'ebos_etp_F_w_F_pef_T_ueol_T',
'ebor_etp_T_w_F_pef_T_ueol_T',
'ebos_etp_T_w_F_pef_T_ueol_T',
'sespl_etp_F_w_F_pef_F_ueol_F',
'esr_etp_F_w_F_pef_F_ueol_F',
'sespl_etp_T_w_F_pef_F_ueol_F',
'esr_etp_T_w_F_pef_F_ueol_F',
'eihr_etp_F_w_T_pef_T_ueol_F',
'eihs_etp_F_w_T_pef_T_ueol_F',
'eihs_etp_T_w_T_pef_T_ueol_F',
'eihr_etp_T_w_T_pef_T_ueol_F',
'eihr_etp_F_w_F_pef_T_ueol_F',
'eihs_etp_F_w_F_pef_T_ueol_F',
'sft_etp_F_w_F_pef_T_ueol_F',
'eihr_etp_T_w_F_pef_T_ueol_F',
'sft_etp_T_w_F_pef_T_ueol_F',
'eihs_etp_T_w_F_pef_T_ueol_F',
'sft_etp_F_w_F_pef_F_ueol_F',
'eihr_etp_F_w_T_pef_F_ueol_F',
'eihs_etp_F_w_T_pef_F_ueol_F',
'sa_etp_F_w_F_pef_F_ueol_F']