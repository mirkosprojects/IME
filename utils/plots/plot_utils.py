import csv
import numpy as np

def read_results(filename: str):
    """Reads the overall_results.csv file and returns dictonaries containing the results"""
    res_illumination = {}
    res_viewpoint = {}
    res_all = {}

    # read csv file into dictonaries
    with open(filename) as f:
        csv_reader = csv.reader(f)
        headings = next(csv_reader)
        sub_headings = next(csv_reader)
        num_thresholds = int(((len(sub_headings)-1)/3) - 2)      # csv file with 3 data columns, one label and two columns, where features and matches are stored
        pixel_thresholds = sub_headings[1:num_thresholds+1]

        for line in csv_reader:
            alg = line[0]
            res_illumination[alg] = [float(line[i+1]) for i, value in enumerate(pixel_thresholds)]
            res_viewpoint[alg] = [float(line[i+13]) for i, value in enumerate(pixel_thresholds)]
            res_all[alg] = [float(line[i+25]) for i, value in enumerate(pixel_thresholds)]
    return res_illumination, res_viewpoint, res_all, pixel_thresholds

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