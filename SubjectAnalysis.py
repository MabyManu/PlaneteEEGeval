# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 11:39:51 2023

@author: manum
"""

import os 
import glob
RootAnalysisFolder = os.path.split(__file__)[0]
from os import chdir
chdir(RootAnalysisFolder)
import mne
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFileDialog

from AddPyABA_Path import PyABA_path
import sys
 
sys.path.append(PyABA_path)

import pyABA_algorithms,mne_tools
from mne.channels import combine_channels

from mne.stats import permutation_cluster_test,f_threshold_mway_rm

import numpy as np
rejection_rate = 0.15

RootFolder =  os.path.split(RootAnalysisFolder)[0]

RootDirectory_RAW = RootFolder + '/_fifData/epochs/'
RootDirectory_evokedData = RootFolder + '/_fifData/evokeds/'
RootDirectory_Results = RootFolder + '/results/'

Listfilename = QFileDialog.getOpenFileNames( caption='Select 2 *.FIF files',
                                                    directory=RootDirectory_RAW,
                                                    filter='*.2D.*Calib*-Target-epo.fif')[0]

ListEpoch_target = []
ListEpoch_Notarget = []
ListConfig=[]
for i_file in range (len(Listfilename)):
	Global_filename_curr = Listfilename[i_file]
	filename_curr = os.path.split(Global_filename_curr)[1]
	ix_2D = filename_curr.find('.2D')
	NameSubject = filename_curr[0:ix_2D-3]
	Config = filename_curr[ix_2D-2:ix_2D]
	ListConfig.append(Config)
	List_Files_Suj = glob.glob(Global_filename_curr[0:-23] + '.*-epo.fif')
	for i_file in range (len(List_Files_Suj)):
		filecurr= List_Files_Suj[i_file]

		if '-NoTarget-epo.fif' in filecurr:
			EpochNotarget_curr = mne.read_epochs(filecurr)
			EpochNotarget_curr.pick(mne.pick_types(EpochNotarget_curr.info, meg=False, eeg=True,misc=False))
			ThresholdPeak2peak,_,_,ixEpochs2Remove,_ = mne_tools.RejectThresh(EpochNotarget_curr,int(rejection_rate*100))
			EpochNotarget_curr.drop(ixEpochs2Remove,verbose=False)			
			Evoked_NT_curr = EpochNotarget_curr.average()
			NoTarget_evoFilename = RootDirectory_evokedData + NameSubject + '_' + Config + '_NoTarget-ave.fif'
			Evoked_NT_curr.save(NoTarget_evoFilename,overwrite=True)
			
			ListEpoch_Notarget.append(EpochNotarget_curr)
	
		else:
			Epochtarget_curr = mne.read_epochs(filecurr)
			Epochtarget_curr.pick(mne.pick_types(Epochtarget_curr.info, meg=False, eeg=True,misc=False))
			ThresholdPeak2peak,_,_,ixEpochs2Remove,_ = mne_tools.RejectThresh(Epochtarget_curr,int(rejection_rate*100))
			Epochtarget_curr.drop(ixEpochs2Remove,verbose=False)		
			Evoked_T_curr = Epochtarget_curr.average()
			Target_evoFilename = RootDirectory_evokedData + NameSubject + '_' + Config + '_Target-ave.fif'
			Evoked_T_curr.save(Target_evoFilename,overwrite=True)
			
			ListEpoch_target.append(Epochtarget_curr)
		





# ---------- Comparison Target No Target Responses

for i_Config in range(len(ListConfig)):
	Epoch_T_Curr= ListEpoch_target[i_Config]
	Epoch_NT_Curr= ListEpoch_Notarget[i_Config]
	
	sphere = mne.make_sphere_model('auto', 'auto', Epoch_T_Curr.info, verbose=0)
	src = mne.setup_volume_source_space(sphere=sphere,exclude=30.,pos=15.,verbose=0)
	forward = mne.make_forward_solution(Epoch_T_Curr.info,trans=None,src=src,bem=sphere,verbose=0)
	
	Epoch_T_Curr_rest,_ = mne.set_eeg_reference(Epoch_T_Curr,'REST', forward=forward)
	Epoch_NT_Curr_rest,_ = mne.set_eeg_reference(Epoch_NT_Curr,'REST', forward=forward)
	
	Evoked_NT_Curr_rest = Epoch_NT_Curr_rest['NoTarget'].average()
	Evoked_T_Curr_rest = Epoch_T_Curr_rest['Target'].average()
	
	
	X = [Epoch_NT_Curr_rest['NoTarget'].get_data().transpose(0, 2, 1), Epoch_T_Curr_rest['Target'].get_data().transpose(0, 2, 1)]
	# organize data for plotting
	colors_config = {"Target": "r", "NoTarget": 'k'}
	styles_config ={"Target": {"linewidth": 1},"NoTarget": {"linewidth": 1}}

	evokeds = {'NoTarget':Evoked_NT_Curr_rest,'Target':Evoked_T_Curr_rest}
	p_accept = 0.05
	fig_TvsNT = mne_tools.SpatTemp_TFCE_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)
	fig_TvsNT[0].suptitle( NameSubject + ' - System ' + ListConfig[i_Config] + ' -  Target vs NoTarget')

	manager = plt.get_current_fig_manager()
	manager.full_screen_toggle()
	fig_TvsNT[0].savefig( RootDirectory_Results + NameSubject + '.' + ListConfig[i_Config] +  '.TargvsNoTarg.png',dpi=400, bbox_inches='tight')
	fig_TvsNT[0].canvas.manager.window.showMaximized()
		
	Evoked_DiffConfig = mne.EvokedArray(Evoked_T_Curr_rest.get_data()-Evoked_NT_Curr_rest.get_data(), Evoked_NT_Curr_rest.info)
	times = np.arange(0.05, 0.500, 0.025)
	Evoked_DiffConfig.plot_topomap(times, ch_type="eeg")


# ---------- Comparison Systems on Target Responses
ListEpoch_T = []
for i_Config in range(len(ListConfig)):
	sphere = mne.make_sphere_model('auto', 'auto', ListEpoch_target[i_Config].info, verbose=0)
	src = mne.setup_volume_source_space(sphere=sphere,exclude=30.,pos=15.,verbose=0)
	forward = mne.make_forward_solution(ListEpoch_target[i_Config].info,trans=None,src=src,bem=sphere,verbose=0)
	Epoch_T_Curr_rest, _= mne.set_eeg_reference(ListEpoch_target[i_Config],'REST', forward=forward)
	ListEpoch_T.append(Epoch_T_Curr_rest)
	

#    Align epoch data with the same sampling frequency
if (ListEpoch_T[0].info['sfreq'] > ListEpoch_T[1].info['sfreq']):
	ListEpoch_T[1].resample(ListEpoch_T[0].info['sfreq'])
if (ListEpoch_T[0].info['sfreq'] < ListEpoch_T[1].info['sfreq']):
	ListEpoch_T[0].resample(ListEpoch_T[1].info['sfreq'])


 
#    Align epoch data with the same time windows of interest
if (len(ListEpoch_T[0].times) > len(ListEpoch_T[1].times)):
	ListEpoch_T[0].crop(0,ListEpoch_T[1].times[-1])

if (len(ListEpoch_T[1].times) > len(ListEpoch_T[0].times)):
	ListEpoch_T[1].crop(0,ListEpoch_T[0].times[-1])

#    Align epoch data with the same channels
List_01 = ListEpoch_T[0].info['ch_names']
List_02 = ListEpoch_T[1].info['ch_names']
List_ChanComm = [value for value in List_01 if value in List_02]
ListEpoch_T[0].pick_channels(List_ChanComm)
ListEpoch_T[1].pick_channels(List_ChanComm)

#    Align epoch data with the same order of channels
Data_Epoch_T_1 = np.zeros((ListEpoch_T[1]['Target'].get_data().transpose(0, 2, 1).shape))

for i_chan in range(ListEpoch_T[0]['Target'].info['nchan']):
	ChannelNameCurr = ListEpoch_T[0]['Target'].info['ch_names'][i_chan]
	epoch_curr= ListEpoch_T[1]['Target'].pick_channels([ChannelNameCurr])
	Data_Epoch_T_1[:,:,i_chan] = np.squeeze(epoch_curr.get_data())
Epoch_T_1 = mne.EpochsArray(Data_Epoch_T_1.transpose(0, 2, 1),ListEpoch_T[0]['Target'].info)	




X = [ListEpoch_T[0]['Target'].get_data().transpose(0, 2, 1), Data_Epoch_T_1]
Evoked_T_01 = ListEpoch_T[0]['Target'].average()
Evoked_T_02 = Epoch_T_1.average()


# organize data for plotting
colors_config = {ListConfig[0]: "tomato", ListConfig[1]: 'green'}
styles_config ={ListConfig[0]: {"linewidth": 1.5},ListConfig[1]: {"linewidth": 1.5}}

evokeds = {ListConfig[0]:Evoked_T_01,ListConfig[1]:Evoked_T_02}
p_accept = 0.05
fig_Targ = mne_tools.SpatTemp_TFCE_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)

fig_Targ[0].suptitle( 'Target evoked Responses - ' + ListConfig[0] + ' vs ' + ListConfig[1])
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
fig_Targ[0].savefig( RootDirectory_Results + NameSubject + '.' +  'Targ_'+ ListConfig[0] + 'vs' + ListConfig[1] + '.png',dpi=400, bbox_inches='tight')
fig_Targ[0].canvas.manager.window.showMaximized()


Evoked_DiffConfig = mne.EvokedArray(Evoked_T_02.get_data()-Evoked_T_01.get_data(),Evoked_T_01.info)
times = np.arange(0.05, 0.500, 0.025)
Evoked_DiffConfig.plot_topomap(times, ch_type="eeg")







# ---------- Comparison Systems on No Target Responses
ListEpoch_NT = []
for i_Config in range(len(ListConfig)):
	sphere = mne.make_sphere_model('auto', 'auto', ListEpoch_Notarget[i_Config].info, verbose=0)
	src = mne.setup_volume_source_space(sphere=sphere,exclude=30.,pos=15.,verbose=0)
	forward = mne.make_forward_solution(ListEpoch_Notarget[i_Config].info,trans=None,src=src,bem=sphere,verbose=0)
	Epoch_NT_Curr_rest, _= mne.set_eeg_reference(ListEpoch_Notarget[i_Config],'REST', forward=forward)
	ListEpoch_NT.append(Epoch_NT_Curr_rest)
	

#    Align epoch data with the same sampling frequency
if (ListEpoch_NT[0].info['sfreq'] > ListEpoch_NT[1].info['sfreq']):
	ListEpoch_NT[1].resample(ListEpoch_NT[0].info['sfreq'])
if (ListEpoch_NT[0].info['sfreq'] < ListEpoch_NT[1].info['sfreq']):
	ListEpoch_NT[0].resample(ListEpoch_NT[1].info['sfreq'])

#    Align epoch data with the same time windows of interest
if (len(ListEpoch_NT[0].times) > len(ListEpoch_NT[1].times)):
	ListEpoch_NT[0].crop(0,ListEpoch_NT[1].times[-1])

if (len(ListEpoch_NT[1].times) > len(ListEpoch_NT[0].times)):
	ListEpoch_NT[1].crop(0,ListEpoch_NT[0].times[-1])

#    Align epoch data with the same channels
List_01 = ListEpoch_NT[0].info['ch_names']
List_02 = ListEpoch_NT[1].info['ch_names']

List_ChanComm = [value for value in List_01 if value in List_02]

ListEpoch_NT[0].pick_channels(List_ChanComm)
ListEpoch_NT[1].pick_channels(List_ChanComm)



#    Align epoch data with the same order of channels
Data_Epoch_NT_1 = np.zeros((ListEpoch_NT[1]['NoTarget'].get_data().transpose(0, 2, 1).shape))

for i_chan in range(ListEpoch_NT[0]['NoTarget'].info['nchan']):
	ChannelNameCurr = ListEpoch_NT[0]['NoTarget'].info['ch_names'][i_chan]
	epoch_curr= ListEpoch_NT[1]['NoTarget'].pick_channels([ChannelNameCurr])
	Data_Epoch_NT_1[:,:,i_chan] = np.squeeze(epoch_curr.get_data())
Epoch_NT_1 = mne.EpochsArray(Data_Epoch_NT_1.transpose(0, 2, 1),ListEpoch_NT[0]['NoTarget'].info)	






X = [ListEpoch_NT[0]['NoTarget'].get_data().transpose(0, 2, 1), Data_Epoch_NT_1]
Evoked_NT_01 = ListEpoch_NT[0]['NoTarget'].average()
Evoked_NT_02 = Epoch_NT_1.average()


# organize data for plotting
colors_config = {ListConfig[0]: "tomato", ListConfig[1]: 'green'}
styles_config ={ListConfig[0]: {"linewidth": 0.75},ListConfig[1]: {"linewidth": 0.75}}

evokeds = {ListConfig[0]:Evoked_NT_01,ListConfig[1]:Evoked_NT_02}
p_accept = 0.05
fig_NoTarg = mne_tools.SpatTemp_TFCE_plotCompare(X, colors_config, styles_config, evokeds,p_accept,2000)

fig_NoTarg[0].suptitle( 'NoTarget evoked Responses - ' + ListConfig[0] + ' vs ' + ListConfig[1])
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
fig_NoTarg[0].savefig( RootDirectory_Results + NameSubject + '.' +  'NoTarg_'+ ListConfig[0] + 'vs' + ListConfig[1] + '.png',dpi=400, bbox_inches='tight')
fig_NoTarg[0].canvas.manager.window.showMaximized()


Evoked_DiffConfig = mne.EvokedArray(Evoked_NT_02.get_data()-Evoked_NT_01.get_data(), Evoked_NT_02.info)
times = np.arange(0.05, 0.500, 0.025)
Evoked_DiffConfig.plot_topomap(times, ch_type="eeg")

