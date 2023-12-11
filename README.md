# Table of contents
- [Algorithm for dazzled cameras recognition](#dazzled-algorithm)
  - [The physics case](#the-physics-case)
  - [The Models](#the-models)
    - [NN model](#nn-model)
    - [CNN model](#cnn-model)
- [Before starting](#before-starting)
  - [Required softwares](#required-softwares)
  - [Download input files](#download-input-files)
- [Running the algorithms](#running-the-algorithms)

# CNN algorithm for dazzled cameras recognition

The aim of this algorithm is to identify the peculiar signal pattern produced in a SiPM matrix by a passing particle which releases some of its energy directly into the sensor or just nearby, resulting in a loss of efficiency.
The SiPM matrix is one of the 58 matrices which form the photo-detection system of the GRAIN detector, a vessel filled with liquid Argon (LAr) and surrounded by Silicon Photomultiplier (SiPM) sensors. It is part of the DUNE experiment, devoted to neutrino detection. 

## The physics case

The Deep Underground Neutrino Experiment (DUNE) is a long-baseline neutrino experiment which is under construction in the US between Fermilab, where the neutrino beam will be generated, and the Sanford Underground Research Facility in South Dakota.
The experiment will study neutrino oscillations, trying to measure the $\delta_{cp}$ phase of the PMNS matrix and the neutrino mass ordering. It will also be able to detect cosmic neutrinos, providing important information about cosmic ray sources, useful for multimessenger astrophysics.

<p align = "center">
<img src="/images/dune.png" width="500" class="center"/>
</p>

DUNE is composed by a Near Detector (ND) and a Far Detector (FD), this latter consisting of a large TPC filled with liquid Argon. The ND has the scope of monitoring the neutrino beam just after its generation; it is composed of three sub-detectors: a GAr-TPC, a LAr-TPC, and the SAND detector.

<p align = "center">
<img src="/images/nearDetector.png" width="400" class="center"/>
</p>

SAND is divided into three modules enclosed in a superconducting magnet: a Straw Tube Tracker, an electromagnetic calorimeter and GRAIN.

<p align = "center">
<img src="/images/sand.png" width="500" class="center"/>
</p>

<p align = "center">
The SAND detector. On the left you can see the GRAIN module surrounded by the ECAL.
</p>

The GRAIN (GRanular Argon for Interctions of Neutrinos) module is a vessel containing ~1 ton of liquid Argon in which neutrinos can interact. The charged particles generated in these interactions move inside LAr emmitting scintillation light, which can be detected by SiPMs placed on the walls of the vessel. The SiPMs are arranged in 58 matrices, of 32x32 pixels each. Every matrix is coupled to a Coded Aperture Mask constituiting what we call a "camera".

<p align = "center">
<img src="/images/grainCam.png" width="300" class="center"/>
</p>

<p align = "center">
View of the GRAIN vessel, with SiPM cameras on its walls.
</p>

The aim of GRAIN is to reconstruct the trajectories of secondary particles produced by neutrino interactions. This could be achieved through an algorithm which assigns a probability to every unit volume ("voxel") of GRAIN according to the photons detected by SiPMs: given a photon detected by a specific pixel, the algorithm computes all the possible trajectories the photon could have followed to impinge on that pixel passing through one of the holes of the mask associated to the matrix. Taking into account the attenutaion length and other factors, a different probability is assigned each voxel standing along one of the possible trajetories. Putting together information from every camera and applying a threshold upon the probability, it is possibile to visualise the points from which photons have been generated, and hence reconstruct the path of the secondary particles.

One of the factors that could lead to misreconstruction of trajectories is the presence of "dazzled" cameras, i.e. the fact that a particle could cross a SiPM matrix or could even releases photons in the small gap between the mask and the matrix. In both cases the signal detected by the camera cannot be used in the track-reconstruction process. The peculiar pattern generated on the matrices is shown in the figure below. 

<p align = "center">
<img src="/images/dazzledCam.png" width="800" class="center"/>
</p>

<p align = "center">
Examples of dazzled cameras.
</p>

As it can be seen from the figures above however, the signal pattern can vary significantly from case to case. A Neural Network could hence be an efficient way to classify cameras according to thei pattern.

In the following section two different algorithms are presented: a NN model, which tries to classify cameras according to some features we extracted from the data, and a CNN model, which analyses directly the signal pattern of each matrix as an image.


## The Models

Altough the two models are different, there is a common preprocessing for the raw data. 

### NN model
The algorithm which employes a Neural Network model to classify dazzled cameras can be found in `nn_algorithm.ipynb`. In this file two features are extracted from the data:
- the maximum amplitude of each camera
- the ratio between the mean value and the maximum of each camera
Two binary classifiers are tested on the data: SGDClassifier and KFold.


### CNN model
The algorithm which employes a Convolutional Neural Network model to classify dazzled cameras can be found in `cnn_algorithm.ipynb`. 
It analyses matrices as images composed by 32x32 pixels. Each pixel has an amplitude given by the number of photons detected.
As in the previous case we try to perform a binary classification on the data.

# Before starting
In order to be able to run the algorithms, make sure the following requirements are fulfilled:
- have all the required softwares installed
- download the needed input files
- have a sufficiently powerful machine (CPU cores, GPU, RAM) 

## Required softwares
Pyhton3 has to be installed. Looking at the first lines of the notebooks in this repository, the users can check the additional modules which are needed. In particular I underline the mandatory installation of jupyter notebook and tensorflow.

## Download input files
I provide to the user some files which contain simulated data and the MC truth. They are called *simulation.npy* and *inner_ph.npy* respectively. 
A *simulation.npy* file contains 1000 events of neutrino interaction with the number of photons detected by each pixel, computed taking into account several parameters such as the absorption length of LAr and the PDE of SiPMs. A *inner_ph.npy* file stores the same 1000 events of the simulation file and for each of them the number of photons produced inside every camera i.e. in the volume between the mask and the matrix. 

I provide to the user three couples of files: 
* *simulation_11.npy* and *inner_ph_11.npy*
* *simulation_22.npy* and *inner_ph_22.npy*
* *simulation_33.npy* and *inner_ph_33.npy*

Since they are quite heavy files, they are stored on Google Drive. I shared them so that using the commands below everyone will be able to download them directly into the preferred folder on neutrino-01.

The first step hence should be the creation of a dedicated folder for the files, if possible I suggest to create a `dazzled_camera_dataset` directory inside the cloned repository. 

```
mkdir /path/to/cloned/repository/dazzled_camera_dataset
```
At this point, navigate to the folder, and use the following commands:
* inner_ph_11.npy (907 KB)
```
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1dpQnNqO8nOl5ySE0A5AFdQKZHF6eXXw3' -O inner_ph_11.npy
```
* simulation_11.npy (464 MB)
```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1YGGBfQVbiQVzuggrm3NzRwGYT6iKy1g1' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1YGGBfQVbiQVzuggrm3NzRwGYT6iKy1g1" -O simulation_11.npy && rm -rf /tmp/cookies.txt
```
* inner_ph_22.npy (938 KB)
```
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1CxSrNbynVKtFhQ3wKBS8asp1n5pNmd3R' -O inner_ph_22.npy
```
* simulation_22.npy (480 MB)
```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1NenNQ9XAw3a_rHcCeT-QQsliWLfr1FiS' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1NenNQ9XAw3a_rHcCeT-QQsliWLfr1FiS" -O simulation_22.npy && rm -rf /tmp/cookies.txt
```
* inner_ph_33.npy (938 KB)
```
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Zy0N9lwQztPwuk3jofZAaWV5uUWg8_g9' -O inner_ph_33.npy
```
* simulation_33.npy (480 MB)
```
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1qyznrKdBKlOZ9Uo-FAURa2sYp9i6yLJx' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1qyznrKdBKlOZ9Uo-FAURa2sYp9i6yLJx" -O simulation_33.npy && rm -rf /tmp/cookies.txt
```

# Running the algorithms
The Jupyter Notebook files can be easily executed. Move to the cloned repository and open the notebook files.
