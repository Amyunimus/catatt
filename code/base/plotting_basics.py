#!/usr/bin/env python
# encoding: utf-8
"""
plotting_basics.py

Created by Emily Ward on 2017-05-29.
Copyright (c) 2017 Emily Ward. All rights reserved.
"""

import sys
import os


def main():
    pass

def plotMyEffect(a_test, CIs):

    figsize(6, 6)
    mpl.rcParams['font.size']=22

    fig, ax = plt.subplots(1)
    #ax.margins(0.05)

    spines_to_remove = ['top', 'right']

    for spine in spines_to_remove:
        ax.spines[spine].set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    
    d = a_test.reset_index()
    first = len(pd.Series(d.ix[:,0].values).unique())
    second = len(pd.Series(d.ix[:,1].values).unique())
    try:
        third = len(pd.Series(d.ix[:,2].values).unique())
    except IndexError:
        third = 0

    colors = ['#b2df8a']*second
    colors.extend(['#a6cee3']*second)
    colors.extend(['#1c9099']*second)
    colors.extend(['#ffc676']*second)

    #colors = ['#b2df8a','#b2df8a','#a6cee3','#a6cee3','#1c9099','#1c9099']
    #colors = ['#fb9a99','#fb9a99','lightgray','lightgray']

    tick_params(labelsize=18)
    ylabel(a_test.name, fontsize=22) #ind = np.arange(N)    # the x locations for the groups
    
    #colors = ['#fb9a99','#fb9a99','lightgray','lightgray']
    a_test.plot(kind='bar',grid=False, yerr=CIs,color=colors,ecolor='#262626',ax=ax)
    ##print a_test
    
    ax.set_xlim(-1, len(a_test))
    plt.show()
    
    
if __name__ == '__main__':
    main()