# Image Matching Evaluation (IME)

IME provides to test any feature matching algorithm on datasets containing ground-truth homographies. 

Also, one can reproduce the results given in our paper [*Effect of Parameter Optimization on Classical and Learning-based Image Matching Methods*](https://openaccess.thecvf.com/content/ICCV2021W/TradiCV/papers/Efe_Effect_of_Parameter_Optimization_on_Classical_and_Learning-Based_Image_Matching_ICCVW_2021_paper.pdf) published in [ICCV 2021 TradiCV Workshop.](https://sites.google.com/view/tradicv) 

## Currently Supported Algorithms

| **Classical** | **Learning-Based** |
|:---------:|:--------------:|
| SIFT      | SuperPoint     |
| SURF      | SuperGlue      |
| ORB       | Patch2Pix      |
| KAZE      | DFM            |
| AKAZE     |                |
    
## Environment Setup
This repository is created using Anaconda.

Open a terminal in the IME folder and run the following commands;

1. Run bash script to create environment for IME, download algorithms and datasets
    ```sh
    bash install.sh
    ```

2. Activate the environment
    ```sh
    conda activate ime
    ```

## Usage
1. Configure the algorithms to run by editing the following lines in `main.ipy` file

    ```py
        # set up variables
        algorithms = ['dfm', 'akaze', 'kaze', 'orb', 'sift', 'surf']    # algorithms to run
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]      # use thresholds = ['best'] to use each algorithm with the default threshold
        results = 'Results_rt'                                          # result directory
        datasets = ['hpatches', 'hpatches_sp', 'hpatches_speckle']      # datasets to evaluate
    ```

2. Make sure the relative paths of algorithms and datasets are in the `config.json` file
    ```json
    {
        "algorithms": {
            "sift": "Algorithms/sift",
            "surf": "Algorithms/surf",
            "orb": "Algorithms/orb",
            "kaze": "Algorithms/kaze",
            "akaze": "Algorithms/akaze",
            "superpoint": "Algorithms/SuperPoint",
            "superglue": "Algorithms/SuperGlue",
            "patch2pix": "Algorithms/patch2pix",
            "dfm": "Algorithms/DFM/python"
        },
        "datasets": {
            "multi_modal": "Datasets/multi_modal",
            "hpatches": "Datasets/hpatches",
            "hpatches_test": "Datasets/hpatches_test",
            "hpatches_sp": "Datasets/hpatches_sp",
            "hpatches_speckle": "Datasets/hpatches_speckle"
        }
    }
    ```

3. Start the algorithm

    ```sh
    python main.ipy
    ```

4. The results will be saved in `<RESULT_DIR>/<DATASET>/<RATIO_THRESHOLD>/<ALGORITHM>`

5. You can create Mean Matching Accuracy (MMA) and Homography Estimation Accuracy (HEA) plots, by executing the plot utilities as follows
    * Generate MMA and HEA plots with the results from one dataset and one ratio threshold
        ```sh
        python mma_hea.py --result_directory RESULT_DIR --dataset DATASET/RATIO_THRESHOLD
        ```

    * Generate MMA and HEA plots with the results from multiple datasets and one ratio threshold
        ```sh
        python mma_hea_multi_data.py --result_directory RESULT_DIR --datasets DATASET1/RATIO_THRESHOLD DATASET2/RATIO_THRESHOLD
        ```

    * Generate the best MMA and HEA plots with the results from one dataset and multiple ratio thresholds
        ```sh
        python mma_hea_best_rt.py --result_directory RESULT_DIR --dataset DATASET
        ```
        optional: `--ratio_thresholds 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9`

    * Generate MMA and HEA plots with the results from one dataset and multiple ratio thresholds
        ```sh
        python mma_hea_multi_rt.py --result_directory RESULT_DIR --dataset DATASET
        ```
        optional: `--ratio_thresholds 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9`

## Image Noise

To add artificial noise to a dataset, use the following command

```sh
python utils/Datasets/augment_noise.py --dataset_dir PATH_TO_DATASET --name NAME_FOR_NEW_DATASET
```
optional: `--noise TYPE` see available noise types here: [skimage.random_noise](https://scikit-image.org/docs/stable/api/skimage.util.html#skimage.util.random_noise)  
You can add additional skimage parameters by adding `--name value`

> [!NOTE]  
> You can can compare the results from different noises by first running the algorithm on all datasets, then using the `mma_hea_multi_data.py` plot tool

## BibTeX Citation
Please cite our paper if you use the code:

```
@InProceedings{Efe_2021_ICCV,
    author    = {Efe, Ufuk and Ince, Kutalmis Gokalp and Alatan, Aydin},
    title     = {Effect of Parameter Optimization on Classical and Learning-based Image Matching Methods},
    booktitle = {Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV) Workshops},
    month     = {October},
    year      = {2021},
}
```
