# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 16:40:52 2023

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
import scipy

RootFolder =  os.path.split(RootAnalysisFolder)[0]

RootDirectory_evokedData = RootFolder + '/_fifData/evokeds/'
RootDirectory_Results = RootFolder + '/results/'



# ------------    Concatenate evoked data for each subject

#    --  S1 System - Target responses
List_ave_S1_Target =  glob.glob(RootDirectory_evokedData + '/*S1_Target-ave.fif', recursive=True)
NbFiles = len(List_ave_S1_Target)
Evokeds_Target_S1 = []
NbChan = mne.read_evokeds(List_ave_S1_Target[0], verbose=False)[0].info['nchan']
NbSamp = np.size(mne.read_evokeds(List_ave_S1_Target[0], verbose=False)[0].times)
DataConcat_evokeds_Target_S1 = np.zeros((NbFiles,NbChan,NbSamp))

for i_files in range(NbFiles):
	File_curr = List_ave_S1_Target[i_files]
	evoked_curr = mne.read_evokeds(File_curr)[0]
	Evokeds_Target_S1.append(evoked_curr)
	DataConcat_evokeds_Target_S1[i_files,:,:]=evoked_curr.data



#    --  S2 System - Target responses
List_ave_S2_Target =  glob.glob(RootDirectory_evokedData + '/*S2_Target-ave.fif', recursive=True)
NbFiles = len(List_ave_S2_Target)
Evokeds_Target_S2 = []
NbChan = mne.read_evokeds(List_ave_S2_Target[0], verbose=False)[0].info['nchan']
NbSamp = np.size(mne.read_evokeds(List_ave_S2_Target[0], verbose=False)[0].times)
DataConcat_evokeds_Target_S2 = np.zeros((NbFiles,NbChan,NbSamp))

for i_files in range(NbFiles):
	File_curr = List_ave_S2_Target[i_files]
	evoked_curr = mne.read_evokeds(File_curr)[0]
	Evokeds_Target_S2.append(evoked_curr)
	DataConcat_evokeds_Target_S2[i_files,:,:]=evoked_curr.data



#    --  S3 System - Target responses
List_ave_S3_Target =  glob.glob(RootDirectory_evokedData + '/*S3_Target-ave.fif', recursive=True)
NbFiles = len(List_ave_S3_Target)
Evokeds_Target_S3 = []
NbChan = mne.read_evokeds(List_ave_S3_Target[0], verbose=False)[0].info['nchan']
NbSamp = np.size(mne.read_evokeds(List_ave_S3_Target[0], verbose=False)[0].times)
DataConcat_evokeds_Target_S3 = np.zeros((NbFiles,NbChan,NbSamp))

for i_files in range(NbFiles):
	File_curr = List_ave_S3_Target[i_files]
	evoked_curr = mne.read_evokeds(File_curr)[0]
	Evokeds_Target_S3.append(evoked_curr)
	DataConcat_evokeds_Target_S3[i_files,:,:]=evoked_curr.data




#    --  S1 System - NoTarget responses
List_ave_S1_NoTarget =  glob.glob(RootDirectory_evokedData + '/*S1_NoTarget-ave.fif', recursive=True)
NbFiles = len(List_ave_S1_NoTarget)
Evokeds_NoTarget_S1 = []
NbChan = mne.read_evokeds(List_ave_S1_NoTarget[0], verbose=False)[0].info['nchan']
NbSamp = np.size(mne.read_evokeds(List_ave_S1_NoTarget[0], verbose=False)[0].times)
DataConcat_evokeds_NoTarget_S1 = np.zeros((NbFiles,NbChan,NbSamp))

for i_files in range(NbFiles):
	File_curr = List_ave_S1_NoTarget[i_files]
	evoked_curr = mne.read_evokeds(File_curr)[0]
	Evokeds_NoTarget_S1.append(evoked_curr)
	DataConcat_evokeds_NoTarget_S1[i_files,:,:]=evoked_curr.data



#    --  S2 System - NoTarget responses
List_ave_S2_NoTarget =  glob.glob(RootDirectory_evokedData + '/*S2_NoTarget-ave.fif', recursive=True)
NbFiles = len(List_ave_S2_NoTarget)
Evokeds_NoTarget_S2 = []
NbChan = mne.read_evokeds(List_ave_S2_NoTarget[0], verbose=False)[0].info['nchan']
NbSamp = np.size(mne.read_evokeds(List_ave_S2_NoTarget[0], verbose=False)[0].times)
DataConcat_evokeds_NoTarget_S2 = np.zeros((NbFiles,NbChan,NbSamp))

for i_files in range(NbFiles):
	File_curr = List_ave_S2_NoTarget[i_files]
	evoked_curr = mne.read_evokeds(File_curr)[0]
	Evokeds_NoTarget_S2.append(evoked_curr)
	DataConcat_evokeds_NoTarget_S2[i_files,:,:]=evoked_curr.data



#    --  S3 System - NoTarget responses
List_ave_S3_NoTarget =  glob.glob(RootDirectory_evokedData + '/*S3_NoTarget-ave.fif', recursive=True)
NbFiles = len(List_ave_S3_NoTarget)
Evokeds_NoTarget_S3 = []
NbChan = mne.read_evokeds(List_ave_S3_NoTarget[0], verbose=False)[0].info['nchan']
NbSamp = np.size(mne.read_evokeds(List_ave_S3_NoTarget[0], verbose=False)[0].times)
DataConcat_evokeds_NoTarget_S3 = np.zeros((NbFiles,NbChan,NbSamp))

for i_files in range(NbFiles):
	File_curr = List_ave_S3_NoTarget[i_files]
	evoked_curr = mne.read_evokeds(File_curr)[0]
	Evokeds_NoTarget_S3.append(evoked_curr)
	DataConcat_evokeds_NoTarget_S3[i_files,:,:]=evoked_curr.data



# Compute Grand average ok eveoked data across subjects

GrandEvoked_Target_S1    =  mne.grand_average(Evokeds_Target_S1)
GrandEvoked_NoTarget_S1  =  mne.grand_average(Evokeds_NoTarget_S1)
GrandEvoked_Target_S2    =  mne.grand_average(Evokeds_Target_S2)
GrandEvoked_NoTarget_S2  =  mne.grand_average(Evokeds_NoTarget_S2)
GrandEvoked_Target_S3    =  mne.grand_average(Evokeds_Target_S3)
GrandEvoked_NoTarget_S3  =  mne.grand_average(Evokeds_NoTarget_S3)



# ---------------------------------------------------------------
#  -----------------      Target vs No Target Evaluation
# ---------------------------------------------------------------

#   --       System S1       --
X = [DataConcat_evokeds_NoTarget_S1.transpose(0, 2, 1), DataConcat_evokeds_Target_S1.transpose(0, 2, 1)]
# organize data for plotting
colors_config = {"Target": "r", "NoTarget": 'k'}
styles_config ={"Target": {"linewidth": 0.75},"NoTarget": {"linewidth": 0.75}}

evokeds = {'NoTarget':GrandEvoked_NoTarget_S1,'Target':GrandEvoked_Target_S1}
p_accept = 0.05
fig_S1 = mne_tools.SpatTemp_TFCE_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)
fig_S1[0].suptitle( 'S1  -  Target vs NoTarget')

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
# fig_S1[0].savefig( RootDirectory_Results + 'GROUP.S1.TargvsNoTarg.png',dpi=400, bbox_inches='tight')
fig_S1[0].canvas.manager.window.showMaximized()


#   --       System S2       --
X = [DataConcat_evokeds_NoTarget_S2.transpose(0, 2, 1), DataConcat_evokeds_Target_S2.transpose(0, 2, 1)]
# organize data for plotting
colors_config = {"Target": "r", "NoTarget": 'k'}
styles_config ={"Target": {"linewidth": 0.75},"NoTarget": {"linewidth": 0.75}}

evokeds = {'NoTarget':GrandEvoked_NoTarget_S2,'Target':GrandEvoked_Target_S2}
p_accept = 0.05
fig_S2 = mne_tools.SpatTemp_TFCE_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)
fig_S2[0].suptitle( 'S2  -  Target vs NoTarget')

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
# fig_S2[0].savefig( RootDirectory_Results + 'GROUP.S2.TargvsNoTarg.png',dpi=400, bbox_inches='tight')
fig_S2[0].canvas.manager.window.showMaximized()




#   --       System S3       --
X = [DataConcat_evokeds_NoTarget_S3.transpose(0, 2, 1), DataConcat_evokeds_Target_S3.transpose(0, 2, 1)]
# organize data for plotting
colors_config = {"Target": "r", "NoTarget": 'k'}
styles_config ={"Target": {"linewidth": 0.75},"NoTarget": {"linewidth": 0.75}}

evokeds = {'NoTarget':GrandEvoked_NoTarget_S3,'Target':GrandEvoked_Target_S3}
p_accept = 0.05
fig_S3 = mne_tools.SpatTemp_TFCE_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)
fig_S3[0].suptitle( 'S3  -  Target vs NoTarget')

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
# fig_S3[0].savefig( RootDirectory_Results + 'GROUP.S3.TargvsNoTarg.png',dpi=400, bbox_inches='tight')
fig_S3[0].canvas.manager.window.showMaximized()






# -------------------------------------------------------------------------
#   -----------------      COMPARE S1 and S2 Systems  on  Target Responses
# -------------------------------------------------------------------------

List_01 = GrandEvoked_Target_S1.info['ch_names']
List_02 = GrandEvoked_Target_S2.info['ch_names']

List_ChanComm = [value for value in List_01 if value in List_02]

GrandEvoked_Target_S1.pick_channels(List_ChanComm)
GrandEvoked_Target_S2.pick_channels(List_ChanComm)

if (GrandEvoked_Target_S1.info['sfreq'] > GrandEvoked_Target_S2.info['sfreq']):
	GrandEvoked_Target_S2.resample(GrandEvoked_Target_S1.info['sfreq'])
if (GrandEvoked_Target_S1.info['sfreq'] < GrandEvoked_Target_S2.info['sfreq']):
	GrandEvoked_Target_S1.resample(GrandEvoked_Target_S2.info['sfreq'])
	
	
	
#    Align epoch data with the same time windows of interest
if (len(GrandEvoked_Target_S1.times) > len(GrandEvoked_Target_S2.times)):
	GrandEvoked_Target_S1.crop(0,GrandEvoked_Target_S2.times[-1])

if (len(GrandEvoked_Target_S2.times) > len(GrandEvoked_Target_S1.times)):
	GrandEvoked_Target_S2.crop(0,GrandEvoked_Target_S1.times[-1])
	
	
NbSamp = np.max((DataConcat_evokeds_Target_S1.shape[2],DataConcat_evokeds_Target_S2.shape[2]))
if (DataConcat_evokeds_Target_S1.shape[2]<NbSamp):
	DataConcat_evokeds_Target_S1 = scipy.signal.resample(DataConcat_evokeds_Target_S1, NbSamp, axis=2)	
if (DataConcat_evokeds_Target_S2.shape[2]<NbSamp):
	DataConcat_evokeds_Target_S2 = scipy.signal.resample(DataConcat_evokeds_Target_S2, NbSamp, axis=2)	



X = [DataConcat_evokeds_Target_S1.transpose(0, 2, 1), DataConcat_evokeds_Target_S2.transpose(0, 2, 1)]
# organize data for plotting
colors_config = {"S1": "r", "S2": 'k'}
styles_config ={"S1": {"linewidth": 2.75},"S2": {"linewidth": 2.75}}

evokeds = {'S1':GrandEvoked_Target_S1,'S2':GrandEvoked_Target_S2}
p_accept = 0.05
fig_T_S1S2 = mne_tools.PermutCluster_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)
fig_T_S1S2[0].suptitle( 'Target Responses S1 vs S2')

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
# fig_2D[0].savefig( RootDirectory_Results + 'GROUP.Target.S1vsS2.png',dpi=400, bbox_inches='tight')
fig_T_S1S2[0].canvas.manager.window.showMaximized()





# -------------------------------------------------------------------------
#   -----------------      COMPARE S1 and S3 Systems  on  Target Responses
# -------------------------------------------------------------------------

List_01 = GrandEvoked_Target_S1.info['ch_names']
List_02 = GrandEvoked_Target_S3.info['ch_names']

List_ChanComm = [value for value in List_01 if value in List_02]

GrandEvoked_Target_S1.pick_channels(List_ChanComm)
GrandEvoked_Target_S3.pick_channels(List_ChanComm)

if (GrandEvoked_Target_S1.info['sfreq'] > GrandEvoked_Target_S3.info['sfreq']):
	GrandEvoked_Target_S3.resample(GrandEvoked_Target_S1.info['sfreq'])
if (GrandEvoked_Target_S1.info['sfreq'] < GrandEvoked_Target_S3.info['sfreq']):
	GrandEvoked_Target_S1.resample(GrandEvoked_Target_S3.info['sfreq'])
	
	
	
#    Align epoch data with the same time windows of interest
if (len(GrandEvoked_Target_S1.times) > len(GrandEvoked_Target_S3.times)):
	GrandEvoked_Target_S1.crop(0,GrandEvoked_Target_S3.times[-1])

if (len(GrandEvoked_Target_S3.times) > len(GrandEvoked_Target_S1.times)):
	GrandEvoked_Target_S3.crop(0,GrandEvoked_Target_S1.times[-1])
	
	
NbSamp = np.max((DataConcat_evokeds_Target_S1.shape[2],DataConcat_evokeds_Target_S3.shape[2]))
if (DataConcat_evokeds_Target_S1.shape[2]<NbSamp):
	DataConcat_evokeds_Target_S1 = scipy.signal.resample(DataConcat_evokeds_Target_S1, NbSamp, axis=2)	
if (DataConcat_evokeds_Target_S3.shape[2]<NbSamp):
	DataConcat_evokeds_Target_S3 = scipy.signal.resample(DataConcat_evokeds_Target_S3, NbSamp, axis=2)	



X = [DataConcat_evokeds_Target_S1.transpose(0, 2, 1), DataConcat_evokeds_Target_S3.transpose(0, 2, 1)]
# organize data for plotting
colors_config = {"S1": "r", "S3": 'g'}
styles_config ={"S1": {"linewidth": 2.75},"S3": {"linewidth": 2.75}}

evokeds = {'S1':GrandEvoked_Target_S1,'S3':GrandEvoked_Target_S3}
p_accept = 0.05
fig_T_S1S3 = mne_tools.PermutCluster_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)
fig_T_S1S3[0].suptitle( 'Target Responses S1 vs S3')

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
# fig_2D[0].savefig( RootDirectory_Results + 'GROUP.Target.S1vsS3.png',dpi=400, bbox_inches='tight')
fig_T_S1S3[0].canvas.manager.window.showMaximized()






# -------------------------------------------------------------------------
#   -----------------      COMPARE S2 and S3 Systems  on  Target Responses
# -------------------------------------------------------------------------

List_01 = GrandEvoked_Target_S2.info['ch_names']
List_02 = GrandEvoked_Target_S3.info['ch_names']

List_ChanComm = [value for value in List_01 if value in List_02]

GrandEvoked_Target_S2.pick_channels(List_ChanComm)
GrandEvoked_Target_S3.pick_channels(List_ChanComm)

if (GrandEvoked_Target_S2.info['sfreq'] > GrandEvoked_Target_S3.info['sfreq']):
	GrandEvoked_Target_S3.resample(GrandEvoked_Target_S2.info['sfreq'])
if (GrandEvoked_Target_S2.info['sfreq'] < GrandEvoked_Target_S3.info['sfreq']):
	GrandEvoked_Target_S2.resample(GrandEvoked_Target_S3.info['sfreq'])
	
	
	
#    Align epoch data with the same time windows of interest
if (len(GrandEvoked_Target_S2.times) > len(GrandEvoked_Target_S3.times)):
	GrandEvoked_Target_S2.crop(0,GrandEvoked_Target_S3.times[-1])

if (len(GrandEvoked_Target_S3.times) > len(GrandEvoked_Target_S2.times)):
	GrandEvoked_Target_S3.crop(0,GrandEvoked_Target_S2.times[-1])
	
	
NbSamp = np.max((DataConcat_evokeds_Target_S2.shape[2],DataConcat_evokeds_Target_S3.shape[2]))
if (DataConcat_evokeds_Target_S2.shape[2]<NbSamp):
	DataConcat_evokeds_Target_S2 = scipy.signal.resample(DataConcat_evokeds_Target_S2, NbSamp, axis=2)	
if (DataConcat_evokeds_Target_S3.shape[2]<NbSamp):
	DataConcat_evokeds_Target_S3 = scipy.signal.resample(DataConcat_evokeds_Target_S3, NbSamp, axis=2)	



X = [DataConcat_evokeds_Target_S2.transpose(0, 2, 1), DataConcat_evokeds_Target_S3.transpose(0, 2, 1)]
# organize data for plotting
colors_config = {"S2": "k", "S3": 'g'}
styles_config ={"S2": {"linewidth": 2.75},"S3": {"linewidth": 2.75}}

evokeds = {'S2':GrandEvoked_Target_S2,'S3':GrandEvoked_Target_S3}
p_accept = 0.05
fig_T_S2S3 = mne_tools.PermutCluster_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)
fig_T_S2S3[0].suptitle( 'Target Responses S2 vs S3')

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
# fig_2D[0].savefig( RootDirectory_Results + 'GROUP.Target.S2vsS3.png',dpi=400, bbox_inches='tight')
fig_T_S2S3[0].canvas.manager.window.showMaximized()
















# -------------------------------------------------------------------------
#   -----------------      COMPARE S1 and S2 Systems  on  No Target Responses
# -------------------------------------------------------------------------

List_01 = GrandEvoked_NoTarget_S1.info['ch_names']
List_02 = GrandEvoked_NoTarget_S2.info['ch_names']

List_ChanComm = [value for value in List_01 if value in List_02]

GrandEvoked_NoTarget_S1.pick_channels(List_ChanComm)
GrandEvoked_NoTarget_S2.pick_channels(List_ChanComm)

if (GrandEvoked_NoTarget_S1.info['sfreq'] > GrandEvoked_NoTarget_S2.info['sfreq']):
	GrandEvoked_NoTarget_S2.resample(GrandEvoked_NoTarget_S1.info['sfreq'])
if (GrandEvoked_NoTarget_S1.info['sfreq'] < GrandEvoked_NoTarget_S2.info['sfreq']):
	GrandEvoked_NoTarget_S1.resample(GrandEvoked_NoTarget_S2.info['sfreq'])
	
	
	
#    Align epoch data with the same time windows of interest
if (len(GrandEvoked_NoTarget_S1.times) > len(GrandEvoked_NoTarget_S2.times)):
	GrandEvoked_NoTarget_S1.crop(0,GrandEvoked_NoTarget_S2.times[-1])

if (len(GrandEvoked_NoTarget_S2.times) > len(GrandEvoked_NoTarget_S1.times)):
	GrandEvoked_NoTarget_S2.crop(0,GrandEvoked_NoTarget_S1.times[-1])
	
	
NbSamp = np.max((DataConcat_evokeds_NoTarget_S1.shape[2],DataConcat_evokeds_NoTarget_S2.shape[2]))
if (DataConcat_evokeds_NoTarget_S1.shape[2]<NbSamp):
	DataConcat_evokeds_NoTarget_S1 = scipy.signal.resample(DataConcat_evokeds_NoTarget_S1, NbSamp, axis=2)	
if (DataConcat_evokeds_NoTarget_S2.shape[2]<NbSamp):
	DataConcat_evokeds_NoTarget_S2 = scipy.signal.resample(DataConcat_evokeds_NoTarget_S2, NbSamp, axis=2)	



X = [DataConcat_evokeds_NoTarget_S1.transpose(0, 2, 1), DataConcat_evokeds_NoTarget_S2.transpose(0, 2, 1)]
# organize data for plotting
colors_config = {"S1": "r", "S2": 'k'}
styles_config ={"S1": {"linewidth": 0.75},"S2": {"linewidth": 0.75}}

evokeds = {'S1':GrandEvoked_NoTarget_S1,'S2':GrandEvoked_NoTarget_S2}
p_accept = 0.05
fig_T_S1S2 = mne_tools.PermutCluster_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)
fig_T_S1S2[0].suptitle( 'NoTarget Responses S1 vs S2')

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
# fig_2D[0].savefig( RootDirectory_Results + 'GROUP.NoTarget.S1vsS2.png',dpi=400, bbox_inches='tight')
fig_T_S1S2[0].canvas.manager.window.showMaximized()





# -------------------------------------------------------------------------
#   -----------------      COMPARE S1 and S3 Systems  on  NoTarget Responses
# -------------------------------------------------------------------------

List_01 = GrandEvoked_NoTarget_S1.info['ch_names']
List_02 = GrandEvoked_NoTarget_S3.info['ch_names']

List_ChanComm = [value for value in List_01 if value in List_02]

GrandEvoked_NoTarget_S1.pick_channels(List_ChanComm)
GrandEvoked_NoTarget_S3.pick_channels(List_ChanComm)

if (GrandEvoked_NoTarget_S1.info['sfreq'] > GrandEvoked_NoTarget_S3.info['sfreq']):
	GrandEvoked_NoTarget_S3.resample(GrandEvoked_NoTarget_S1.info['sfreq'])
if (GrandEvoked_NoTarget_S1.info['sfreq'] < GrandEvoked_NoTarget_S3.info['sfreq']):
	GrandEvoked_NoTarget_S1.resample(GrandEvoked_NoTarget_S3.info['sfreq'])
	
	
	
#    Align epoch data with the same time windows of interest
if (len(GrandEvoked_NoTarget_S1.times) > len(GrandEvoked_NoTarget_S3.times)):
	GrandEvoked_NoTarget_S1.crop(0,GrandEvoked_NoTarget_S3.times[-1])

if (len(GrandEvoked_NoTarget_S3.times) > len(GrandEvoked_NoTarget_S1.times)):
	GrandEvoked_NoTarget_S3.crop(0,GrandEvoked_NoTarget_S1.times[-1])
	
	
NbSamp = np.max((DataConcat_evokeds_NoTarget_S1.shape[2],DataConcat_evokeds_NoTarget_S3.shape[2]))
if (DataConcat_evokeds_NoTarget_S1.shape[2]<NbSamp):
	DataConcat_evokeds_NoTarget_S1 = scipy.signal.resample(DataConcat_evokeds_NoTarget_S1, NbSamp, axis=2)	
if (DataConcat_evokeds_NoTarget_S3.shape[2]<NbSamp):
	DataConcat_evokeds_NoTarget_S3 = scipy.signal.resample(DataConcat_evokeds_NoTarget_S3, NbSamp, axis=2)	



X = [DataConcat_evokeds_NoTarget_S1.transpose(0, 2, 1), DataConcat_evokeds_NoTarget_S3.transpose(0, 2, 1)]
# organize data for plotting
colors_config = {"S1": "r", "S3": 'g'}
styles_config ={"S1": {"linewidth": 0.75},"S3": {"linewidth": 0.75}}

evokeds = {'S1':GrandEvoked_NoTarget_S1,'S3':GrandEvoked_NoTarget_S3}
p_accept = 0.05
fig_T_S1S3 = mne_tools.PermutCluster_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)
fig_T_S1S3[0].suptitle( 'NoTarget Responses S1 vs S3')

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
# fig_2D[0].savefig( RootDirectory_Results + 'GROUP.NoTarget.S1vsS3.png',dpi=400, bbox_inches='tight')
fig_T_S1S3[0].canvas.manager.window.showMaximized()






# -------------------------------------------------------------------------
#   -----------------      COMPARE S2 and S3 Systems  on  NoTarget Responses
# -------------------------------------------------------------------------

List_01 = GrandEvoked_NoTarget_S2.info['ch_names']
List_02 = GrandEvoked_NoTarget_S3.info['ch_names']

List_ChanComm = [value for value in List_01 if value in List_02]

GrandEvoked_NoTarget_S2.pick_channels(List_ChanComm)
GrandEvoked_NoTarget_S3.pick_channels(List_ChanComm)

if (GrandEvoked_NoTarget_S2.info['sfreq'] > GrandEvoked_NoTarget_S3.info['sfreq']):
	GrandEvoked_NoTarget_S3.resample(GrandEvoked_NoTarget_S2.info['sfreq'])
if (GrandEvoked_NoTarget_S2.info['sfreq'] < GrandEvoked_NoTarget_S3.info['sfreq']):
	GrandEvoked_NoTarget_S2.resample(GrandEvoked_NoTarget_S3.info['sfreq'])
	
	
	
#    Align epoch data with the same time windows of interest
if (len(GrandEvoked_NoTarget_S2.times) > len(GrandEvoked_NoTarget_S3.times)):
	GrandEvoked_NoTarget_S2.crop(0,GrandEvoked_NoTarget_S3.times[-1])

if (len(GrandEvoked_NoTarget_S3.times) > len(GrandEvoked_NoTarget_S2.times)):
	GrandEvoked_NoTarget_S3.crop(0,GrandEvoked_NoTarget_S2.times[-1])
	
	
NbSamp = np.max((DataConcat_evokeds_NoTarget_S2.shape[2],DataConcat_evokeds_NoTarget_S3.shape[2]))
if (DataConcat_evokeds_NoTarget_S2.shape[2]<NbSamp):
	DataConcat_evokeds_NoTarget_S2 = scipy.signal.resample(DataConcat_evokeds_NoTarget_S2, NbSamp, axis=2)	
if (DataConcat_evokeds_NoTarget_S3.shape[2]<NbSamp):
	DataConcat_evokeds_NoTarget_S3 = scipy.signal.resample(DataConcat_evokeds_NoTarget_S3, NbSamp, axis=2)	



X = [DataConcat_evokeds_NoTarget_S2.transpose(0, 2, 1), DataConcat_evokeds_NoTarget_S3.transpose(0, 2, 1)]
# organize data for plotting
colors_config = {"S2": "k", "S3": 'g'}
styles_config ={"S2": {"linewidth": 0.75},"S3": {"linewidth": 0.75}}

evokeds = {'S2':GrandEvoked_NoTarget_S2,'S3':GrandEvoked_NoTarget_S3}
p_accept = 0.05
fig_T_S2S3 = mne_tools.PermutCluster_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)
fig_T_S2S3[0].suptitle( 'NoTarget Responses S2 vs S3')

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
# fig_2D[0].savefig( RootDirectory_Results + 'GROUP.NoTarget.S2vsS3.png',dpi=400, bbox_inches='tight')
fig_T_S2S3[0].canvas.manager.window.showMaximized()














