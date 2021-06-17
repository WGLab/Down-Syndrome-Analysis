import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict
import sys
import argparse

# makes beautiful bar charts in the style of the CCR paper
# 10: defaultdict(<class 'float'>, {'cTakes': 25.0, 'CLAMP': 17.857142857142858, 'txt2hpo': 10.714285714285714, 'MetaMap': 17.857142857142858, 'Expert': 11.11111111111111})
# 50: defaultdict(<class 'float'>, {'cTakes': 42.857142857142854, 'CLAMP': 32.142857142857146, 'txt2hpo': 53.57142857142857, 'MetaMap': 46.42857142857143, 'Expert': 33.333333333333336})
# 100: defaultdict(<class 'float'>, {'cTakes': 42.857142857142854, 'CLAMP': 42.857142857142854, 'txt2hpo': 53.57142857142857, 'MetaMap': 50.0, 'Expert': 40.74074074074074})
# 1000: defaultdict(<class 'float'>, {'cTakes': 67.85714285714286, 'CLAMP': 64.28571428571429, 'txt2hpo': 71.42857142857143, 'MetaMap': 71.42857142857143, 'Expert': 66.66666666666667})
# defaultdict(<function <lambda> at 0x7f8658af73a0>, {'cTakes': defaultdict(<class 'float'>, {'top1000': 67.85714285714286, 'top10': 25.0, 'top50': 42.857142857142854, 'top100': 42.857142857142854}), 'CLAMP': defaultdict(<class 'float'>, {'top1000': 64.28571428571429, 'top50': 32.142857142857146, 'top100': 42.857142857142854, 'top10': 17.857142857142858}), 'txt2hpo': defaultdict(<class 'float'>, {'top1000': 71.42857142857143, 'top50': 53.57142857142857, 'top100': 53.57142857142857, 'top10': 10.714285714285714}), 'MetaMap': defaultdict(<class 'float'>, {'top1000': 71.42857142857143, 'top50': 46.42857142857143, 'top100': 50.0, 'top10': 17.857142857142858}), 'Expert': defaultdict(<class 'float'>, {'top1000': 66.66666666666667, 'top100': 40.74074074074074, 'top50': 33.333333333333336, 'top10': 11.11111111111111})})
def accplot(dicts, labels, filename):

    print(dicts)

    if(not labels):
        labels = ['cTakes', 'CLAMP', 'txt2hpo', 'MetaMap', 'Expert']
        

    while(len(labels) < 4):
        labels.append('label{}'.format(str(len(labels))))

    '''
    if labels:
        label=labels[0]
        adlabel=labels[-1]
    else:
        label="Phen2Gene"
        adlabel="Original Phenolyzer (ver. 0.2.2)"
    '''

    def autolabel(rects, ax, yoffset=0, xoffset=0):
        """
        Attach a text label above each bar displaying its height
        """
        global filename
        for rect in rects:
            height = rect.get_height()
            if height==1: # 2 for log2
                height=rect.get_y()
                ax.text(rect.get_x() + rect.get_width()/2., .65*height,
                        '%.1f' % float(height),
                        ha='center', va='bottom')
                continue
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                   '%.1f' % float(height),
                   ha='center', va='bottom', fontweight='bold')

    import seaborn as sns
    sns.set_style('white')
    matplotlib.rcParams['pdf.fonttype'] = 42
    #matplotlib.rcParams['font.family'] = 'sans-serif'
    #matplotlib.rcParams['font.sans-serif'] = ['Arial']
    matplotlib.rcParams['font.size'] = 11

    fig, ax = plt.subplots(figsize=(15,5))

    width=0.6
    distance = 4
    ct = 0
    colors = [(161/255.0,218/255.0,215/255.0),(56/255.0,138/255.0,172/255.0),(95/255.0,158/255.0,160/255.0),(135/255.0,206/255.0,250/255.0),(105/255.0,222/255.0,250/255.0)]
    edgecolor=(96/255.0, 133/255.0, 131/255.0)
    for i, d in enumerate(dicts):
        ct+=1
        print(d)
        ranks = dicts[d].keys()
        heights = dicts[d].values()

        lefts=np.arange(0+(i+1)*width,distance*len(ranks)+width, distance)
        rects=ax.bar(x=lefts,height=heights,width=width,tick_label=ranks,color=colors[i], edgecolor=edgecolor,label=d)
        # autolabel(rects, ax, -6, -0.1)
        autolabel(rects, ax, xoffset=-0.2)


    ax.set_xticks(lefts-width*2)
    ax.set_xticklabels(ranks)

    ax.legend(loc='upper left', ncol=1,bbox_to_anchor=(0, 1.1))
    # fig.legend(loc='upper center', ncol=1,bbox_to_anchor=(0, 1.1))

    def mkdir_p(path):
        import os
        if not os.path.isdir(path):
            os.makedirs(path)

    lims=ax.get_ylim()
    # ax.set_ylim(lims[0]/1.5, lims[1]*1.11)
    ax.set_ylim(lims[0]/1.5, lims[1]+.4)
    ax.set_xlabel("Ranked Gene Lists", fontsize=15)
    ax.set_ylabel("% of Cases with Causal Gene in List", fontsize=14.5)
    sns.despine()
    mkdir_p("figures")
    plt.savefig('figures/phen2gene'+filename+'.png', bbox_inches='tight')
