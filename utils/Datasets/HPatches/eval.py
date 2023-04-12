#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 14:15:00 2021

@authors: kutalmisince and ufukefe
"""

import argparse
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import os

def eval_matches(p1s, p2s, homography):
    """
    Borrowed from https://github.com/GrumpyZhou/image-matching-toolbox 

    Compute the reprojection errors from im1 to im2 with the given the GT homography
    """
    p1s_h = np.concatenate([p1s, np.ones([p1s.shape[0], 1])], axis=1)   # convert to homogenous coordinates 
    p2s_proj_h = np.transpose(np.dot(homography, np.transpose(p1s_h)))  # Project p1s onto p2s using homography matrix
    p2s_proj = p2s_proj_h[:, :2] / p2s_proj_h[:, 2:]                    # convert back to cartesian coordinates
    dist = np.sqrt(np.sum((p2s - p2s_proj) ** 2, axis=1))               # calculate l2-distance
    return dist

def eval_homography(p1s, p2s, h_gt, im1_path):
    """
    Borrowed from https://github.com/GrumpyZhou/image-matching-toolbox hpatches_helper
    
    Estimate the homography between the matches using RANSAC
    """
    try:
        H_pred, inliers = cv2.findHomography(p1s, p2s, cv2.USAC_MAGSAC, ransacReprojThreshold=3, maxIters=5000, confidence=0.9999)
    except:
        H_pred = None
        inliers = np.zeros(0)
    
    if H_pred is None:
        correctness = np.zeros(10)
    else:
        im = Image.open(im1_path)
        w, h = im.size
        corners = np.array([[0, 0, 1],
                            [0, w - 1, 1],
                            [h - 1, 0, 1],
                            [h - 1, w - 1, 1]])
        real_warped_corners = np.dot(corners, np.transpose(h_gt))
        real_warped_corners = real_warped_corners[:, :2] / real_warped_corners[:, 2:]           # convert back to cartesian coordinates ?
        warped_corners = np.dot(corners, np.transpose(H_pred))
        warped_corners = warped_corners[:, :2] / warped_corners[:, 2:]                          # convert back to cartesian coordinates ?
        mean_dist = np.mean(np.linalg.norm(real_warped_corners - warped_corners, axis=1))
        correctness = np.array([float(mean_dist <= i) for i in range (1,11)])
    return correctness, inliers


def main():
    algorithm_results_mma = {}
    algorithm_results_hom = {}
        
    for i, alg in enumerate(algorithms):
        out_dir = os.path.join(result_directory, alg)
        
        all_results_mma = np.empty(shape=[0, 12])
        all_results_hom = np.empty(shape=[0, 12])
        
        #Enumerate over image_pairs.txt and do evaluation  
        with open(os.path.join(dataset_dir, 'image_pairs.txt')) as f:
            for k, line in enumerate(f):
                pairs = line.split(' ')                 # [path_to_img1 path_to_img2 path_to_homography]
                subset = pairs[0].split('/')[0]         # "illumination" or "viewpoint"
                subsubset = pairs[0].split('/')[1]      # image folder name
                            
                p1 = pairs[0].split('/')[2].split('.')[0]   # name of first file
                p2 = pairs[1].split('/')[2].split('.')[0]   # name of second file
                output_name = p1 + '_' + p2 + '_' + 'matches' + '.npz'
            
                #Load output points and matches
                outputs = np.load(os.path.join(out_dir, 'outputs', subset, subsubset, output_name))
        
                pointsA = outputs['pointsA']    # coordinates of features in image A
                pointsB = outputs['pointsB']    # coordinates of features in image B
                matches = outputs['matches']    # coordinates of matches
                
                #Load groundtruth homographies
                h_name = pairs[2].split('/')[2].split('\n')[0]                                      # homography name from image_pairs
                h_gt = np.loadtxt(os.path.join(dataset_dir, subset, subsubset, h_name))             # load homography
                im1_path = os.path.join(dataset_dir, subset, subsubset, p1 + '.ppm')                # path of image1

                #Load matched points (matches is a matrix of two columns, that contains information about which column of pointsA matches to which column of pointsB ?????)
                pointsA_matched = pointsA[matches[:,0]]
                pointsB_matched = pointsB[matches[:,1]]
                
                #Calculate distances between ground-truth homography and estimated homography
                distances = eval_matches(pointsA_matched, pointsB_matched, h_gt)
                
                if distances.shape[0] >= 1:
                    mma = np.around(np.array([np.count_nonzero(distances <= i)/distances.shape[0] for i in range (1,11)]),3)    # mma = (number of distances <= threshold) / (number of distances)
                                                                                                                                # threshold = 1px - 11px
                else:
                    mma = np.zeros(10)

                #Calculate distances between image projected with ground-truth homography and image projected with estimated homography
                hom_qual, inliers = eval_homography(pointsA_matched, pointsB_matched, h_gt, im1_path)
                
                if inliers.shape[0] > 0:
                    number_of_inliers = sum(inliers > 0)[0]
                else:
                    number_of_inliers = 0
                
                # Write the results in hpatches eval format(0-10px mma, #features / #matches)
                results_mma = np.hstack((mma,(pointsA.shape[0]+pointsB.shape[0])/2,matches.shape[0]))   # [mma1px, mma2px, ... , #features, #matches]
                all_results_mma = np.vstack((all_results_mma,results_mma))                              # append all results from different images into array

                # Write the results in hpatches eval format(0-10px hom_qual, #matches / #inliers)
                results_hom = np.hstack((hom_qual, matches.shape[0], number_of_inliers))    # [hom1px, hom2px, ... , #matches, #inliers]
                all_results_hom = np.vstack((all_results_hom,results_hom))                  # append all results from different images into array


        #Write all_results_mma for each algorithms as csv    
        np.savetxt(out_dir + '_mma' + ".csv", all_results_mma, delimiter=",")
        np.savetxt(out_dir + '_hom' + ".csv", all_results_hom, delimiter=",")

        # number of results for illumination or viewpoint
        num_illumination = 0
        # num_viewpoint = 0
        with open(os.path.join(dataset_dir, 'image_pairs.txt')) as f:
            for line in f:
                if line.startswith('illumination'):
                    num_illumination += 1 
                # if line.startswith('viewpoint'):
                #     num_viewpoint += 1

        # calculate mean results for illumination, viewpoint and overall
        mean_illumination_mma = np.mean(all_results_mma[ : num_illumination, : ], 0)
        mean_viewpoint_mma = np.mean(all_results_mma[num_illumination : , : ], 0)
        mean_all_mma = np.mean(all_results_mma,0)
        algorithm_results_mma[alg] = np.hstack([mean_illumination_mma, mean_viewpoint_mma, mean_all_mma])

        mean_illumination_hom = np.mean(all_results_hom[ : num_illumination, : ], 0)
        mean_viewpoint_hom = np.mean(all_results_hom[num_illumination : , : ], 0)
        mean_all_hom = np.mean(all_results_hom,0)
        algorithm_results_hom[alg] = np.hstack([mean_illumination_hom, mean_viewpoint_hom, mean_all_hom])

    # create headers for csv file
    header1 = ['','', '', '', '', 'Illumination All', '', '', '', '', '', '', 
                '', '', '', '', '', 'Viewpoint All', '', '', '', '', '', '',
                '', '', '', '', '', 'All Results', '', '', '', '', '', '']
    header2_mma = ['1px','2px','3px','4px','5px','6px','7px','8px','9px','10px','#Features','Mmatches',
                '1px','2px','3px','4px','5px','6px','7px','8px','9px','10px','#Features','Mmatches',
                '1px','2px','3px','4px','5px','6px','7px','8px','9px','10px','#Features','Mmatches']
    header2_hom = ['1px','2px','3px','4px','5px','6px','7px','8px','9px','10px','#Matches','#Inliers',
                '1px','2px','3px','4px','5px','6px','7px','8px','9px','10px','#Matches','#Inliers',
                '1px','2px','3px','4px','5px','6px','7px','8px','9px','10px','#Matches','#Inliers']
    headers_mma = pd.MultiIndex.from_arrays([header1, header2_mma], names=['Algorithms', ''])
    headers_hom = pd.MultiIndex.from_arrays([header1, header2_hom], names=['Algorithms', ''])

    # write result to dataframe object
    df_mma = pd.DataFrame.from_dict(algorithm_results_mma,orient='index', columns=headers_mma)
    df_hom = pd.DataFrame.from_dict(algorithm_results_hom,orient='index', columns=headers_hom)

    # print dataframe to csv file
    df_mma.to_csv(os.path.join(result_directory, 'overall_results_mma.csv'), float_format='%.2f')
    df_hom.to_csv(os.path.join(result_directory, 'overall_results_hom.csv'), float_format='%.2f')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Algorithm wrapper for Image Matching Evaluation',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--algorithms', '--algorithms', nargs='+', default=[])
    parser.add_argument('--result_directory', type=str)
    parser.add_argument('--dataset_dir', type=str) 

    args = parser.parse_args()
    algorithms = args.algorithms
    result_directory = args.result_directory
    dataset_dir = args.dataset_dir
    
    main()