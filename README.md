# PlaneteEEGeval

Python Scripts to convert and analyze EEG data in aim to compare 3 EEG systems : 

LIVEAMP :

[![LiveAmp](https://www.brainproducts.com/wp-content/uploads/2021/01/PDP_LiveAmp32-400x400.jpg)](https://www.brainproducts.com/solutions/liveamp/)


EPOCH FLEX : 

[![Epoch Flex](https://cdn-bhgin.nitrocdn.com/fYiCbyekuWxdwsIavStGyhFBtSFZmwkM/assets/images/optimized/rev-bf60e52/d2z0k1elb7rxgj.cloudfront.net/uploads/2021/09/EpocFlex-product-header.png)](https://www.emotiv.com/epoc-flex/)


BRAINAMP : 

[![BrainAmp](https://www.brainproducts.com/wp-content/uploads/2021/02/PDP_BrainAmp-PowerPack-BUA-1000-400x400.jpg)](https://www.brainproducts.com/solutions/brainamp/)


## Instructions

### Installation
- Clone or download this folder

- Clone the repo PyABA : Python developer tools for the Analysis of Brain Activity

`` https://github.com/MabyManu/PyABA.git ``

- Change Path in AddPyABA_Path.py

### Dependencies
You will need:

- numpy
- mne
- json
- scipy

## Scripts

### Convert json Files in mne *.fif files - ConvertJSONFiles.py


Select the root directory that contains the *.json file

Converted data are stored in *\_fifData\epochs\* folder


### Analysis for one dataset - SingleAnalysis.py


Select a * *Target-epo.fif * file
Compare Target and Non Target Responses


### Analysis on subject level - SubjectAnalysis.py


Select 2 * *Target-epo.fif * files to compare 2 EEG systems

