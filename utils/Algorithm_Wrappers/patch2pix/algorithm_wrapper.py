#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 14:15:00 2021

@authors: ufukefe and kutalmisince
"""
import os
import argparse
import numpy as np


#First, extract and save the original algorithm's output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Algorithm wrapper for Image Matching Evaluation',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--alg_name', type=str)
    parser.add_argument('--alg_dir', type=str)
    parser.add_argument('--dataset_dir', type=str) 
    parser.add_argument('--output_dir', type=str)    
    parser.add_argument('--ratio_th', type=float, default=0.9)

    args = parser.parse_args()
      
    
    os.system('conda run -n ' + args.alg_name + ' python3 ' + args.alg_dir + '/' + 'algorithm_wrapper_util.py' +
              ' --alg_dir ' + args.alg_dir + ' --input_dir ' + args.dataset_dir + 
              ' --input_pairs ' + args.dataset_dir + '/' + 'image_pairs.txt' +
              ' --output_dir ' + args.output_dir + '/' + 'original_outputs' + ' --resize 1024' + 
              ' --ratio_th ' + str(args.ratio_th)) 
    
 #Then, read saved outputs and transform to proper format (keypointsA, keypointsB, matches)
    
    pairs_out = os.listdir(args.output_dir  + '/' + 'original_outputs')
    
    with open(args.dataset_dir + '/' + 'image_pairs.txt') as f:
        for line in f:
            pairs = line.split(' ')
            subset = pairs[0].split('/')[0]
            subsubset = pairs[0].split('/')[1]
            p1 = pairs[0].split('/')[2].split('.')[0]
            p2 = pairs[1].split('/')[2].split('.')[0]
            
            if not os.path.exists(args.output_dir + '/' + 'outputs' + '/' + subset + '/' + subsubset):
                os.makedirs(args.output_dir + '/' + 'outputs' + '/' + subset + '/' + subsubset)
            
            for k in pairs_out:
                if p1 in k and p2 in k:
                    
                    # Original Algorithm's Output
                    pair_out = np.load(args.output_dir + '/' + 'original_outputs' + '/' + k)
                    
                    keypoints0 = pair_out['keypoints0']
                    keypoints1 = pair_out['keypoints1']
                    mtchs = pair_out['matches']
                    
                    # Wrapper's Output
                    pointsA = keypoints0
                    pointsB = keypoints1
                    matches = np.vstack(((mtchs > -1).nonzero(), mtchs[mtchs > -1])).T                  
                    
                    np.savez_compressed(args.output_dir + '/' + 'outputs' + '/' + subset + '/' + subsubset + 
                                        '/' + k, pointsA=pointsA, pointsB=pointsB, matches=mtchs)
                    
          
