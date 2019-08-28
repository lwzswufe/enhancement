# author='lwz'
# coding:utf-8
import numpy as np
import pandas as pd
import math
import os
from DecisionTree.cart_frame import CartTree, disp_tree, dot2jpg


def main():
    filename = "sample.csv"
    labels = ['mean5_close', 'mean5_vol', 'mean20_close',
       'mean20_vol', 'mean60_close', 'mean60_vol', 'mean5_001', 'mean20_001',
       'mean60_001', 'mean5_005', 'mean20_005', 'mean60_005', 'mean5_006',
       'mean20_006', 'mean60_006', 'mean5_300', 'mean20_300', 'mean60_300',
       'is_break']
    target_col = "y"
    crat = CartTree()
    crat.load_dataset(filename, target_col, labels)
    crat.train()
    disp_tree(crat.tree)
    dot2jpg()


if __name__ == "__main__":
    main()
