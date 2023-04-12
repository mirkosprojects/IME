#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import itertools
import numpy as np

def read_results(filename: str, pixel_thresholds: list):
    """Reads the overall_results.csv file and returns dictonaries containing the results"""
    res_illumination = {}
    res_viewpoint = {}
    res_all = {}

    # read csv file into dictonaries
    with open(filename) as f:
        for idx, line in enumerate(f):
            line = line.split(',')
            alg = line[0]
            if idx >=2:
                res_illumination[alg] = [float(line[i+1]) for i, value in enumerate(pixel_thresholds)]
                res_viewpoint[alg] = [float(line[i+13]) for i, value in enumerate(pixel_thresholds)]
                res_all[alg] = [float(line[i+25]) for i, value in enumerate(pixel_thresholds)]
    return res_illumination, res_viewpoint, res_all

def calculate_auc(data: list):
    """Calculates the area under curve (AUC) using the trapezoidal rule"""
    data = np.array(data)
    return np.sum(data[:-1] + data[1:]) / 2

def check_best_result(best: dict, current: dict, thresholds: dict, threshold: str):
    """Returns a dictonary containing the results with the highest AUC for every algorithm"""
    result_dict = {}
    if not best:
        thresholds = dict.fromkeys(current.keys())
        return current, thresholds
    else:
        for alg in current:
            if calculate_auc(best[alg]) > calculate_auc(current[alg]):
                result_dict[alg] = best[alg] 
            else:
                result_dict[alg] = current[alg]
                thresholds[alg] = threshold

    return result_dict, thresholds

def main():
    """
    Create mean matching accuracy vs pixel threshold plot from the overall_results.csv files of multiple ratio thresholds.
    Only the curve with the highest AUC is plotted for each algorithm, the corresponding ratio threshold is shown in a table.
    
    Create homography estimation accuracy vs pixel threshold plot from the overall_results.csv files of multiple ratio thresholds.
    Only the curve with the highest AUC is plotted for each algorithm, the corresponding ratio threshold is shown in a table.
    """

    # iteratable colors
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color'] # get default color cycle

    # create figure and axes
    fig, axs = plt.subplots(1, 3, figsize=(17, 5), sharey=True)    

    # best auc result
    best_auc_illumination = {}
    best_auc_viewpoint = {}
    best_auc_all = {}
    thresholds_illimination = {}
    thresholds_viewpoint = {}
    thresholds_all = {}

    for rt_dir, rt in zip(result_dirs, ratio_thresholds):

        ######## Mean Matching Accuracy (MMA) #########

        mma_illumination, mma_viewpoint, mma_all = read_results(os.path.join(rt_dir, 'overall_results_mma.csv'), pixel_thresholds)

        # calculate the result with highest auc
        best_auc_illumination, thresholds_illimination = check_best_result(best_auc_illumination, mma_illumination, thresholds_illimination, rt)
        best_auc_viewpoint, thresholds_viewpoint = check_best_result(best_auc_viewpoint, mma_viewpoint, thresholds_viewpoint, rt)
        best_auc_all, thresholds_all = check_best_result(best_auc_all, mma_all, thresholds_all, rt)
        
    # create illumination subplot
    for alg, color in zip(sorted(best_auc_illumination.keys()), itertools.cycle(colors)):
        axs[0].plot(pixel_thresholds, best_auc_illumination[alg],color=color, label=alg)
    axs[0].table(cellText=[list(thresholds_illimination.values())], colLabels=list(best_auc_illumination.keys()), cellLoc='lower right', bbox=[0.5, 0.0, 0.5, 0.1])

    # create viewpoint subplot
    for alg, color in zip(sorted(best_auc_viewpoint.keys()), itertools.cycle(colors)):
        axs[1].plot(pixel_thresholds, best_auc_viewpoint[alg], color=color, label=alg)
    axs[1].table(cellText=[list(thresholds_viewpoint.values())], colLabels=list(best_auc_viewpoint.keys()), cellLoc='lower right', bbox=[0.5, 0.0, 0.5, 0.1])
    
    # create all subplot
    for alg, color in zip(sorted(best_auc_all.keys()), itertools.cycle(colors)):
        axs[2].plot(pixel_thresholds, best_auc_all[alg], color=color, label=alg)
    axs[2].table(cellText=[list(thresholds_all.values())], colLabels=list(best_auc_all.keys()), cellLoc='lower right', bbox=[0.5, 0.0, 0.5, 0.1])

    # labels, title and legend
    for ax in axs:
        ax.set_xlabel('Pixel Threshold')
        ax.set_ylabel('MMA')
        ax.yaxis.set_tick_params(labelbottom=True)
        ax.set_ylim([0, 1])
    axs[0].set_title('Illumination')
    axs[1].set_title('Viewpoint')
    axs[2].set_title('All')
    axs[2].legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    plt.savefig(os.path.join(os.path.dirname(result_dirs[0]), 'mma_best.png'), dpi=300)

    # create figure and axes
    fig, axs = plt.subplots(1, 3, figsize=(17, 5), sharey=True)

    # best auc result
    best_auc_illumination = {}
    best_auc_viewpoint = {}
    best_auc_all = {}
    thresholds_illimination = {}
    thresholds_viewpoint = {}
    thresholds_all = {}

    for rt_dir, rt in zip(result_dirs, ratio_thresholds):
        ######## Homography Estimation Accuracy (HEA) #########

        hea_illumination, hea_viewpoint, hea_all = read_results(os.path.join(rt_dir, 'overall_results_hom.csv'), pixel_thresholds)

        # calculate the result with highest auc
        best_auc_illumination, thresholds_illimination = check_best_result(best_auc_illumination, hea_illumination, thresholds_illimination, rt)
        best_auc_viewpoint, thresholds_viewpoint = check_best_result(best_auc_viewpoint, hea_viewpoint, thresholds_viewpoint, rt)
        best_auc_all, thresholds_all = check_best_result(best_auc_all, hea_all, thresholds_all, rt)

    # create illumination subplot
    for alg, color in zip(sorted(best_auc_illumination.keys()), itertools.cycle(colors)):
        axs[0].plot(pixel_thresholds, best_auc_illumination[alg], color=color, label=alg)
    axs[0].table(cellText=[list(thresholds_illimination.values())], colLabels=list(best_auc_illumination.keys()), cellLoc='lower right', bbox=[0.5, 0.0, 0.5, 0.1])

    # create viewpoint subplot
    for alg, color in zip(sorted(best_auc_viewpoint.keys()), itertools.cycle(colors)):
        axs[1].plot(pixel_thresholds, best_auc_viewpoint[alg], color=color, label=alg)
    axs[1].table(cellText=[list(thresholds_viewpoint.values())], colLabels=list(best_auc_viewpoint.keys()), cellLoc='lower right', bbox=[0.5, 0.0, 0.5, 0.1])
    
    # create all subplot
    for alg, color in zip(sorted(best_auc_all.keys()), itertools.cycle(colors)):
        axs[2].plot(pixel_thresholds, best_auc_all[alg], color=color, label=alg)
    axs[2].table(cellText=[list(thresholds_all.values())], colLabels=list(best_auc_all.keys()), cellLoc='lower right', bbox=[0.5, 0.0, 0.5, 0.1])
        
    # labels, title and legend
    for ax in axs:
        ax.set_xlabel('Pixel Threshold')
        ax.set_ylabel('HEA')
        ax.yaxis.set_tick_params(labelbottom=True)
        ax.set_ylim([0, 1])
    axs[0].set_title('Illumination')
    axs[1].set_title('Viewpoint')
    axs[2].set_title('All')
    axs[2].legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    plt.savefig(os.path.join(os.path.dirname(result_dirs[0]), 'hea_best.png'), dpi=300)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create mma and hea plots',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--result_directory', type=str, default='Results')
    parser.add_argument('--dataset', type=str, default='hpatches')
    parser.add_argument('--pixel_thresholds', '--pixel_thresholds', nargs='+', default=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    parser.add_argument('--ratio_thresholds', '--ratio_thresholds', nargs='+', default=['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9'])

    args = parser.parse_known_args()[0]
    result_dirs = [os.path.join(args.result_directory, args.dataset, rt) for rt in args.ratio_thresholds]
    pixel_thresholds = args.pixel_thresholds
    ratio_thresholds = args.ratio_thresholds

    main()