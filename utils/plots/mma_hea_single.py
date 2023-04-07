#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import matplotlib.pyplot as plt

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


def main():
    """
    Create mean matching accuracy vs pixel threshold plot from the overall_results.csv file
    
    Create homography estimation accuracy vs pixel threshold plot from the overall_results.csv file
    """
    
    ######## Mean Matching Accuracy (MMA) #########

    mma_illumination, mma_viewpoint, mma_all = read_results(os.path.join(directory, 'overall_results_mma.csv'), pixel_thresholds)
    
    # create figure and axes
    fig, axs = plt.subplots(1, 3, figsize=(17, 5), sharey=True)

    # create illumination subplot
    for alg in mma_illumination.keys():
        axs[0].plot(pixel_thresholds, mma_illumination[alg], label=alg)

    # create viewpoint subplot
    for alg in mma_viewpoint.keys():
        axs[1].plot(pixel_thresholds, mma_viewpoint[alg], label=alg)
    
    # create all subplot
    for alg in mma_all.keys():
        axs[2].plot(pixel_thresholds, mma_all[alg], label=alg)
    
    # labels, title and legend
    for ax in axs:
        ax.set_xlabel('Pixel Threshold')
        ax.set_ylabel('MMA')
        ax.yaxis.set_tick_params(labelbottom=True)
    axs[0].set_title('Illumination')
    axs[1].set_title('Viewpoint')
    axs[2].set_title('All')
    axs[2].legend(loc='lower right')

    plt.savefig(os.path.join(directory, 'mma.png'), dpi=300)


    ######## Homography Estimation Accuracy (HEA) #########

    hea_illumination, hea_viewpoint, hea_all = read_results(os.path.join(directory, 'overall_results_hom.csv'), pixel_thresholds)
    
    # create figure and axes
    fig, axs = plt.subplots(1, 3, figsize=(17, 5), sharey=True)

    # create illumination subplot
    for alg in hea_illumination.keys():
        axs[0].plot(pixel_thresholds, hea_illumination[alg], label=alg)

    # create viewpoint subplot
    for alg in hea_viewpoint.keys():
        axs[1].plot(pixel_thresholds, hea_viewpoint[alg], label=alg)
    
    # create all subplot
    for alg in hea_all.keys():
        axs[2].plot(pixel_thresholds, hea_all[alg], label=alg)
    
    # labels, title and legend
    for ax in axs:
        ax.set_xlabel('Pixel Threshold')
        ax.set_ylabel('HEA')
        ax.yaxis.set_tick_params(labelbottom=True)
    axs[0].set_title('Illumination')
    axs[1].set_title('Viewpoint')
    axs[2].set_title('All')
    axs[2].legend(loc='lower right')

    plt.savefig(os.path.join(directory, 'hea.png'), dpi=300)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create mma and hea plots',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--result_directory', type=str, default='Results')
    parser.add_argument('--dataset', type=str, default='hpatches')
    parser.add_argument('--pixel_thresholds', '--pixel_thresholds', nargs='+', default=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])

    args = parser.parse_known_args()[0]
    directory = os.path.join(args.result_directory, args.dataset)
    pixel_thresholds = args.pixel_thresholds

    main()