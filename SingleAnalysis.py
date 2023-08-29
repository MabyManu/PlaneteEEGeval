# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 11:12:42 2023

@author: manum
"""

import os 
import glob
RootAnalysisFolder = os.path.split(__file__)[0]
from os import chdir
chdir(RootAnalysisFolder)
import mne
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFileDialog,QListView,QAbstractItemView,QTreeView

from AddPyABA_Path import PyABA_path
import sys
 
sys.path.append(PyABA_path)

import pyABA_algorithms,mne_tools
from mne.channels import combine_channels

from mne.stats import permutation_cluster_test,f_threshold_mway_rm

import numpy as np
rejection_rate = 0.15

RootFolder =  os.path.split(RootAnalysisFolder)[0]


filename = QFileDialog.getOpenFileNames( caption='Choose a FIF file .fif file',
                                                    directory=RootFolder,
                                                    filter='*-Target-epo.fif')   


TargetFilename = filename[0][0]
NoTargetFilename = TargetFilename[0:TargetFilename.find("-Target-epo.fif")] + "-NoTarget-epo.fif"

Epochs_NoTarget=mne.read_epochs(NoTargetFilename)
Epochs_Target=mne.read_epochs(TargetFilename)

ThresholdPeak2peak,_,_,ixEpochs2Remove,_ = mne_tools.RejectThresh(Epochs_NoTarget,int(rejection_rate*100))
Epochs_NoTarget.drop(ixEpochs2Remove,verbose=False)			

ThresholdPeak2peak,_,_,ixEpochs2Remove,_ = mne_tools.RejectThresh(Epochs_Target,int(rejection_rate*100))
Epochs_Target.drop(ixEpochs2Remove,verbose=False)




Evoked_NoTarget  = Epochs_NoTarget['NoTarget'].average()
Evoked_Target  = Epochs_Target['Target'].average()

X = [Epochs_NoTarget['NoTarget'].get_data().transpose(0, 2, 1), Epochs_Target['Target'].get_data().transpose(0, 2, 1)]
# organize data for plotting
colors_config = {"Target": "r", "NoTarget": 'k'}
styles_config ={"Target": {"linewidth": 1.75},"NoTarget": {"linewidth": 1.75}}

evokeds = {'NoTarget':Evoked_NoTarget,'Target':Evoked_Target}
p_accept = 0.05
fig_2D = mne_tools.SpatTemp_TFCE_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)
fig_2D[0].suptitle( '2D  -  Target vs NoTarget')

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
fig_2D[0].canvas.manager.window.showMaximized()



Evoked_DiffConfig = mne.EvokedArray(Evoked_Target.get_data()-Evoked_NoTarget.get_data(), Evoked_Target.info)
times = np.arange(0.05, 0.500, 0.025)
Evoked_DiffConfig.plot_topomap(times, ch_type="eeg")


















