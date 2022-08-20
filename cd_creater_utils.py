# Author: Hassan Ismail Fawaz <hassan.ismail-fawaz@uha.fr>
#         Germain Forestier <germain.forestier@uha.fr>
#         Jonathan Weber <jonathan.weber@uha.fr>
#         Lhassane Idoumghar <lhassane.idoumghar@uha.fr>
#         Pierre-Alain Muller <pierre-alain.muller@uha.fr>
# License: GPL3

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Arial'

import operator
import math
from scipy.stats import wilcoxon
from scipy.stats import friedmanchisquare
import networkx


ALGORITHM_COLUMN_NAME = 'method'
PERFORMANCE_METRIC_COLUMN_NAME = 'test_accuracy'
TASK_COLUMN_NAME = 'task_id'


# inspired from orange3 https://docs.orange.biolab.si/3/data-mining-library/reference/evaluation.cd.html
def graph_ranks(avranks, names, p_values, cd=None, cdmethod=None, lowv=None, highv=None,
                width=6, textspace=1, reverse=False, filename=None, labels=False, **kwargs):
    """
    Draws a CD graph, which is used to display  the differences in methods'
    performance. See Janez Demsar, Statistical Comparisons of Classifiers over
    Multiple Data Sets, 7(Jan):1--30, 2006.

    Needs matplotlib to work.

    The image is ploted on `plt` imported using
    `import matplotlib.pyplot as plt`.

    Args:
        avranks (list of float): average ranks of methods.
        names (list of str): names of methods.
        cd (float): Critical difference used for statistically significance of
            difference between methods.
        cdmethod (int, optional): the method that is compared with other methods
            If omitted, show pairwise comparison of methods
        lowv (int, optional): the lowest shown rank
        highv (int, optional): the highest shown rank
        width (int, optional): default width in inches (default: 6)
        textspace (int, optional): space on figure sides (in inches) for the
            method names (default: 1)
        reverse (bool, optional):  if set to `True`, the lowest rank is on the
            right (default: `False`)
        filename (str, optional): output file name (with extension). If not
            given, the function does not write a file.
        labels (bool, optional): if set to `True`, the calculated avg rank
        values will be displayed
    """
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_agg import FigureCanvasAgg
    except ImportError:
        raise ImportError("Function graph_ranks requires matplotlib.")

    width = float(width)
    textspace = float(textspace)

    def nth(l, n):
        """
        Returns only nth elemnt in a list.
        """
        n = lloc(l, n)
        return [a[n] for a in l]

    def lloc(l, n):
        """
        List location in list of list structure.
        Enable the use of negative locations:
        -1 is the last element, -2 second last...
        """
        if n < 0:
            return len(l[0]) + n
        else:
            return n

    def mxrange(lr):
        """
        Multiple xranges. Can be used to traverse matrices.
        This function is very slow due to unknown number of
        parameters.

        >>> mxrange([3,5])
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]

        >>> mxrange([[3,5,1],[9,0,-3]])
        [(3, 9), (3, 6), (3, 3), (4, 9), (4, 6), (4, 3)]

        """
        if not len(lr):
            yield ()
        else:
            # it can work with single numbers
            index = lr[0]
            if isinstance(index, int):
                index = [index]
            for a in range(*index):
                for b in mxrange(lr[1:]):
                    yield tuple([a] + list(b))

    def print_figure(fig, *args, **kwargs):
        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(*args, **kwargs)

    sums = avranks

    nnames = names
    ssums = sums

    if lowv is None:
        lowv = min(1, int(math.floor(min(ssums))))
    if highv is None:
        highv = max(len(avranks), int(math.ceil(max(ssums))))

    cline = 0.4

    k = len(sums)

    lines = None

    linesblank = 0
    scalewidth = width - 2 * textspace

    def rankpos(rank):
        if not reverse:
            a = rank - lowv
        else:
            a = highv - rank
        return textspace + scalewidth / (highv - lowv) * a

    distanceh = 0.25

    cline += distanceh

    # calculate height needed height of an image
    minnotsignificant = max(2 * 0.2, linesblank)
    height = cline + ((k + 1) / 2) * 0.2 + minnotsignificant

    fig = plt.figure(figsize=(width, height))
    fig.set_facecolor('white')
    ax = fig.add_axes([0, 0, 1, 1])  # reverse y axis
    ax.set_axis_off()

    hf = 1. / height  # height factor
    wf = 1. / width

    def hfl(l):
        return [a * hf for a in l]

    def wfl(l):
        return [a * wf for a in l]

    # Upper left corner is (0,0).
    ax.plot([0, 1], [0, 1], c="w")
    ax.set_xlim(0, 1)
    ax.set_ylim(1, 0)

    def line(l, color='k', **kwargs):
        """
        Input is a list of pairs of points.
        """
        ax.plot(wfl(nth(l, 0)), hfl(nth(l, 1)), color=color, **kwargs)

    def text(x, y, s, *args, **kwargs):
        ax.text(wf * x, hf * y, s, *args, **kwargs)

    line([(textspace, cline), (width - textspace, cline)], linewidth=2)

    bigtick = 0.3
    smalltick = 0.15
    linewidth = 2.0
    linewidth_sign = 4.0

    tick = None
    for a in list(np.arange(lowv, highv, 0.5)) + [highv]:
        tick = smalltick
        if a == int(a):
            tick = bigtick
        line([(rankpos(a), cline - tick / 2),
              (rankpos(a), cline)],
             linewidth=2)

    for a in range(lowv, highv + 1):
        text(rankpos(a), cline - tick / 2 - 0.05, str(a),
             ha="center", va="bottom", size=16)

    k = len(ssums)

    def filter_names(name):
        return name

    space_between_names = 0.24

    for i in range(math.ceil(k / 2)):
        chei = cline + minnotsignificant + i * space_between_names
        line([(rankpos(ssums[i]), cline),
              (rankpos(ssums[i]), chei),
              (textspace - 0.1, chei)],
             linewidth=linewidth)
        if labels:
            text(textspace + 0.3, chei - 0.075, format(ssums[i], '.4f'), ha="right", va="center", size=10)
        text(textspace - 0.2, chei, filter_names(nnames[i]), ha="right", va="center", size=16)

    for i in range(math.ceil(k / 2), k):
        chei = cline + minnotsignificant + (k - i - 1) * space_between_names
        line([(rankpos(ssums[i]), cline),
              (rankpos(ssums[i]), chei),
              (textspace + scalewidth + 0.1, chei)],
             linewidth=linewidth)
        if labels:
            text(textspace + scalewidth - 0.3, chei - 0.075, format(ssums[i], '.4f'), ha="left", va="center", size=10)
        text(textspace + scalewidth + 0.2, chei, filter_names(nnames[i]),
             ha="left", va="center", size=16)

    # no-significance lines
    def draw_lines(lines, side=0.05, height=0.1):
        start = cline + 0.2

        for l, r in lines:
            line([(rankpos(ssums[l]) - side, start),
                  (rankpos(ssums[r]) + side, start)],
                 linewidth=linewidth_sign)
            start += height
            print('drawing: ', l, r)

    # draw_lines(lines)
    start = cline + 0.2
    side = -0.02
    height = 0.1

    # draw no significant lines
    # get the cliques
    cliques = form_cliques(p_values, nnames)
    i = 1
    achieved_half = False
    print(nnames)
    for clq in cliques:
        if len(clq) == 1:
            continue
        print(clq)
        min_idx = np.array(clq).min()
        max_idx = np.array(clq).max()
        if min_idx >= len(nnames) / 2 and achieved_half == False:
            start = cline + 0.25
            achieved_half = True
        line([(rankpos(ssums[min_idx]) - side, start),
              (rankpos(ssums[max_idx]) + side, start)],
             linewidth=linewidth_sign)
        start += height


def form_cliques(p_values, nnames):
    """
    This method forms the cliques
    """
    # first form the numpy matrix data
    m = len(nnames)
    g_data = np.zeros((m, m), dtype=np.int64)
    for p in p_values:
        if p[3] == False:
            i = np.where(nnames == p[0])[0][0]
            j = np.where(nnames == p[1])[0][0]
            min_i = min(i, j)
            max_j = max(i, j)
            g_data[min_i, max_j] = 1

    g = networkx.Graph(g_data)
    return networkx.find_cliques(g)


def draw_cd_diagram(df_perf=None, alpha=0.05, title=None, labels=False, figname='cd-diagram'):
    """
    Draws the critical difference diagram given the list of pairwise classifiers that are
    significant or not
    """
    p_values, average_ranks, _ = wilcoxon_holm(df_perf=df_perf, alpha=alpha)

    print(average_ranks)

    for p in p_values:
        print(p)


    graph_ranks(average_ranks.values, average_ranks.keys(), p_values,
                cd=None, reverse=True, width=9, textspace=1.5, labels=labels)

    font = {'family': 'sans-serif',
        'color':  'black',
        'weight': 'normal',
        'size': 22,
        }
    if title:
        plt.title(title,fontdict=font, y=0.9, x=0.5)
    plt.savefig(f'{figname}.png',bbox_inches='tight')

def wilcoxon_holm(alpha=0.05, df_perf=None):
    """
    Applies the wilcoxon signed rank test between each pair of algorithm and then use Holm
    to reject the null's hypothesis
    """
    print(pd.unique(df_perf[ALGORITHM_COLUMN_NAME]))
    # count the number of tested datasets per classifier
    df_counts = pd.DataFrame({'count': df_perf.groupby(
        [ALGORITHM_COLUMN_NAME]).size()}).reset_index()
    # get the maximum number of tested datasets
    max_nb_datasets = df_counts['count'].max()
    # get the list of classifiers who have been tested on nb_max_datasets
    classifiers = list(df_counts.loc[df_counts['count'] == max_nb_datasets]
                       [ALGORITHM_COLUMN_NAME])
    # test the null hypothesis using friedman before doing a post-hoc analysis
    friedman_p_value = friedmanchisquare(*(
        np.array(df_perf.loc[df_perf[ALGORITHM_COLUMN_NAME] == c][PERFORMANCE_METRIC_COLUMN_NAME])
        for c in classifiers))[1]
    # if friedman_p_value >= alpha:
    #     # then the null hypothesis over the entire classifiers cannot be rejected
    #     print('the null hypothesis over the entire classifiers cannot be rejected')
    #     exit()
    # get the number of classifiers
    m = len(classifiers)
    # init array that contains the p-values calculated by the Wilcoxon signed rank test
    p_values = []
    # loop through the algorithms to compare pairwise
    better_classifiers = []
    for i in range(m - 1):
        # get the name of classifier one
        classifier_1 = classifiers[i]
        # get the performance of classifier one
        perf_1 = np.array(df_perf.loc[df_perf[ALGORITHM_COLUMN_NAME] == classifier_1][PERFORMANCE_METRIC_COLUMN_NAME]
                          , dtype=np.float64)
        for j in range(i + 1, m):
            # get the name of the second classifier
            classifier_2 = classifiers[j]
            # get the performance of classifier one
            perf_2 = np.array(df_perf.loc[df_perf[ALGORITHM_COLUMN_NAME] == classifier_2]
                              [PERFORMANCE_METRIC_COLUMN_NAME], dtype=np.float64)
            diff_perf = perf_1-perf_2
            wins = sum(diff_perf>0)
            tie = sum(diff_perf==0)
            loss = sum(diff_perf<0)
            if wins > loss:
                winner = classifier_1
            else:
                winner = classifier_2
            # calculate the p_value
            p_value = wilcoxon(perf_1, perf_2, zero_method='pratt')[1]
            # appen to the list
            p_values.append((classifier_1, classifier_2, p_value, False))
            better_classifiers.append(
                {'classifier_1': classifier_1,
                'classifier_2': classifier_2,
                'p_value': p_value,
                'winner': winner,
                'wins': wins,
                'tie': tie,
                'loss': loss})

    # get the number of hypothesis
    k = len(p_values)
    # sort the list in acsending manner of p-value
    p_values.sort(key=operator.itemgetter(2))
    better_classifiers.sort(key=operator.itemgetter('p_value'))
    better_classifiers = pd.DataFrame(better_classifiers)
    better_classifiers.to_csv('cd_comparison_pairwise.csv')
    # loop through the hypothesis
    for i in range(k):
        # correct alpha with holm
        new_alpha = float(alpha / (k - i))
        # test if significant after holm's correction of alpha
        if p_values[i][2] <= new_alpha:
            p_values[i] = (p_values[i][0], p_values[i][1], p_values[i][2], p_values[i][2] <= new_alpha)
        else:
            # stop
            break
    # compute the average ranks to be returned (useful for drawing the cd diagram)
    # sort the dataframe of performances
    sorted_df_perf = df_perf.loc[df_perf[ALGORITHM_COLUMN_NAME].isin(classifiers)]. \
        sort_values([ALGORITHM_COLUMN_NAME, TASK_COLUMN_NAME])
    # get the rank data
    rank_data = np.array(sorted_df_perf[PERFORMANCE_METRIC_COLUMN_NAME]).reshape(m, max_nb_datasets)

    # create the data frame containg the accuracies
    df_ranks = pd.DataFrame(data=rank_data, index=np.sort(classifiers), columns=
    np.unique(sorted_df_perf[TASK_COLUMN_NAME]))

    # number of wins
    dfff = df_ranks.rank(ascending=False)
    print(dfff)  # [dfff == 1.0].sum(axis=1))
    dfff.to_csv("rank_per_task.csv")
    # average the ranks
    average_ranks = df_ranks.rank(ascending=False).mean(axis=1).sort_values(ascending=False)
    # return the p-values and the average ranks
    return p_values, average_ranks, max_nb_datasets

if __name__ == '__main__':
    df_perf = pd.read_csv('DefaultvsTunedvsEnsembleCritDiffAcc.csv',index_col=False)

    draw_cd_diagram(df_perf=df_perf, title='Accuracy', labels=True)

'''
('eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.00010332274110989746, 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2')
('eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.00013593489535795354, 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2')
('es_pef_F_etp_F_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0001943738953956463, 'es_pef_F_etp_F_ueol_F_w_F_nsl_1')
('es_pef_F_etp_T_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.00025829067878297833, 'es_pef_F_etp_T_ueol_F_w_F_nsl_1')
('eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0004339496168527481, 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2')
('eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.0008465894185333137, 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.0008485688912271598, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0008492294116545201, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.0009183217630187919, 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2')
('eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.001116983297250933, 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.0012667398771491636, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.001267202327408076, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.0013104186322074867, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0013104186322074867, 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.001318529516604007, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.0013722633110084424, 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.0015338232587121371, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.0016057252153630058, 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2')
('eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0016102338039827573, 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2')
('eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.0017344898395088343, 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0017350901356426222, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.0020244047187590957, 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2')
('eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.0025494541702612617, 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2')
('eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0030706744077062796, 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2')
('eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.003179225914633124, 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.003421645022260485, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.0036807777803203544, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.0036852088742126573, 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2')
('eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.003686317135651154, 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0036896430911168804, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.003952940296889082, 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.004404638884323926, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.004417431690076987, 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.004905377898183998, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0049165194106076966, 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.005262762033937447, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.005276012838734499, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.005425218491749714, 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0058582773489792, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.006053925682328033, 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.006067069417403606, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.006067069417403606, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.006487490499788165, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.0071546942367701595, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.007203454408538365, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.00743741197068406, 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.007439338798103838, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.007960726051013054, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.008512463742462529, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.008514601181916137, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.008764828179775053, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 0.008988326900804436, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.009100434094641435, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.009120687096493118, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.009426263499117493, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.009745694926283351, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.009931964132321561, 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2')
('eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.010388694477344947, 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.010729361544703142, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.01109041527420393, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.011108704218644024, 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2')
('eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.011855872394250304, 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.012621316864199063, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.012641459562260949, 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.013475854342622643, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.013735399011286906, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.013830789110548965, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.014734673130882982, 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.01569360335658341, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.015818525667277147, 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.01669986646014744, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.01732354087149456, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.01783274556661222, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 0.018389390230635627, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.0183931778295345, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0183931778295345, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.018895415409226537, 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.020808050438464284, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.02251395726262883, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.02345279453877484, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.023457292130096754, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.024039793356646567, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.029596665045679402, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.029601947147287217, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.03135034477398798, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.03139428244616936, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.03500166655866317, 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 0.035114143897214276, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.037173322461907986, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.037185616024687104, 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.039308057870728594, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.04023867711975933, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.04266392954421394, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 0.043862586119384296, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.046245505645095206, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 0.047556914223003045, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.047556914223003045, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.04878903031752207, 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2')

('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.0527050417902266, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.05723169651289076, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.0587132398010534, 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2')
('eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.06162929045141016, 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.06669943650722936, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.06677009690616179, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.06796080926565959, 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2')
('es_pef_F_etp_T_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.0701921677868738, 'es_pef_F_etp_T_ueol_F_w_F_nsl_1')
('eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.07375401375945774, 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.077503695687017, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.08966145598636162, 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.08969266894373631, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.0961367245289723, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.10077965082261052, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.10348046221911303, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.11348609196918961, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.11867760180009224, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.1242393110515578, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.12674317708870914, 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.12982542697715868, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('es_pef_F_etp_F_ueol_F_w_F_nsl_1', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.1356960385037615, 'es_pef_F_etp_F_ueol_F_w_F_nsl_1')
('es_pef_F_etp_T_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.13846390656614488, 'es_pef_F_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.1480498386698243, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.15919135528292194, 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2')
('es_pef_F_etp_T_ueol_F_w_F_nsl_1', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.16121781297754134, 'es_pef_F_etp_T_ueol_F_w_F_nsl_1')
('eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.1753935456315695, 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.1824064642175477, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.18658721888641716, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 0.19815156999959882, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.20207765971521519, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 0.210251197819885, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.2141142277262974, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.21442654850403764, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 0.21444141318408938, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.21878083478935417, 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.21882562656238658, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 0.22309094973330323, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 0.2316799663387673, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.23186158352815023, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('es_pef_F_etp_F_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.24075227632484308, 'es_pef_F_etp_F_ueol_F_w_F_nsl_1')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.24507388408317632, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 0.2500080829044353, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('es_pef_F_etp_T_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.2544505826463366, 'es_pef_F_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 0.2644459259440093, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 0.26925833791159826, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.2693825350570316, 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.27430358983891256, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.299700943641236, 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1')
('es_pef_F_etp_F_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.316183023257128, 'es_pef_F_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.3218078700949252, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 0.32187061637781267, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 0.3330888315914573, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.33866670775729757, 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.34462041899087525, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 0.3562305023853076, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.3619347669211924, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('es_pef_F_etp_F_ueol_F_w_F_nsl_1', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.3683408747771475, 'es_pef_F_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.36835515010721387, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.379690495597761, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.38686641984360415, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.39297592344856025, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'es_pef_F_etp_T_ueol_F_w_F_nsl_1', 0.39308332666426715, 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.3994231502789568, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.41793169319155477, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.418808361535453, 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 0.43166041225376484, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.4383501510885759, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 0.4455277277121905, 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.4523776866075748, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 0.45921309307332503, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.4798427052511658, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 0.4936612303677803, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.49436273103320993, 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.5033024974311059, 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 0.5162116991888028, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 0.5233570171191724, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.5307746917971448, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('es_pef_F_etp_F_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.5386149676579693, 'es_pef_F_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.5460840884364713, 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 'sa_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.5460840884364713, 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2')
('eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'es_pef_F_etp_F_ueol_F_w_F_nsl_1', 0.5765542356840254, 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 0.5924410699391618, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 0.6082732892281546, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.6160709679114824, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 0.6243148157509877, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.6321876687169254, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.6323865559488365, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('eihr_pef_T_etp_T_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_T_ueol_F_w_F_nsl_2', 0.6406111782179932, 'eihr_pef_T_etp_T_ueol_F_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 0.648503379652976, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.6569075823673494, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.6888093294750408, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ebos_pef_T_etp_F_ueol_T_w_F_nsl_2', 0.6986345103503548, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.732163797782561, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 0.7498547243254692, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 0.7613452634431408, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 0.7667674662984937, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('eih_pef_T_etp_F_ueol_F_w_F_nsl_1', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.7671276783770936, 'eih_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.77584710796318, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('eihr_pef_T_etp_F_ueol_F_w_F_nsl_2', 'eihs_pef_T_etp_F_ueol_F_w_F_nsl_2', 0.7845806883903671, 'eihr_pef_T_etp_F_ueol_F_w_F_nsl_2')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.8022117949916099, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('esr_pef_F_etp_T_ueol_F_w_F_nsl_2', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.8197075378297882, 'esr_pef_F_etp_T_ueol_F_w_F_nsl_2')
('ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 'esr_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.8374713100441715, 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.837611617430081, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 0.8553136786453324, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('eih_pef_T_etp_T_ueol_F_w_F_nsl_1', 'ess_pef_F_etp_F_ueol_F_w_F_nsl_2', 0.8823201618331834, 'eih_pef_T_etp_T_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.8911137955734916, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.891310412715593, 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2')
('ebo_pef_T_etp_F_ueol_F_w_F_nsl_1', 'ebo_pef_T_etp_T_ueol_F_w_F_nsl_1', 0.908511732654558, 'ebo_pef_T_etp_F_ueol_F_w_F_nsl_1')
('ebo_pef_T_etp_F_ueol_T_w_F_nsl_1', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.945531939598918, 'ebo_pef_T_etp_F_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ebor_pef_T_etp_F_ueol_T_w_F_nsl_2', 0.9636392787499026, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebo_pef_T_etp_T_ueol_T_w_F_nsl_1', 'ebor_pef_T_etp_T_ueol_T_w_F_nsl_2', 0.9727430162097797, 'ebo_pef_T_etp_T_ueol_T_w_F_nsl_1')
('ebos_pef_T_etp_T_ueol_T_w_F_nsl_2', 'eihs_pef_T_etp_T_ueol_F_w_F_nsl_2', 0.98183142546504, 'ebos_pef_T_etp_T_ueol_T_w_F_nsl_2')

'''