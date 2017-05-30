#!/usr/bin/env python
# encoding: utf-8
"""
formatting_basics.py

Created by Emily Ward on 2017-05-29.
Copyright (c) 2017 Emily Ward. All rights reserved.
"""

import sys
import os


def main():
    pass
    
def formatMyEffect(in_df,DV,in_list):
    g = in_df.groupby(in_list)
    a = g[DV].mean()
    a = a.reset_index()

    CIs = withinSubCIs(a,DV)
    print "CIs:",' '.join([str(item) for item in CIs])

    ## Get condtion means
    in_list = [item for item in in_list if item != 'subject']

    c = a.groupby(in_list)
    m = c[DV].mean()
    a_test = m

    return a_test, CIs


if __name__ == '__main__':
    main()
