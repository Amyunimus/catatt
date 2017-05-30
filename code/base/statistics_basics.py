#!/usr/bin/env python
# encoding: utf-8
"""
statistics_basics.py

Created by Emily Ward on 2017-05-29.
Copyright (c) 2017 Emily Ward. All rights reserved.
"""

import sys
import os


def main():
    pass

def withinSubCIs(a,DV):

    ## Get subject average
    by_sub = a.groupby('subject')[DV].mean().reset_index()

    ## Get group grand mean
    group_mean = by_sub[DV].mean()

    ## Rename sub average of DV
    by_sub = by_sub.rename(columns={DV:'subAvg'})

    ## Create DF with normalized DV values
    j = a.merge(by_sub,on='subject')
    j['groupAvg'] = group_mean
    j['DV_norm'] = j[DV] - j.subAvg + j.groupAvg

    ## Find IVs from input DF
    IVs = [item for item in list(j.columns) if item not in ['subject','subAvg','groupAvg','DV_norm',DV]]

    ## Group DF across subjects by IVs to get standard deviation by condition
    conditions_norm = j.groupby(IVs)['DV_norm'].std().reset_index()

    ## Find SE, Morey (2008) correction and t-value, and CIs
    conditions_norm['se'] = conditions_norm.DV_norm/np.sqrt(by_sub.shape[0])
    conditions_norm['correction'] = np.sqrt(float(conditions_norm.shape[0])/(float(conditions_norm.shape[0]) - 1))
    conditions_norm['t_val'] = stats.t.ppf(1 - 0.025, by_sub.shape[0] -1)
    conditions_norm['CI'] = conditions_norm.se*conditions_norm.t_val*conditions_norm.correction

    return list(conditions_norm['CI'])

if __name__ == '__main__':
    main()

